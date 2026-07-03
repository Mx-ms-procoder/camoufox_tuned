/* Camoufox: content-aware 2D canvas noise.
 *
 * Firefox already randomises getImageData output via
 * nsRFPService::RandomizePixels, but ONLY on the
 * CanvasUtils::ImageExtraction::Randomize path, which is gated behind
 * privacy.resistFingerprinting. Camoufox deliberately ships RFP OFF (RFP
 * is itself a fingerprint), so that path never runs and getImageData /
 * toDataURL return the real, un-noised Firefox rendering — a hash that is
 * identical across every Camoufox instance on the same GPU. This applies a
 * deterministic, per-identity perturbation instead, keyed by the
 * canvas:noiseSeed value that pythonlib/camoufox/identity.py derives from
 * the fingerprint seed. (Before this, identity.py set canvas:noiseSeed and
 * IdentityStateProvider exposed it, but no render path ever consumed it.)
 *
 * The perturbation is CONTENT-AWARE: each pixel's delta is derived from a
 * hash of (seed, x, y, that pixel's own RGBA). A position-only or
 * seed+position defence can be undone by the Pixel-Recovery attack
 * ("Breaking the Shield: Analyzing and Attacking Canvas Fingerprinting
 * Defenses in the Wild", ACM Web Conference 2025), which paints a known
 * colour and reads back the fixed offset to solve for and subtract it.
 * Folding each pixel's own value into the hash removes that fixed
 * position->delta mapping, so a solid-colour probe no longer reveals the
 * transform used on arbitrary content.
 */
#ifndef CAMOUCFG_CANVAS_NOISE_HPP
#define CAMOUCFG_CANVAS_NOISE_HPP

#include <cstdint>

namespace camoufox {

// SplitMix64 finaliser — fast, good avalanche, stateless.
static inline uint64_t CanvasMix64(uint64_t h) {
  h += 0x9E3779B97F4A7C15ULL;
  h = (h ^ (h >> 30)) * 0xBF58476D1CE4E5B9ULL;
  h = (h ^ (h >> 27)) * 0x94D049BB133111EBULL;
  return h ^ (h >> 31);
}

// Perturb the mapped readback in place. The surface is A8R8G8B8_UINT32,
// i.e. B,G,R,A byte order in little-endian memory; `aStride` is the row
// stride in bytes. Alpha (byte index 3) is left untouched so opacity-based
// signals stay intact; only a sparse ~1/8 subset of pixels is nudged by
// +/-1 on R/G/B, which keeps the image visually identical while making the
// extracted hash unstable per identity. The whole transform is
// deterministic for a given (seed, content), so repeated getImageData calls
// within one identity are self-consistent — a detector cannot flag drift
// between two reads of the same canvas.
static inline void ApplyCanvasNoise(uint8_t* aData, int32_t aStride,
                                    int32_t aWidth, int32_t aHeight,
                                    uint64_t aSeed) {
  if (!aData || aSeed == 0 || aWidth <= 0 || aHeight <= 0 || aStride <= 0) {
    return;
  }
  for (int32_t y = 0; y < aHeight; ++y) {
    uint8_t* row = aData + static_cast<int64_t>(y) * aStride;
    for (int32_t x = 0; x < aWidth; ++x) {
      uint8_t* px = row + static_cast<int64_t>(x) * 4;
      uint64_t h = aSeed;
      h ^= (static_cast<uint64_t>(static_cast<uint32_t>(x)) << 32) ^
           static_cast<uint32_t>(y);
      h ^= static_cast<uint64_t>(px[0]) |
           (static_cast<uint64_t>(px[1]) << 8) |
           (static_cast<uint64_t>(px[2]) << 16) |
           (static_cast<uint64_t>(px[3]) << 24);
      h = CanvasMix64(h);
      // Nudge only ~1 pixel in 8.
      if ((h & 0x7ULL) != 0) {
        continue;
      }
      for (int c = 0; c < 3; ++c) {
        // delta in {-1, 0, 1, 0} from two bits of the hash.
        int delta = static_cast<int>((h >> (8 + c * 2)) & 0x3ULL) - 1;
        int v = static_cast<int>(px[c]) + delta;
        px[c] = static_cast<uint8_t>(v < 0 ? 0 : (v > 255 ? 255 : v));
      }
    }
  }
}

// Perturb an 8-bit-per-channel readback buffer, e.g. WebGL readPixels() with
// type UNSIGNED_BYTE. `aElementsPerPixel` bytes make up one pixel (4 for RGBA,
// 3 for RGB, 2 for luminance-alpha, 1 otherwise); when `aHasAlpha` the LAST
// channel is alpha and is left untouched so transparency stays exact. Same
// content-aware SplitMix64 scheme as ApplyCanvasNoise: this exists because
// Firefox's own nsRFPService::RandomizeElements for readPixels only runs under
// RFP, which Camoufox keeps OFF — so without this the real backend's pixels
// (e.g. llvmpipe in a container, while the spoofed renderer string claims a
// discrete GPU) leak straight through and can be compared against a reference.
//
// `aWidth`/`aHeight` describe the pixel rectangle. readPixels packs each row to
// GL_PACK_ALIGNMENT (WebGL default 4), so a row of aWidth pixels can be followed
// by padding bytes. We model that row stride so padding is skipped and the
// per-pixel hash stays aligned to real pixels across rows. RGBA (epp==4) rows
// are always 4-aligned, so that case has no padding and behaves exactly as a
// tightly packed buffer. If the row-major layout does not fit aSizeBytes
// (non-default packing, or an unexpected view size) we fall back to treating
// the whole buffer as one tightly packed span so every pixel is still nudged.
static inline void ApplyByteReadbackNoise(uint8_t* aData, size_t aSizeBytes,
                                          int32_t aWidth, int32_t aHeight,
                                          uint32_t aElementsPerPixel,
                                          bool aHasAlpha, uint64_t aSeed) {
  if (!aData || aSeed == 0 || aElementsPerPixel == 0 || aSizeBytes == 0) {
    return;
  }
  // Index of the alpha channel, or a value no channel matches when opaque.
  const uint32_t alphaIdx = aHasAlpha ? (aElementsPerPixel - 1) : aElementsPerPixel;

  const size_t rowBytes = static_cast<size_t>(aWidth) * aElementsPerPixel;
  size_t rowStride = rowBytes;
  if (rowStride % 4 != 0) {
    rowStride += 4 - (rowStride % 4);  // GL_PACK_ALIGNMENT default
  }
  size_t stride, perRowPixels, rows;
  if (aWidth > 0 && aHeight > 0 && rowStride > 0 &&
      rowStride * static_cast<size_t>(aHeight) <= aSizeBytes) {
    stride = rowStride;
    perRowPixels = static_cast<size_t>(aWidth);
    rows = static_cast<size_t>(aHeight);
  } else {
    stride = aSizeBytes;
    perRowPixels = aSizeBytes / aElementsPerPixel;
    rows = 1;
  }

  size_t pixelIndex = 0;
  for (size_t row = 0; row < rows; ++row) {
    uint8_t* rowPtr = aData + row * stride;
    for (size_t col = 0; col < perRowPixels; ++col, ++pixelIndex) {
      uint8_t* px = rowPtr + col * aElementsPerPixel;
      uint64_t h = aSeed ^ (static_cast<uint64_t>(pixelIndex) * 0x9E3779B97F4A7C15ULL);
      for (uint32_t c = 0; c < aElementsPerPixel; ++c) {
        h ^= static_cast<uint64_t>(px[c]) << ((c & 7) * 8);
      }
      h = CanvasMix64(h);
      if ((h & 0x7ULL) != 0) {
        continue;
      }
      for (uint32_t c = 0; c < aElementsPerPixel; ++c) {
        if (c == alphaIdx) {
          continue;
        }
        int delta = static_cast<int>((h >> (8 + (c & 7) * 2)) & 0x3ULL) - 1;
        int v = static_cast<int>(px[c]) + delta;
        px[c] = static_cast<uint8_t>(v < 0 ? 0 : (v > 255 ? 255 : v));
      }
    }
  }
}

}  // namespace camoufox

#endif  // CAMOUCFG_CANVAS_NOISE_HPP
