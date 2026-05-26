# Camoufox Tuned on Windows

## Current Status

This repository is a Firefox/Camoufox build tree. The main build orchestration is still Unix-oriented: `Makefile`, `bash` scripts, `python3`, `aria2c`, `7z`, `patch`, and Mozilla `mach` are expected. Native PowerShell helper commands such as `patch-firefox.ps1` are not present in this checkout.

The most reliable Windows path is therefore WSL2 or a Linux container/CI runner. A native Windows build is not documented as verified in this repository.

## Prerequisites

- Git
- WSL2 with a Linux distribution, or a Linux CI/container environment
- Python 3.9 or newer for the Firefox build tooling
- Go 1.25 or newer for `bundle/utls_proxy.go`
- `make`, `bash`, `aria2`, `p7zip`, `msitools`, `wget`
- Enough disk space for a Firefox source build. Mozilla documents at least 30 GB free disk space and recommends 8 GB or more RAM.

## Build From WSL2

Run these commands inside the Linux distribution, not from plain PowerShell:

```bash
cd /mnt/c/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned
make fetch
make setup-minimal
python3 scripts/validate_patches.py
make dir
make build
```

Package a build with one of:

```bash
make package-linux arch=x86_64
make package-windows arch=x86_64
make package-windows arch=i686
```

## Tests

After a successful browser build:

```bash
cd tests
bash setup-venv.sh
bash run-tests.sh --executable-path ../camoufox-150.0.3-beta.25/obj-x86_64-pc-linux-gnu/dist/bin/camoufox-bin
```

The exact object directory depends on the selected target architecture.

## Installing Python on the Windows Host

The 2026-05-17 audit found that neither `python` nor `py.exe` resolved on
the host, which forced static checks (`scripts/validate_patches.py`,
`scripts/patch.py --check-conflicts --strict`, `pip-tools`, etc.) to fall
back to the Codex-bundled interpreter. To make local development work
end-to-end on Windows, install Python natively:

1. Install the latest 3.11 or 3.12 from https://www.python.org/downloads/windows/
   (or via `winget install Python.Python.3.12`). Tick **"Add python.exe to
   PATH"** in the installer.
2. Restart the shell and verify:
   ```powershell
   python --version    # should print Python 3.11+ / 3.12+
   py --version        # py.exe launcher
   ```
3. Create an isolated venv for the build tooling (recommended):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
4. For fully reproducible installs, generate a hash-locked lock file
   from `requirements.txt`:
   ```powershell
   pip install pip-tools
   pip-compile --generate-hashes -o requirements.lock requirements.txt
   ```
   then `pip install --require-hashes -r requirements.lock`.

The patch validation gates (`validate_patches.py`,
`patch.py --check-conflicts --strict`) run pure-Python and only need a
recent CPython; they do not require Mozilla `mach` or the full Firefox
toolchain.

## Local Host Notes From The 2026-05-17 Audit

- `make` was not available in the Windows `PATH`.
- `bash.exe` was present, but WSL had no installed Linux distribution.
- Docker Desktop CLI was present, but the Docker daemon was not running.
- `python` was not available in `PATH`; only the Codex bundled Python
  runtime was usable for static checks. See the "Installing Python on
  the Windows Host" section above for the recommended fix.
- The Go toolchain was available and `go build ./...` passed for
  `bundle/`.

## Known Build Risks

- `tests/setup-venv.sh` now installs from the root `requirements.txt`; keep this file in sync with the package metadata.
- The patch conflict checker reports shared Gecko files across `identity`, `media`, and `security`. This is tolerated via `patches/manifests/expected_overlaps.yaml` but is a real maintenance risk when rebasing to a new Firefox version. See K-7 in `AUDIT_2026-05-18.md`.
- The root `Dockerfile` is pinned to `ubuntu:24.04` and installs the Rust toolchain **only** via rustup (Rust 1.94.0, matching the Firefox 150 baseline). The apt-installed `rustc` is intentionally excluded — see the comment block above the rustup install step in `Dockerfile`. Bump `RUSTUP_INIT_VERSION` and `RUST_TOOLCHAIN` together when the Firefox baseline moves.

## Operational security notes (audit 2026-05-18)

- **Identity blob in process environment (K-12).** The launcher chunks
  the Camoufox identity JSON into `CAMOU_CONFIG_1..N` environment
  variables. Any process running under the same UID can read the full
  identity from `/proc/<pid>/environ` on Linux or via the process token
  on Windows. Treat the identity as compromised on multi-tenant hosts.
  A shared-memory replacement is the recommended follow-up but is not
  yet implemented; do not run Camoufox alongside untrusted workloads
  under the same OS user.

- **Broker token is hard requirement on non-loopback binds (K-5).**
  The previously documented `CAMOUFOX_BROKER_ALLOW_UNAUTHENTICATED=1`
  escape hatch has been removed. Tokenless brokers are only allowed
  on `127.0.0.1` / `::1` / `localhost`.

- **uTLS sidecar is off the default path (K-3).** Source moved to
  `bundle/_experimental/`. The default Firefox-native NSS handshake is
  used; do not assume any utls-based fingerprint parity.

- **TLS-cipher-order claim withdrawn (K-1).** `CAMOU_TLS_CIPHERS`
  enables/disables NSS suites but does not control ClientHello order;
  NSS's hard-coded internal order is what hits the wire. This matches
  the Firefox default and is the intended outcome.

- **HTTP/2 SETTINGS not enforced by the build (K-2).** Until
  `Http2Session.cpp` is patched to read `IdentityStateProvider`, the
  launched Firefox emits its native HTTP/2 SETTINGS. For
  Firefox-version-correct profiles this matches a real Firefox client.

Last reviewed: 2026-05-18.
