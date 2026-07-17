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
"$tmp/xwin" --accept-license --arch "$XWIN_ARCHES" splat --output "$XWIN_ROOT"

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
