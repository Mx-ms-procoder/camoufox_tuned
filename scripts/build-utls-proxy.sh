#!/usr/bin/env bash
# Build the experimental uTLS sidecar from source.
#
# This binary used to live in bundle/utls_proxy{,.exe} as a checked-in
# artifact. It was removed in K-8 / AUDIT_2026-05-18.md because:
#   • shipping ~27 MB of opaque binaries in an anti-detect repo defeats
#     reproducibility;
#   • no registered TLS profile selects the sidecar anyway, so the
#     binary on the default path was dead;
#   • CI already builds it inside Dockerfile.slim's go-builder stage.
#
# If you actually need the sidecar locally, run this script.

set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
src_dir="$repo_root/bundle/_experimental"
out_dir="$repo_root/bundle/_experimental/build"
mkdir -p "$out_dir"

cd "$src_dir"

if ! command -v go >/dev/null 2>&1; then
    echo "go toolchain not found in PATH. Install Go 1.25+ first." >&2
    exit 1
fi

# Linux x86_64 (typical CI runner target)
echo "[build-utls-proxy] building linux/amd64..."
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o "$out_dir/utls_proxy" ./utls_proxy.go

# Windows x86_64 (only build if requested, since it requires cross headers)
if [ "${BUILD_WINDOWS:-0}" = "1" ]; then
    echo "[build-utls-proxy] building windows/amd64..."
    CGO_ENABLED=0 GOOS=windows GOARCH=amd64 \
        go build -ldflags="-s -w" -o "$out_dir/utls-proxy.exe" ./utls_proxy.go
fi

echo "[build-utls-proxy] wrote artifacts to: $out_dir"
ls -lh "$out_dir"

cat <<NOTE

NOTE: this binary is EXPERIMENTAL. Nothing in the default Camoufox
launch path uses it. utls v1.8.2 has no HelloFirefox_150 parrot, so
even when run, its ClientHello will not match a Firefox 150 UA.
See K-3 in AUDIT_2026-05-18.md.
NOTE
