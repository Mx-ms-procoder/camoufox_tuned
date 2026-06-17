#!/usr/bin/env python3
"""Backfill Windows 11-era DirectComposition interfaces into an old mingw-w64
``dcomp.h``.

Ubuntu 24.04 ships mingw-w64 11.0.1 (2023), whose ``dcomp.h`` predates and
therefore lacks ``IDCompositionDevice4`` (``CreateCompositionTexture`` /
``CheckCompositionTextureSupport``), ``IDCompositionTexture`` and the
``IDCompositionColorMatrixEffect`` / ``IDCompositionTableTransferEffect``
color-management effects. It also stubs
``IDCompositionDevice3::CreateColorMatrixEffect`` /
``CreateTableTransferEffect`` as ``void **`` TODOs.

Firefox 150's ``gfx/webrender_bindings`` (DCLayerTree.cpp,
RenderD3D11TextureHost.cpp) uses all of those. MSVC's SDK has them, so Mozilla
never hits this gap. Rather than ``#ifdef``-ing the whole DComposition-texture +
color-management subsystem out of Firefox source (invasive, and it would disable
real features), we patch the system header itself -- the clean fix that makes
every consumer compile at once and keeps all features enabled. This is exactly
what a newer mingw-w64 ``dcomp.h`` already provides.

Three edits, each mirroring a newer upstream mingw-w64 ``dcomp.h`` verbatim:

  (a) retype Device3's two ``void **`` effect-factory stubs so Firefox's typed
      ``getter_AddRefs(RefPtr<...Effect>)`` argument binds;
  (b) forward-declare the four missing interfaces just before Device3 (its
      retyped pointer-to-pointer params reference them);
  (c) append the four full interface definitions -- with ``__CRT_UUID_DECL`` so
      ``__uuidof`` / ``RefPtr::QueryInterface<T>`` resolve -- before the include
      guard's closing ``#endif``.

Idempotent and tolerant: a ``dcomp.h`` that already declares
``IDCompositionDevice4`` (a newer toolchain, or a re-run) is left untouched.

Usage:  ci_fix_mingw_dcomp.py <path/to/dcomp.h>
"""
import re
import sys

# (b) Forward declarations injected before Device3. `interface` is == struct this
# deep in dcomp.h (objbase.h has long since defined it), matching mingw's own
# widl forward-decl idiom and working in both C and C++ translation units.
FORWARD_DECLS = (
    '/* camoufox: forward-declare DComposition interfaces absent in mingw-w64 11.0.1 */\n'
    '#ifndef __IDCompositionColorMatrixEffect_FWD_DEFINED__\n'
    '#define __IDCompositionColorMatrixEffect_FWD_DEFINED__\n'
    'typedef interface IDCompositionColorMatrixEffect IDCompositionColorMatrixEffect;\n'
    '#endif\n'
    '#ifndef __IDCompositionTableTransferEffect_FWD_DEFINED__\n'
    '#define __IDCompositionTableTransferEffect_FWD_DEFINED__\n'
    'typedef interface IDCompositionTableTransferEffect IDCompositionTableTransferEffect;\n'
    '#endif\n'
    '#ifndef __IDCompositionTexture_FWD_DEFINED__\n'
    '#define __IDCompositionTexture_FWD_DEFINED__\n'
    'typedef interface IDCompositionTexture IDCompositionTexture;\n'
    '#endif\n'
    '#ifndef __IDCompositionDevice4_FWD_DEFINED__\n'
    '#define __IDCompositionDevice4_FWD_DEFINED__\n'
    'typedef interface IDCompositionDevice4 IDCompositionDevice4;\n'
    '#endif\n'
)

# (c) Full interface definitions appended before the include guard's closing
# #endif. Defensive includes pull in the D2D/DXGI value types the signatures
# reference (D2D1_MATRIX_5X4_F, D2D1_COLORMATRIX_ALPHA_MODE, D2D_RECT_U,
# DXGI_COLOR_SPACE_TYPE, DXGI_ALPHA_MODE). Wrapped in the same
# `_WIN32_WINNT >= 0x0603` guard that gates Device3, so availability tracks it.
INTERFACE_DEFS = r'''
/* camoufox: IDCompositionDevice4 + dependencies backfilled for mingw-w64 11.0.1 */
#if (_WIN32_WINNT >= 0x0603)
#include <d2d1.h>
#include <d2d1effects.h>
#include <dxgicommon.h>

#undef INTERFACE
#define INTERFACE IDCompositionColorMatrixEffect
DECLARE_INTERFACE_IID_(IDCompositionColorMatrixEffect, IDCompositionFilterEffect, "C1170A22-3CE2-4966-90D4-55408BFC84C4")
{
    STDMETHOD(SetMatrix)(THIS_ const D2D1_MATRIX_5X4_F &matrix) PURE;
#if defined(_MSC_VER) && defined(__cplusplus)
    STDMETHOD(SetMatrixElement)(THIS_ int row, int column, float value) PURE;
    STDMETHOD(SetMatrixElement)(THIS_ int row, int column, IDCompositionAnimation *animation) PURE;
#else
    STDMETHOD(SetMatrixElement)(THIS_ int row, int column, IDCompositionAnimation *animation) PURE;
    STDMETHOD(SetMatrixElement)(THIS_ int row, int column, float value) PURE;
#endif
    STDMETHOD(SetAlphaMode)(THIS_ D2D1_COLORMATRIX_ALPHA_MODE mode) PURE;
    STDMETHOD(SetClampOutput)(THIS_ BOOL clamp) PURE;
};
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(IDCompositionColorMatrixEffect,0xc1170a22,0x3ce2,0x4966,0x90,0xd4,0x55,0x40,0x8b,0xfc,0x84,0xc4)
#endif

#undef INTERFACE
#define INTERFACE IDCompositionTableTransferEffect
DECLARE_INTERFACE_IID_(IDCompositionTableTransferEffect, IDCompositionFilterEffect, "9B7E82E2-69C5-4EB4-A5F5-A7033F5132CD")
{
    STDMETHOD(SetRedTable)(THIS_ const float *tableValues, UINT count) PURE;
    STDMETHOD(SetGreenTable)(THIS_ const float *tableValues, UINT count) PURE;
    STDMETHOD(SetBlueTable)(THIS_ const float *tableValues, UINT count) PURE;
    STDMETHOD(SetAlphaTable)(THIS_ const float *tableValues, UINT count) PURE;
    STDMETHOD(SetRedDisable)(THIS_ BOOL redDisable) PURE;
    STDMETHOD(SetGreenDisable)(THIS_ BOOL greenDisable) PURE;
    STDMETHOD(SetBlueDisable)(THIS_ BOOL blueDisable) PURE;
    STDMETHOD(SetAlphaDisable)(THIS_ BOOL alphaDisable) PURE;
    STDMETHOD(SetClampOutput)(THIS_ BOOL clampOutput) PURE;
#if defined(_MSC_VER) && defined(__cplusplus)
    STDMETHOD(SetRedTableValue)(THIS_ UINT index, float value) PURE;
    STDMETHOD(SetRedTableValue)(THIS_ UINT index, IDCompositionAnimation *animation) PURE;
    STDMETHOD(SetGreenTableValue)(THIS_ UINT index, float value) PURE;
    STDMETHOD(SetGreenTableValue)(THIS_ UINT index, IDCompositionAnimation *animation) PURE;
    STDMETHOD(SetBlueTableValue)(THIS_ UINT index, float value) PURE;
    STDMETHOD(SetBlueTableValue)(THIS_ UINT index, IDCompositionAnimation *animation) PURE;
    STDMETHOD(SetAlphaTableValue)(THIS_ UINT index, float value) PURE;
    STDMETHOD(SetAlphaTableValue)(THIS_ UINT index, IDCompositionAnimation *animation) PURE;
#else
    STDMETHOD(SetRedTableValue)(THIS_ UINT index, IDCompositionAnimation *animation) PURE;
    STDMETHOD(SetRedTableValue)(THIS_ UINT index, float value) PURE;
    STDMETHOD(SetGreenTableValue)(THIS_ UINT index, IDCompositionAnimation *animation) PURE;
    STDMETHOD(SetGreenTableValue)(THIS_ UINT index, float value) PURE;
    STDMETHOD(SetBlueTableValue)(THIS_ UINT index, IDCompositionAnimation *animation) PURE;
    STDMETHOD(SetBlueTableValue)(THIS_ UINT index, float value) PURE;
    STDMETHOD(SetAlphaTableValue)(THIS_ UINT index, IDCompositionAnimation *animation) PURE;
    STDMETHOD(SetAlphaTableValue)(THIS_ UINT index, float value) PURE;
#endif
};
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(IDCompositionTableTransferEffect,0x9b7e82e2,0x69c5,0x4eb4,0xa5,0xf5,0xa7,0x03,0x3f,0x51,0x32,0xcd)
#endif

#undef INTERFACE
#define INTERFACE IDCompositionTexture
DECLARE_INTERFACE_IID_(IDCompositionTexture, IUnknown, "929BB1AA-725F-433B-ABD7-273075A835F2")
{
    STDMETHOD(SetSourceRect)(THIS_ const D2D_RECT_U &sourceRect) PURE;
    STDMETHOD(SetColorSpace)(THIS_ DXGI_COLOR_SPACE_TYPE colorSpace) PURE;
    STDMETHOD(SetAlphaMode)(THIS_ DXGI_ALPHA_MODE alphaMode) PURE;
    STDMETHOD(GetAvailableFence)(THIS_ UINT64 *fenceValue, REFIID iid, void **availableFence) PURE;
};
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(IDCompositionTexture,0x929bb1aa,0x725f,0x433b,0xab,0xd7,0x27,0x30,0x75,0xa8,0x35,0xf2)
#endif

#undef INTERFACE
#define INTERFACE IDCompositionDevice4
DECLARE_INTERFACE_IID_(IDCompositionDevice4, IDCompositionDevice3, "85FC5CCA-2DA6-494C-86B6-4A775C049B8A")
{
    STDMETHOD(CheckCompositionTextureSupport)(THIS_ IUnknown *renderingDevice, WINBOOL *supportsCompositionTextures) PURE;
    STDMETHOD(CreateCompositionTexture)(THIS_ IUnknown *d3dTexture, IDCompositionTexture **compositionTexture) PURE;
};
#ifdef __CRT_UUID_DECL
__CRT_UUID_DECL(IDCompositionDevice4,0x85fc5cca,0x2da6,0x494c,0x86,0xb6,0x4a,0x77,0x5c,0x04,0x9b,0x8a)
#endif
#endif /* _WIN32_WINNT >= 0x0603 */
'''

DEVICE3_MARKER = '#define INTERFACE IDCompositionDevice3'

REQUIRED_AFTER = (
    'IDCompositionDevice4',
    'IDCompositionTexture',
    'IDCompositionColorMatrixEffect',
    'IDCompositionTableTransferEffect',
)


def fail(msg):
    sys.stderr.write('ci_fix_mingw_dcomp: ERROR: %s\n' % msg)
    raise SystemExit(1)


def main(argv):
    if len(argv) != 2:
        fail('usage: ci_fix_mingw_dcomp.py <dcomp.h>')
    path = argv[1]

    with open(path, 'r', encoding='utf-8', errors='surrogateescape') as fh:
        src = fh.read()

    if 'IDCompositionDevice4' in src:
        print('ci_fix_mingw_dcomp: %s already declares IDCompositionDevice4; skipping.' % path)
        return 0

    # (a) Retype Device3's two void** effect-factory stubs. The TODO comment
    # between THIS_ and `void **` is absorbed by the non-greedy [^;]*?, so this
    # tolerates comment-text drift across mingw-w64 point releases.
    src, n1 = re.subn(
        r'(CreateColorMatrixEffect\)\(THIS_)[^;]*?void\s*\*\*\s*colorMatrixEffect\)',
        r'\1 IDCompositionColorMatrixEffect **colorMatrixEffect)', src)
    src, n2 = re.subn(
        r'(CreateTableTransferEffect\)\(THIS_)[^;]*?void\s*\*\*\s*tableTransferEffect\)',
        r'\1 IDCompositionTableTransferEffect **tableTransferEffect)', src)
    if n1 != 1 or n2 != 1:
        fail('expected 1 ColorMatrix + 1 TableTransfer Device3 void** stub, '
             'got %d + %d in %s (layout changed?)' % (n1, n2, path))

    # (b) Forward-declare the four interfaces immediately before Device3.
    count = src.count(DEVICE3_MARKER)
    if count != 1:
        fail('%d occurrences of Device3 INTERFACE define in %s' % (count, path))
    src = src.replace(DEVICE3_MARKER, FORWARD_DECLS + DEVICE3_MARKER, 1)

    # (c) Append the four full definitions before the include guard's last
    # closing #endif (the `#endif /* _DCOMP_H_ */` line).
    ends = list(re.finditer(r'(?m)^#endif\b.*_DCOMP_H_.*$', src))
    if not ends:
        fail('include-guard closing #endif (_DCOMP_H_) not found in %s' % path)
    pos = ends[-1].start()
    src = src[:pos] + INTERFACE_DEFS + '\n' + src[pos:]

    with open(path, 'w', encoding='utf-8', errors='surrogateescape') as fh:
        fh.write(src)

    # Verify the backfill actually took.
    missing = [name for name in REQUIRED_AFTER
               if ('#define INTERFACE %s' % name) not in src]
    if missing:
        fail('still missing after backfill in %s: %s' % (path, ', '.join(missing)))

    print('ci_fix_mingw_dcomp: backfilled + verified DComposition interfaces in %s' % path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
