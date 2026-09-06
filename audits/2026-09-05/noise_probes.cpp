#include <cstddef>
#include <algorithm>
#include <cstdio>
#include <vector>
#include "CanvasNoise.hpp"
#include "AudioNoise.hpp"

int main() {
  std::vector<unsigned char> pixels(64*64*4,127),original=pixels;
  camoufox::ApplyCanvasNoise(pixels.data(),64*4,64,64,111);
  int maximum=0;for(size_t i=0;i<pixels.size();++i)maximum=std::max(maximum,int(pixels[i])-int(original[i]));
  std::printf("canvas_max_positive_delta=%d (documented maximum: 1)\n",maximum);
  auto empty=original;
  camoufox::ApplyByteReadbackNoise(empty.data(),empty.size(),0,0,4,true,111);
  size_t changes=0;for(size_t i=0;i<empty.size();++i)changes+=empty[i]!=original[i];
  std::printf("webgl_zero_rectangle_changed_bytes=%zu (expected: 0)\n",changes);
  std::vector<float> full(1024,.25f),slice(128,.25f);
  camoufox::ApplyAudioNoise(full.data(),full.size(),111);
  camoufox::ApplyAudioNoise(slice.data(),slice.size(),111);
  size_t mismatches=0;for(size_t i=0;i<slice.size();++i)mismatches+=slice[i]!=full[256+i];
  std::printf("audio_partial_vs_full_slice_mismatches=%zu (expected: 0)\n",mismatches);
}
