# Windows build migration: mingw (`*-windows-gnu`) → clang-cl (`*-windows-msvc`)

**Status:** prototype scaffold, iteration 1. Branch `windows-msvc-migration`.
The mingw path (`assets/windows.mozconfig` + all its CI steps) is **left intact
as the fallback** — nothing in this migration touches it.

## Why

The mingw cross-build works around the fact that it is *not* Mozilla's supported
Windows toolchain. It has accreted a dozen documented workarounds, and it has now
hit a wall with no clean mingw-side fix:

- **mozjemalloc DllMain deadlock/crash** (the trigger for this migration): a
  global static ctor allocates during `DLL_PROCESS_ATTACH`, bootstrapping
  mozjemalloc inside mozglue's DllMain, where it reads its own `thread_local`
  (tsd). Under mingw **emulated TLS** that read allocates → re-enters the
  jemalloc init SRW lock → **deadlock**. Under mingw **native TLS**
  (`-fno-emulated-tls`, the fix on branch `remediation/R0-R12`) the `.tls` block
  isn't live in DllMain → garbage pointer → **crash (0xC0000142)**. Both TLS
  models fail in DllMain. On `windows-msvc`, native TLS works in DllMain (as it
  does in every official Firefox build), so the whole class disappears.

Workarounds that **retire** with clang-cl (all are `# ITERATE:`-verify, but each
exists solely because of clang+mingw-gcc-libstdc++):

| Workaround (mingw) | Why it goes away on msvc |
| --- | --- |
| `-femulated-tls` | MSVC native TLS; no emutls |
| jemalloc DllMain deadlock/crash | native TLS works in DllMain |
| missing `libssp-0.dll` | MSVC CRT provides `__security_*`, no libssp |
| `--allow-multiple-definition` | uses MSVC STL, no libstdc++ COMDAT clash |
| `-static-libstdc++ -static-libgcc` | MSVC CRT, no libstdc++/libgcc |
| `--disable-debug-symbols` (PDB/lld crash) | clang-cl PDBs work; can re-enable |
| `--disable-lto` (mingw LTO fail) | cross-LTO supported on msvc |
| `--disable-notification-server` | upstream builds it on clang-cl |
| `ci_fix_mingw_dcomp.py` (dcomp.h backfill) | Win SDK ships current dcomp.h |
| `bcryptprimitives.a` synth | Win SDK ships the import lib |
| `-fms-extensions` / enum-forward-ref hacks | clang-cl accepts MSVC-isms |
| `cc`/`cxx` compiler wrappers | not needed |
| posix-threads mingw gcc for `std::__once_callable` | MSVC STL |

## Toolchain (Linux host → windows-msvc)

- **clang-cl + lld-link + llvm-lib** from host llvm-18 (already installed for the
  linux/win legs; `base.mozconfig` pins libclang to `/usr/lib/llvm-18/lib`).
- **MSVC CRT + Windows SDK** via [`xwin`](https://github.com/Jake-Shadle/xwin) —
  `scripts/setup_xwin.sh` downloads + `splat`s them to `$XWIN_ROOT` (`~/.xwin`),
  case-corrected. Microsoft's license permits this for building.
- **No DIA SDK** needed — `base.mozconfig` sets `--disable-crashreporter`.
- **Assembler:** `llvm-ml` (MASM-compatible) replaces `ml64.exe`. `# ITERATE`.
- **HLSL (fxc):** reuse the existing fxc2 + `wine-fxc-wrapper` unchanged
  (toolchain-independent).

## Files in this scaffold

- `assets/windows-msvc.mozconfig` — the clang-cl toolchain config (target,
  CC/CXX=clang-cl, lld-link, xwin `-imsvc`/`-libpath:` paths, assembler). Blocks
  marked `# ITERATE:` are the known-unknowns to resolve against build output.
- `scripts/setup_xwin.sh` — fetch + splat MSVC/SDK (pinned `XWIN_VERSION`, cached
  via `$XWIN_ROOT/.splat-done`).

## Plumbing changes still needed (NOT yet written — do in iteration 1)

1. **`scripts/_mixin.py` `get_moz_target()`** — map target `windows-msvc` →
   `{arch}-pc-windows-msvc`. Add `"windows-msvc"` to `AVAILABLE_TARGETS`.
2. **`scripts/patch.py`** — `_update_mozconfig` already appends
   `assets/<target>.mozconfig`; with target `windows-msvc` it picks up the new
   file automatically. Verify `add_rustup(...)` gets `{arch}-pc-windows-msvc`.
3. **`multibuild.py`** — allow `windows-msvc` as a build target so
   `BUILD_TARGET=windows-msvc,<arch>` is exported.
4. **`.github/workflows/build.yml`** — add a matrix leg (or a `workflow_dispatch`
   input `win_toolchain: mingw|msvc`) that, for `windows-msvc`:
   - installs `clang-tools`/`lld`/`llvm` (llvm-18) + runs `scripts/setup_xwin.sh`
     instead of the mingw apt-get block (lines ~308-349);
   - skips the mingw-only steps: bcryptprimitives synth, `ci_fix_mingw_dcomp.py`,
     the `-femulated-tls` probe, the windres symlinks;
   - keeps: wine (for fxc2), zstd, the fxc2/wine-fxc-wrapper setup.
   - exports `XWIN_ROOT` and puts `llvm-ml`/`clang-cl` on `PATH`.

## Iteration strategy (each CI build is hours — minimize blind cycles)

Run `only_target=windows-msvc` (once the matrix leg exists) and expect to iterate
on, roughly in the order they'll surface:
1. **configure**: mach finding clang-cl, the SDK (`WINDOWSSDKDIR`), the assembler,
   and the linker. Most first-run failures are here and are fast (minutes).
2. **assembler**: `llvm-ml` vs `ml64.exe` expectations (js/, media/, security/nss).
3. **HLSL/fxc** for ANGLE.
4. **link** (lld-link): missing `-libpath:` entries, `raw-dylib` (works on msvc,
   so bcryptprimitives synth is unneeded).
5. **package**: `--disable-notification-server` no longer needed; ensure the
   manifest matches what clang-cl actually produces (e.g. no `libssp-0.dll`).

Add a **launch smoke test** to CI before trusting any green (the whole reason the
mingw builds shipped dead): after packaging, run the exe under wine64 headless
(`camoufox.exe -headless -screenshot ... https://example.com`) or on a Windows
runner, and fail the job if it doesn't produce output. windows-msvc under wine is
far more likely to run than validating on the cross host.

## Fallback

`assets/windows.mozconfig` (mingw) + `remediation/R0-R12` remain the shipping
path until windows-msvc is green **and** passes the launch smoke test. Only then
switch the default `windows` target over (or make msvc the default and keep mingw
behind a flag).
