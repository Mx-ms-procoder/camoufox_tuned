# Comprehensive Project Audit — Camoufox Enhanced (camoufox_updated_captcha)

> **Scope**: Every file in the project — Python, C++, Go, YAML, Dockerfiles, Makefiles, shell scripts, JSON, patches.  
> **Date**: 2026-05-03  
> **Base**: `camoufox-135.0.1-beta.24`

---

## Table of Contents

1. [Bug Audit](#1-bug-audit)
2. [Performance & Legacy Review](#2-performance--legacy-review)
3. [Security Vulnerability Profile](#3-security-vulnerability-profile)
4. [Benchmarking vs. Upstream Camoufox](#4-benchmarking-vs-upstream-camoufox)

---

## 1. Bug Audit

### 1.1 — Critical Bugs

| # | File | Language | Issue | Severity |
|---|------|----------|-------|----------|
| B01 | `scripts/_mixin.py:215-218` | Python | **Path separator mismatch on CI (Linux)**. `list_files()` returns forward-slash paths, but `os.path.join()` on Windows produces backslash paths for `claimed_paths`. The `path not in claimed_paths` comparison fails because `./patches\\core/foo.patch ≠ ./patches/core/foo.patch`. This was the **root cause** of the `Unclaimed patch files` error. **Fixed earlier this session** by deleting the root-level duplicates, but the underlying path normalization bug remains. | 🔴 Critical |
| B02 | `Makefile:90` | Make | **`ff-dbg` references deleted root patches**. `make patch ./patches/chromeutil.patch` and `./patches/browser-init.patch` — these were the root-level duplicates we deleted. `ff-dbg` will now fail with "file not found". | 🔴 Critical |
| B03 | `Makefile:202` | Make | **`make grep` searches deleted root patches**. `grep "$(_ARGS)" -r ./patches/*.patch` — the glob `./patches/*.patch` now returns nothing (all patches are in subdirectories). | 🟡 Medium |
| B04 | `scripts/developer.py:9` | Python | **Unconditional `import easygui`** crashes headless/CI environments. `easygui` is a GUI library that fails on Linux servers without an X display. | 🟡 Medium |
| B05 | `scripts_macros/captcha/captchas_solver/base_solver.py:181` | Python | **Deprecated `asyncio.get_event_loop()`**. In Python 3.10+, calling `get_event_loop()` outside a running loop raises `DeprecationWarning` and may return `None` in 3.12+. Should use `asyncio.get_running_loop()`. | 🟡 Medium |
| B06 | `scripts_macros/captcha/captchas_solver/base_solver.py:87` | Python | **Bare `except: continue`** swallows all exceptions including `KeyboardInterrupt` and `SystemExit`. Should be `except Exception:`. | 🟡 Medium |
| B07 | `scripts_macros/captcha/captchas_solver/base_solver.py:177` | Python | **Another bare `except: continue`** in the SSE stream parser. | 🟡 Medium |
| B08 | `bundle/utls_proxy.go:449` | Go | **`DialTLS` is deprecated** in Go's `net/http`. Should use `DialTLSContext` instead. Older Go compilers warn; newer may remove it. | 🟡 Medium |
| B09 | `bundle/utls_proxy.go:456-461` | Go | **HTTP/2 SETTINGS are never actually applied**. The code calls `http2.ConfigureTransports(transport)` but then does `_ = h2Transport`, discarding the handle without configuring any custom settings. The comment says "Settings applied via ConfigureTransports" — this is incorrect; `ConfigureTransports` only *enables* HTTP/2, it does not inject custom SETTINGS frames. | 🔴 Critical |
| B10 | `additions/camoucfg/MaskConfig.hpp:40` | C++ | **`std::wstring_convert` is deprecated** in C++17 and removed in C++26. The MSVC build may warn. | 🟡 Medium |
| B11 | `additions/camoucfg/MouseTrajectories.hpp:17-21` | C++ | **Factorial overflow** for n > 20. `long long` can hold up to ~19! — anything above silently overflows, producing incorrect Bezier curves. Unlikely to trigger in practice (curves rarely have >20 control points) but unsafe. | 🟢 Low |
| B12 | `multibuild.py:126` | Python | **Typo**: `"Unsuported"` → `"Unsupported"`. | 🟢 Low |
| B13 | `Dockerfile:1` | Docker | **`FROM ubuntu:latest`** is unpinned. Builds are non-reproducible; a new Ubuntu release could silently break the build. | 🟡 Medium |
| B14 | `.github/workflows/build.yml:55` | YAML | **`actions/checkout@v2`** is deprecated. Should use `@v4`. Same for `actions/setup-go@v2` and `actions/setup-python@v2`. | 🟡 Medium |
| B15 | `Dockerfile.slim:60-66` | Docker | **`pip install` has a broken fallback**. The `||` fallback chain is a single `RUN` with mixed `--break-system-packages` and non-`--break-system-packages` invocations, which will fail on either Ubuntu 22.04 or 23.04+ but not both. | 🟡 Medium |
| B16 | `pythonlib/camoufox/cloud_native.py:423` | Python | **S3 `NoSuchKey` exception path wrong**. `self._s3.exceptions.NoSuchKey` — `boto3` client exceptions are accessed via `self._s3.exceptions.NoSuchKey` only for *resource* clients. For low-level `boto3.client("s3")`, use `botocore.exceptions.ClientError` with error code check. | 🟡 Medium |
| B17 | `scripts_macros/captcha/scanner.py:54` | Python | **Mixed line endings** (`\r\n` and `\n` within the same file). This can cause issues with `git diff`, patch generation, and some CI linters. | 🟢 Low |

### 1.2 — Edge Cases

| # | File | Issue |
|---|------|-------|
| E01 | `_mixin.py:232-233` | `is_bootstrap_patch()` regex `\d+\-.*` matches any patch starting with digits. A patch named `135-fix.patch` would silently be treated as a bootstrap patch and skipped by validation. |
| E02 | `bundle/utls_proxy.go:170-171` | Certificate cache eviction is "nuke everything at 4096" — under sustained load, every 4097th connection pays the cost of regenerating ALL cached certs simultaneously. Should use LRU or sharded eviction. |
| E03 | `cloud_native.py:325-339` | Redis `PoolManager.acquire()` uses `KEYS *` pattern scan — O(N) on the entire Redis keyspace. With many workers, this becomes a bottleneck. Should use a sorted set or hash for O(1) lookups. |
| E04 | `cloud_native.py:362` | `HINCRBY active_sessions -1` can go negative if `release()` is called twice for the same `session_id` (idempotency not guaranteed). |

---

## 2. Performance & Legacy Review

### 2.1 — Performance Bottlenecks

| # | Location | Issue | Impact |
|---|----------|-------|--------|
| P01 | `additions/camoucfg/json.hpp` (920KB) | **nlohmann/json single-header** is ~920KB of header-only C++ compiled into every translation unit that includes `MaskConfig.hpp`. This is the single largest compile-time bottleneck. | Build time |
| P02 | `scripts_macros/captcha/scanner.py` (67KB) | **1510-line monolithic JS injection string**. The entire deep-scan JS is a single Python raw string compiled and `evaluate()`d every scan interval. No minification, no caching of compiled result. | Runtime memory |
| P03 | `bundle/utls_proxy.go:448-452` | **New `http.Transport` per HTTP request**. The `handleHTTP()` method creates a fresh transport (and thus a fresh TLS connection) for every non-CONNECT request. No connection pooling. | Network latency |
| P04 | `cloud_native.py:325-339` | **`KEYS *` Redis scan** (mentioned above as E03). | Redis CPU |
| P05 | `pythonlib/camoufox/utils.py` (25KB) | `launch_options()` is called per session creation — it re-reads fonts.json, processes WebGL configs, and does browserforge lookups every time. Could be cached per profile. | Session creation latency |

### 2.2 — Deprecated Methods & Obsolete Libraries

| # | Item | Status | Replacement |
|---|------|--------|-------------|
| D01 | `optparse` in `_mixin.py`, `bootstrap.py` | Deprecated since Python 3.2 | `argparse` |
| D02 | `std::wstring_convert` in `MaskConfig.hpp` | Deprecated C++17, removed C++26 | Win32 `WideCharToMultiByte()` or `std::filesystem::path` |
| D03 | `asyncio.get_event_loop()` in `base_solver.py` | Deprecated Python 3.10+ | `asyncio.get_running_loop()` |
| D04 | `actions/checkout@v2`, `actions/setup-go@v2`, `actions/setup-python@v2` | v2 is unmaintained | `@v4` |
| D05 | `playwright==1.48.0` in `requirements.txt` | Pinned to old version | Update to latest (1.52+) |
| D06 | `golang:1.21-bookworm` in `Dockerfile.slim` | Go 1.21 is EOL | `golang:1.22-bookworm` or later |

### 2.3 — Unnecessary / Redundant Files

| File | Issue |
|------|-------|
| `tmpsccpeg9m/` directory | Leftover temp directory in project root. Should be gitignored/deleted. |
| `camoufox-analysis.md` (42KB) | Analysis document in repo root — should be in docs/ or removed from release builds. |
| `camoufox-cloud-native-blueprint.md` (8KB) | Design blueprint — same as above. |
| `scripts/__pycache__/` | Compiled Python bytecode committed to repo. Should be gitignored. |
| `scripts_macros/__pycache__/` | Same issue. |
| `bundle/.gocache/` | Go build cache in repo. Should be gitignored. |

### 2.4 — Redundant Entry Points

| Entry Point | Issue |
|-------------|-------|
| `scripts/bootstrap.py` | **This is Mozilla's upstream bootstrap.py for cloning mozilla-unified**. It's not used by the Camoufox build at all (the Makefile uses `make setup` → `make fetch` instead). It's dead code that adds confusion. |
| `Makefile:ff-dbg` | References patches that no longer exist at the expected paths (root-level patches were deleted). This target is now broken. |

---

## 3. Security Vulnerability Profile

### 3.1 — Architectural Weaknesses

| # | Category | Weakness | Risk |
|---|----------|----------|------|
| S01 | **TLS Interception** | MitM mode generates an ephemeral CA that isn't pinned or verified by the browser. Any process on the machine can generate certs. The CA private key lives in memory with no protection. | 🔴 High — if deployed in shared environments, other pods could intercept traffic |
| S02 | **Environment Variable Secrets** | `CAMOU_CONFIG` passes the entire identity fingerprint (including session secrets) as an environment variable. On Linux, any process can read another process's environment via `/proc/<pid>/environ`. On shared hosting or K8s without proper isolation, this leaks the full identity. | 🔴 High |
| S03 | **No authentication on Session Broker** | The HTTP server at `0.0.0.0:8000` has zero authentication. Any pod or network neighbor can create/delete sessions. | 🔴 High |
| S04 | **Redis without TLS** | `redis://camoufox-redis:6379/0` — unencrypted. In the K8s manifests, Redis secrets are stored as `stringData` (base64, not encrypted). | 🟡 Medium |
| S05 | **No rate limiting** | Session Broker accepts unlimited POST /sessions requests. Trivial to exhaust worker pool. | 🟡 Medium |
| S06 | **`os.system()` shell injection** | `_mixin.py:run()`, `_mixin.py:patch()`, and `developer.py` pass user-controlled strings through `os.system()` with no escaping. An attacker who can influence patch filenames can inject arbitrary shell commands. | 🟡 Medium (requires control of patch names) |
| S07 | **NVIDIA API key leakage** | `base_solver.py` falls back to `os.environ.get("NVIDIA_API_KEY")` — the key is also embedded in the `requests.post()` call with no redaction in error logs. | 🟡 Medium |
| S08 | **Docker runs as root** | Both `Dockerfile` and `Dockerfile.slim` compile/build as root. The slim image creates a `camoufox` user but never switches to it (`USER camoufox` is missing). | 🟡 Medium |

### 3.2 — Points of Failure

| # | Component | Failure Mode |
|---|-----------|--------------|
| F01 | **Patch validation in CI** | A single broken patch manifest or path mismatch causes the entire build to abort. No partial-build fallback. |
| F02 | **uTLS sidecar crash** | No automatic restart mechanism. If the Go sidecar crashes, the browser continues making requests through plain TCP (transparent mode), completely unmasked. |
| F03 | **Redis dependency** | If Redis is down, the session broker fails open — `health_check()` returns `False` but sessions are still created with the in-memory fallback only if configured. |
| F04 | **Single `json.hpp` parse** | `MaskConfig::GetJson()` uses `std::call_once` — if the first parse fails (malformed JSON), ALL subsequent calls return an empty config for the entire process lifetime with no way to retry. |

---

## 4. Benchmarking vs. Upstream Camoufox

### 4.1 — Architecture Comparison

| Dimension | Upstream Camoufox | This Fork | Verdict |
|-----------|-------------------|-----------|---------|
| **Identity Coherence** | JavaScript-level property spoofing via `MaskConfig.hpp` direct lookups scattered across patches | Added `IdentityStateProvider.hpp` — C++ caching layer with `std::call_once` per subsystem, typed state structs, cross-subsystem validation (WebGL viewport ≥ screen) | 🟢 **Superior** — structured, type-safe, cache-once |
| **TLS Fingerprinting** | NSS defaults only — no JA3/JA4 control | Added `CamouTLSOverride.hpp` (NSS cipher/group/sigalg env-var overrides) + Go uTLS sidecar with MitM mode + `tls_profiles.py` with Firefox 135 profile data + `TLSProfileValidator` | 🟢 **Superior** — dual-layer TLS control (NSS native + sidecar fallback) |
| **HTTP/2 Fingerprinting** | Default Firefox Http2Session | Added `FIREFOX_135_HTTP2` template with captured SETTINGS values (headerTableSize, windowUpdate, etc.) | 🟡 **Partially Superior** — templates exist but B09 shows they're not actually applied in the sidecar |
| **Patch Management** | Flat list of `.patch` files, manual ordering | YAML manifests with named features, conflict detection, `is_bootstrap_patch()`, per-bundle application, validation CI step | 🟢 **Superior** — modular, auditable, CI-enforced |
| **Cloud-Native** | Not supported | Added `cloud_native.py` (session broker, snapshot stores, pool managers), K8s manifests, `Dockerfile.slim` multi-stage | 🟢 **Superior** — not present in upstream at all |
| **CAPTCHA Solving** | Not supported | Added `scripts_macros/captcha/` — multi-provider scanner (reCAPTCHA v2/v3, hCaptcha, Turnstile, TikTok Rotate/Slide/3D), Nvidia Vision API solver | 🟢 **Superior** — significant value-add not in upstream |
| **Mouse Humanization** | `MouseTrajectories.hpp` (Bezier curves) | Same implementation | 🟡 **Parity** |
| **Build System** | Makefile + `patch.py` | Same core, plus `validate_patches.py`, conflict detection | 🟢 **Superior** |

### 4.2 — Stealth Assessment

| Signal | Upstream | This Fork | Notes |
|--------|----------|-----------|-------|
| **Navigator props** | Spoofed via MaskConfig | Same + coherence validation | Parity |
| **Screen/Display** | Spoofed | Same + cross-ref with WebGL viewport | Slightly better |
| **Canvas/WebGL** | Noise injection + param spoofing | Same | Parity |
| **TLS JA3/JA4** | ❌ No control — plain NSS | ✅ NSS cipher ordering + uTLS sidecar | **Major advantage** |
| **HTTP/2 SETTINGS** | ❌ Default Firefox | ⚠️ Templates defined but B09 means sidecar doesn't apply them | **Not yet functional** |
| **Font fingerprinting** | Spoofed list + spacing seed | Same | Parity |
| **Audio fingerprinting** | Context spoofing | Same | Parity |
| **Timezone/Geo/Locale** | Spoofed | Same | Parity |
| **WebRTC IP** | Patched | Same | Parity |
| **CSS Animations** | Disabled | Same | Parity |

### 4.3 — Overall Verdict

```
┌─────────────────────────────────────────────────────────────────┐
│                    OVERALL ASSESSMENT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  This fork is ARCHITECTURALLY SUPERIOR to upstream Camoufox     │
│  in 5 of 8 key dimensions.                                     │
│                                                                 │
│  Critical gaps that prevent "market-leading" status:            │
│                                                                 │
│  1. HTTP/2 SETTINGS are defined but never applied (B09)         │
│  2. uTLS sidecar creates new Transport per request (P03)        │
│  3. Session broker has zero authentication (S03)                │
│  4. CAMOU_CONFIG env-var identity leak (S02)                    │
│  5. Makefile references to deleted root-level patches (B02)     │
│                                                                 │
│  Fix these 5 items and this fork achieves the strongest         │
│  anti-fingerprint posture of any open-source Firefox variant.   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Recommended Priority Fixes

> [!IMPORTANT]
> These are the 5 fixes that should be applied **before the next push** to unblock the build and close the most critical gaps.

### Fix 1: Update Makefile `ff-dbg` target (B02)

```diff
-	make patch ./patches/chromeutil.patch
-	make patch ./patches/browser-init.patch
+	make patch ./patches/core/chromeutil.patch
+	make patch ./patches/core/browser-init.patch
```

### Fix 2: Update Makefile `grep` target (B03)

```diff
-	grep "$(_ARGS)" -r ./patches/*.patch
+	grep "$(_ARGS)" -r ./patches/
```

### Fix 3: Normalize paths in `_mixin.py` list_patches (B01)

Replace the `path not in claimed_paths` check with normalized comparison:

```diff
+    claimed_normalized = {os.path.normpath(p) for p in claimed_paths}
     unclaimed_paths = [
         path for path in all_patch_paths
-        if not is_bootstrap_patch(path) and path not in claimed_paths
+        if not is_bootstrap_patch(path) and os.path.normpath(path) not in claimed_normalized
     ]
```

### Fix 4: Update GitHub Actions versions (B14)

```diff
-      - uses: actions/checkout@v2
+      - uses: actions/checkout@v4
-      - uses: actions/setup-go@v2
+      - uses: actions/setup-go@v5
-      - uses: actions/setup-python@v2
+      - uses: actions/setup-python@v5
```

### Fix 5: Add `USER camoufox` to Dockerfile.slim (S08)

```diff
 # Default: run session broker
+USER camoufox
 CMD ["python3", "-m", "camoufox", "cloud-broker", \
```
