// Proves the claim the new canvas-noise hunk relies on: the toDataURL()
// encode path (packed BGRA, stride == width*4) and the getImageData()
// readback path (mapped surface, stride may be padded) produce byte-identical
// pixels for one identity. If that did not hold, wiring noise into both would
// have *created* the very inconsistency the patch exists to remove.
//
// Build: g++ -std=c++17 -I<additions/camoucfg> canvas_noise_test.cpp

#include "CanvasNoise.hpp"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

namespace {

int gFailures = 0;

void Check(bool ok, const char* what) {
  std::printf("%-62s %s\n", what, ok ? "PASS" : "FAIL");
  if (!ok) ++gFailures;
}

// Deterministic pseudo-canvas content: gradients + a solid block + a
// transparent region, so the content-aware hash sees varied input.
std::vector<uint8_t> MakePixels(int w, int h) {
  std::vector<uint8_t> px(static_cast<size_t>(w) * h * 4);
  for (int y = 0; y < h; ++y) {
    for (int x = 0; x < w; ++x) {
      uint8_t* p = px.data() + (static_cast<size_t>(y) * w + x) * 4;
      if (x < w / 3) {
        p[0] = 64; p[1] = 128; p[2] = 192; p[3] = 255;      // solid block
      } else if (x < 2 * w / 3) {
        p[0] = uint8_t(x * 3); p[1] = uint8_t(y * 5);
        p[2] = uint8_t((x + y) * 7); p[3] = 255;            // gradient
      } else {
        p[0] = 200; p[1] = 30; p[2] = 90; p[3] = uint8_t(x % 256);  // alpha ramp
      }
    }
  }
  return px;
}

// Copy tightly packed pixels into a buffer whose row stride is padded, the
// way a mapped DataSourceSurface can hand them over.
std::vector<uint8_t> ToStrided(const std::vector<uint8_t>& packed, int w, int h,
                               int stride) {
  std::vector<uint8_t> out(static_cast<size_t>(stride) * h, 0xAB);  // padding filler
  for (int y = 0; y < h; ++y) {
    std::memcpy(out.data() + static_cast<size_t>(y) * stride,
                packed.data() + static_cast<size_t>(y) * w * 4,
                static_cast<size_t>(w) * 4);
  }
  return out;
}

bool SamePixels(const std::vector<uint8_t>& packed,
                const std::vector<uint8_t>& strided, int w, int h, int stride) {
  for (int y = 0; y < h; ++y) {
    if (std::memcmp(packed.data() + static_cast<size_t>(y) * w * 4,
                    strided.data() + static_cast<size_t>(y) * stride,
                    static_cast<size_t>(w) * 4) != 0) {
      return false;
    }
  }
  return true;
}

size_t CountChanged(const std::vector<uint8_t>& a, const std::vector<uint8_t>& b) {
  size_t n = 0;
  for (size_t i = 0; i + 3 < a.size() && i + 3 < b.size(); i += 4) {
    if (a[i] != b[i] || a[i + 1] != b[i + 1] || a[i + 2] != b[i + 2]) ++n;
  }
  return n;
}

}  // namespace

int main() {
  const int w = 137, h = 61;  // deliberately not a multiple of 4
  const uint64_t seed = 8416578342316258288ULL;  // a real canvas:noiseSeed
  const int packedStride = w * 4;
  const int paddedStride = packedStride + 48;

  const std::vector<uint8_t> original = MakePixels(w, h);

  // --- 1. encode path (toDataURL): packed, stride == width*4 -------------
  std::vector<uint8_t> encodePath = original;
  camoufox::ApplyCanvasNoise(encodePath.data(), packedStride, w, h, seed);

  // --- 2. readback path (getImageData): mapped surface, padded stride ----
  std::vector<uint8_t> readbackPath = ToStrided(original, w, h, paddedStride);
  camoufox::ApplyCanvasNoise(readbackPath.data(), paddedStride, w, h, seed);

  Check(SamePixels(encodePath, readbackPath, w, h, paddedStride),
        "toDataURL and getImageData agree despite different strides");

  // --- 3. determinism: same input + same seed -> same output -------------
  std::vector<uint8_t> again = original;
  camoufox::ApplyCanvasNoise(again.data(), packedStride, w, h, seed);
  Check(again == encodePath, "same seed + same content is reproducible");

  // --- 4. the noise actually happens ------------------------------------
  const size_t changed = CountChanged(original, encodePath);
  const size_t total = static_cast<size_t>(w) * h;
  Check(changed > 0, "noise is applied at all (not a dead path)");
  // ~1 pixel in 8 is selected; of those a delta of 0 on all three channels is
  // possible, so the observed rate sits just under 1/8.
  Check(changed * 100 / total >= 6 && changed * 100 / total <= 16,
        "perturbation rate is the intended ~1/8 of pixels");

  // --- 5. per-identity separation ---------------------------------------
  std::vector<uint8_t> otherSeed = original;
  camoufox::ApplyCanvasNoise(otherSeed.data(), packedStride, w, h, seed ^ 0x1234);
  Check(otherSeed != encodePath, "a different seed yields a different canvas");

  // --- 6. alpha is never touched ----------------------------------------
  bool alphaIntact = true;
  for (size_t i = 3; i < original.size(); i += 4) {
    if (original[i] != encodePath[i]) { alphaIntact = false; break; }
  }
  Check(alphaIntact, "alpha channel left exact");

  // --- 7. no write past the declared rectangle ---------------------------
  bool paddingIntact = true;
  for (int y = 0; y < h; ++y) {
    for (int b = packedStride; b < paddedStride; ++b) {
      if (readbackPath[static_cast<size_t>(y) * paddedStride + b] != 0xAB) {
        paddingIntact = false; break;
      }
    }
  }
  Check(paddingIntact, "row padding untouched (no out-of-rect writes)");

  // --- 8. disabled when unconfigured ------------------------------------
  std::vector<uint8_t> zeroSeed = original;
  camoufox::ApplyCanvasNoise(zeroSeed.data(), packedStride, w, h, 0);
  Check(zeroSeed == original, "seed 0 is a no-op (feature off)");

  std::printf("\n%s (%d failure(s))\n", gFailures ? "FAILED" : "ALL PASS", gFailures);
  return gFailures ? 1 : 0;
}
