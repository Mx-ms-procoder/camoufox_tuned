#!/bin/bash
# Wine wrapper for fxc2.exe shader compilation.
#
# Wine's d3dcompiler resolves the source-file directory for relative #include
# via strrchr(path, '\\'), so forward-slash paths break Mozilla's HLSL build
# with E4002 ("Failed to open BlendShaderConstants.h") even when the file is
# on disk next to CompositorD3D11.hlsl. This wrapper rewrites Unix-style .hlsl
# arguments into wine Z:-drive paths with backslashes. Translating only .hlsl
# inputs keeps every other argument (flags, output spec, defines) untouched.
set -eu

# The workflow may install this wrapper AT /usr/lib/wine/wine64 (after
# backing up the original to .real) so that mach's hardcoded path-based
# wine detection still goes through us. In that layout we must (a) prefer
# the *.real backups, and (b) defensively skip any candidate that resolves
# to ourselves to avoid an infinite exec loop.
SELF="$(readlink -f -- "$0" 2>/dev/null || echo "$0")"
REAL_WINE=""
for candidate in \
    /usr/lib/wine/wine64.real \
    /usr/lib/x86_64-linux-gnu/wine/wine64.real \
    /usr/bin/wine64.real \
    /usr/bin/wine.real \
    /usr/lib/wine/wine64 \
    /usr/lib/x86_64-linux-gnu/wine/wine64 \
    /usr/bin/wine64 \
    /usr/bin/wine; do
    if [ ! -x "$candidate" ]; then
        continue
    fi
    resolved="$(readlink -f -- "$candidate" 2>/dev/null || echo "$candidate")"
    if [ "$resolved" = "$SELF" ]; then
        continue
    fi
    REAL_WINE="$candidate"
    break
done
if [ -z "$REAL_WINE" ]; then
    echo "wine-fxc-wrapper: cannot find real wine64 binary" >&2
    exit 1
fi

args=()
for arg in "$@"; do
    case "$arg" in
        *.hlsl|*.hlsli)
            if [ -f "$arg" ]; then
                abs="$(readlink -f -- "$arg")"
                args+=("Z:${abs//\//\\}")
            else
                args+=("$arg")
            fi
            ;;
        *)
            args+=("$arg")
            ;;
    esac
done

if [ ${#args[@]} -eq 0 ]; then
    exec "$REAL_WINE"
else
    exec "$REAL_WINE" "${args[@]}"
fi
