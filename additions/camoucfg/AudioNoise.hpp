#ifndef CAMOUFOX_AUDIO_NOISE_HPP
#define CAMOUFOX_AUDIO_NOISE_HPP

#include <algorithm>
#include <cstdint>
#include <cstring>

/**
 * Per-identity AudioContext noise, driven by the `audio:seed` value
 * pythonlib/camoufox/identity.py derives from the fingerprint seed.
 *
 * The seed plumbing is the whole point: the transformation itself was already
 * here, but AudioFingerprintManager::GetSeed() only ever found 0 (the runtime
 * setter that fed its storage key was removed with the window.set* island, and
 * the launcher never wrote the config key), so ApplyTransformation() returned
 * immediately. Measured across three identities the OfflineAudioContext
 * fingerprint was byte-identical — an Apple M1 profile and an NVIDIA Windows
 * profile produced the same audio hash, which both links profiles and
 * contradicts the hardware each one claims.
 *
 * Kept header-only and Gecko-free so AudioNoise_test.cpp can exercise the
 * exact code the browser runs.
 */
namespace camoufox {

// Float samples (AudioBuffer channel data).
//
// Content-aware: each sample's own bits are folded into the PRNG state, so the
// multiplier depends on the value, not just (seed, index). A position-only
// sequence can be recovered from a known reference signal and divided back out
// (cf. Pixel-Recovery, ACM WWW'25); mixing the sample in defeats that
// inversion. Variance is 0.8% (range [0.996, 1.004]) plus a non-linear
// polynomial term — deliberately wider than Brave's 0.1-0.2%, which was
// shown to be averaged out across repeated reads.
inline void ApplyAudioNoise(float* data, uint32_t length, uint32_t seed) {
  if (seed == 0 || length == 0 || !data) {
    return;
  }
  uint32_t state = seed;
  for (uint32_t i = 0; i < length; ++i) {
    uint32_t sampleBits;
    std::memcpy(&sampleBits, &data[i], sizeof(sampleBits));
    state ^= sampleBits;
    state = (state * 1664525u + 1013904223u);
    float normalized = static_cast<float>(state) / 4294967295.0f;
    float base = 0.996f + normalized * 0.008f;
    float adjustment = (normalized * normalized - 0.5f) * 0.002f;
    float multiplier = base + adjustment;
    data[i] *= multiplier;
  }
}

// Byte samples: ±1 adjustment, content-aware for the same reason.
inline void ApplyAudioNoiseBytes(uint8_t* data, uint32_t length, uint32_t seed) {
  if (seed == 0 || length == 0 || !data) {
    return;
  }
  uint32_t state = seed;
  for (uint32_t i = 0; i < length; ++i) {
    state ^= static_cast<uint32_t>(data[i]);
    state = (state * 1664525u + 1013904223u);
    int32_t adjustment = static_cast<int32_t>(state % 3) - 1;
    int32_t newValue = static_cast<int32_t>(data[i]) + adjustment;
    data[i] = static_cast<uint8_t>(std::max(0, std::min(255, newValue)));
  }
}

}  // namespace camoufox

#endif  // CAMOUFOX_AUDIO_NOISE_HPP
