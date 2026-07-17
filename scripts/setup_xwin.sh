#!/bin/sh
# Fetch the MSVC CRT + Windows SDK for a clang-cl windows-msvc cross-build.
#
# Used by the windows-msvc build leg (assets/windows-msvc.mozconfig) instead of
# the mingw apt-get toolchain. `xwin splat` downloads Microsoft's redistributable
# CRT/SDK packages and lays them out case-corrected under $XWIN_ROOT:
#   $XWIN_ROOT/crt/{include,lib/<arch>}
#   $XWIN_ROOT/sdk/{include/{ucrt,um,shared,winrt},lib/{ucrt,um}/<arch>}
#
# Microsoft's license permits downloading these for building. Pin XWIN_VERSION so
# the toolchain is reproducible; bump deliberately.
set -eu

XWIN_VERSION="${XWIN_VERSION:-0.6.5}"
XWIN_ROOT="${XWIN_ROOT:-$HOME/.xwin}"
# splat only the arches we build; default both.
XWIN_ARCHES="${XWIN_ARCHES:-x86_64,x86}"

if [ -f "$XWIN_ROOT/.splat-done" ]; then
    echo "xwin sysroot already present at $XWIN_ROOT (cached)"
    exit 0
fi

tmp="$(mktemp -d)"
url="https://github.com/Jake-Shadle/xwin/releases/download/${XWIN_VERSION}/xwin-${XWIN_VERSION}-x86_64-unknown-linux-musl.tar.gz"
echo "Downloading xwin ${XWIN_VERSION} ..."
curl --fail -L "$url" | tar -xz -C "$tmp" --strip-components=1

echo "Splatting MSVC CRT + Windows SDK to $XWIN_ROOT (arches: $XWIN_ARCHES) ..."
# --preserve-ms-arch-notation: emit MS arch dir names (x64/x86) instead of
# xwin's default x86_64/x86, because Firefox's windows.configure maps its target
# to the MS notation (x86_64 -> x64) when it looks for <vc_path>/lib/<arch> and
# <vc_path>/atlmfc/lib/<arch>. Without this the isdir checks miss.
"$tmp/xwin" --accept-license --arch "$XWIN_ARCHES" splat \
    --preserve-ms-arch-notation --output "$XWIN_ROOT"

# xwin ships no ATL/MFC, but Firefox's windows.configure hard-requires the
# directories <vc_path>/atlmfc/include and <vc_path>/atlmfc/lib/<msarch> to
# EXIST (plain os.path.isdir checks — it does not read their contents at
# configure time). Create empty stubs so configure proceeds; this is a PROBE:
# if any translation unit actually `#include`s an ATL header we'll get a clear
# "atlbase.h not found" compile error and must then source real ATL (msvc-wine).
mkdir -p "$XWIN_ROOT/crt/atlmfc/include"
for a in x64 x86 arm64 arm; do
    mkdir -p "$XWIN_ROOT/crt/atlmfc/lib/$a"
done

# xwin already symlinks the common case variants, but Firefox's SDK includes
# reference a few headers with casings xwin's heuristic can miss. Belt-and-suspenders:
# make every include dir tolerant by lowercasing-symlinking any not-yet-linked header.
# (No-op once xwin's own pass covers them; cheap.)
for d in "$XWIN_ROOT"/crt/include "$XWIN_ROOT"/sdk/include/*; do
    [ -d "$d" ] || continue
    find "$d" -maxdepth 1 -type f -name '*[A-Z]*' 2>/dev/null | while read -r f; do
        lc="$(dirname "$f")/$(basename "$f" | tr '[:upper:]' '[:lower:]')"
        [ -e "$lc" ] || ln -s "$(basename "$f")" "$lc" 2>/dev/null || true
    done
done

touch "$XWIN_ROOT/.splat-done"
rm -rf "$tmp"
echo "xwin sysroot ready at $XWIN_ROOT"
du -sh "$XWIN_ROOT" 2>/dev/null || true
