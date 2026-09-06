#include "CanvasNoise.hpp"
#include <algorithm>
#include <cstdio>
#include <vector>

int main() {
  int failures = 0;
  auto check = [&](bool ok, const char* name) {
    std::printf("%s: %s\n", name, ok ? "PASS" : "FAIL");
    failures += !ok;
  };
  constexpr int width = 37, height = 19, channels = 4;
  constexpr size_t stride = width * channels + 28, offset = 17;
  constexpr uint64_t seed = 222;
  std::vector<uint8_t> packed(width * height * channels);
  for (size_t i = 0; i < packed.size(); ++i) packed[i] = uint8_t(i * 17 + 29);
  auto original = packed;
  std::vector<uint8_t> strided(offset + stride * height + 21, 0xab);
  for (int y = 0; y < height; ++y)
    std::copy_n(packed.data() + y * width * channels, width * channels,
                strided.data() + offset + y * stride);
  auto paddedOriginal = strided;
  camoufox::ApplyByteReadbackNoise(packed.data(), packed.size(), width, height,
                                  channels, true, seed, width * channels, 0, 7, 11);
  camoufox::ApplyByteReadbackNoise(strided.data(), strided.size(), width, height,
                                  channels, true, seed, stride, offset, 7, 11);
  bool same = true, padding = true, alpha = true;
  for (size_t i = 0; i < strided.size(); ++i) {
    const bool inRect = i >= offset && (i - offset) / stride < height &&
                        (i - offset) % stride < width * channels;
    if (!inRect && strided[i] != paddedOriginal[i]) padding = false;
  }
  for (int y = 0; y < height; ++y) {
    for (int x = 0; x < width * channels; ++x) {
      const size_t p = y * width * channels + x;
      same &= packed[p] == strided[offset + y * stride + x];
      if (x % channels == 3) alpha &= packed[p] == original[p];
    }
  }
  check(same, "Direct/PBO layout parity with skips and row padding");
  check(padding, "Prefix, row padding, and oversized suffix remain untouched");
  check(alpha, "Alpha remains exact");
  check(packed != original, "Noise is active");

  // Cropped reads use framebuffer coordinates, not a restarting array index.
  std::vector<uint8_t> crop(9 * 4 * channels);
  for (int y = 0; y < 4; ++y)
    std::copy_n(original.data() + ((y + 3) * width + 5) * channels, 9 * channels,
                crop.data() + y * 9 * channels);
  camoufox::ApplyByteReadbackNoise(crop.data(), crop.size(), 9, 4, channels,
                                  true, seed, 9 * channels, 0, 12, 14);
  bool cropMatches = true;
  for (int y = 0; y < 4; ++y)
    cropMatches &= std::equal(crop.data() + y * 9 * channels,
                             crop.data() + (y + 1) * 9 * channels,
                             packed.data() + ((y + 3) * width + 5) * channels);
  check(cropMatches, "Cropped reads match the corresponding full read");
  auto invalid = paddedOriginal;
  camoufox::ApplyByteReadbackNoise(invalid.data(), 7, width, height, channels,
                                  true, seed);
  camoufox::ApplyByteReadbackNoise(invalid.data(), invalid.size(), -1, height,
                                  channels, true, seed);
  camoufox::ApplyByteReadbackNoise(invalid.data(), invalid.size(), width, height,
                                  channels, true, seed, SIZE_MAX, offset);
  check(invalid == paddedOriginal, "Invalid/overflowing layouts never write");

  // A three-byte last row needs no trailing alignment padding.
  std::vector<uint8_t> rgb(7, 127);
  auto rgbBefore = rgb;
  camoufox::ApplyByteReadbackNoise(rgb.data(), rgb.size(), 1, 2, 3, false, seed);
  check(rgb[3] == rgbBefore[3], "RGB last row without trailing padding is accepted safely");
  return failures ? 1 : 0;
}
