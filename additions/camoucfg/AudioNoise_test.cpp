// Proves the audio noise actually moves the fingerprint that sites measure,
// and only when a seed is configured.
//
// The regression this guards: `audio:seed` was never written by the launcher,
// so GetSeed() returned 0 and ApplyTransformation() early-returned. Measured
// on build015 across identities 1111/2222/3333, the OfflineAudioContext
// fingerprint was byte-identical (sum over samples 4500..5000 =
// 35.749972093850374 every time) even though the profiles claimed an NVIDIA
// Windows box, an Intel machine and an Apple M1. Test 1 reproduces that
// (seed 0 -> untouched); the rest prove a configured seed separates identities
// without destroying the signal.
//
// Build: g++ -std=c++17 -I. AudioNoise_test.cpp -o audio_test && ./audio_test

#include "AudioNoise.hpp"

#include <cmath>
#include <cstdio>
#include <vector>

namespace {

int gFailures = 0;

void Check(bool ok, const char* what) {
  std::printf("%-64s %s\n", what, ok ? "PASS" : "FAIL");
  if (!ok) ++gFailures;
}

// The signal the classic AudioContext fingerprint uses: a 10 kHz triangle
// oscillator through a DynamicsCompressor. A plain triangle is close enough
// to exercise the same code path.
std::vector<float> MakeSignal(uint32_t n) {
  std::vector<float> v(n);
  for (uint32_t i = 0; i < n; ++i) {
    const double t = static_cast<double>(i) / 44100.0;
    const double phase = std::fmod(t * 10000.0, 1.0);
    v[i] = static_cast<float>(2.0 * std::fabs(2.0 * phase - 1.0) - 1.0);
  }
  return v;
}

// What fingerprinters actually hash: the sum of |sample| over a fixed window.
double FingerprintSum(const std::vector<float>& v) {
  double s = 0.0;
  for (uint32_t i = 4500; i < 5000 && i < v.size(); ++i) s += std::fabs(v[i]);
  return s;
}

double MaxRelativeDelta(const std::vector<float>& a, const std::vector<float>& b) {
  double worst = 0.0;
  for (size_t i = 0; i < a.size(); ++i) {
    if (a[i] == 0.0f) continue;
    const double rel = std::fabs(static_cast<double>(b[i] - a[i]) / a[i]);
    worst = std::max(worst, rel);
  }
  return worst;
}

}  // namespace

int main() {
  const uint32_t kLen = 44100;
  const std::vector<float> original = MakeSignal(kLen);
  const double baseSum = FingerprintSum(original);

  // --- 1. regression: no seed means no noise at all --------------------
  std::vector<float> unseeded = original;
  camoufox::ApplyAudioNoise(unseeded.data(), kLen, 0);
  Check(unseeded == original, "seed 0 leaves the signal untouched (the bug)");

  // --- 2. a configured seed moves the fingerprint ----------------------
  std::vector<float> a = original;
  camoufox::ApplyAudioNoise(a.data(), kLen, 658742122u);  // real audio:seed
  const double sumA = FingerprintSum(a);
  Check(sumA != baseSum, "a configured seed changes the fingerprint sum");

  // --- 3. different identities separate --------------------------------
  std::vector<float> b = original;
  camoufox::ApplyAudioNoise(b.data(), kLen, 3555370239u);
  const double sumB = FingerprintSum(b);
  Check(sumA != sumB, "two identities produce different fingerprints");
  Check(a != b, "sample data differs between identities");

  // --- 4. one identity is reproducible ---------------------------------
  std::vector<float> again = original;
  camoufox::ApplyAudioNoise(again.data(), kLen, 658742122u);
  Check(again == a, "same seed is reproducible across runs");

  // --- 5. the perturbation stays inaudible / plausible -----------------
  const double worst = MaxRelativeDelta(original, a);
  Check(worst > 0.0 && worst <= 0.011,
        "per-sample deviation stays within the intended ~0.8-1.0%");
  Check(std::fabs(sumA - baseSum) / baseSum < 0.02,
        "aggregate signal is preserved (no audible distortion)");

  // --- 6. content-aware: identical samples do not get identical factors -
  std::vector<float> flat(2048, 0.25f);
  std::vector<float> flatNoised = flat;
  camoufox::ApplyAudioNoise(flatNoised.data(), 2048, 658742122u);
  bool allSame = true;
  for (size_t i = 1; i < flatNoised.size(); ++i) {
    if (flatNoised[i] != flatNoised[0]) { allSame = false; break; }
  }
  Check(!allSame, "a constant input is not scaled by a constant factor");

  // --- 7. byte path -----------------------------------------------------
  std::vector<uint8_t> bytes(512), bytesCopy;
  for (size_t i = 0; i < bytes.size(); ++i) bytes[i] = static_cast<uint8_t>(i % 256);
  bytesCopy = bytes;
  camoufox::ApplyAudioNoiseBytes(bytesCopy.data(), 512, 0);
  Check(bytesCopy == bytes, "byte path: seed 0 is a no-op");
  camoufox::ApplyAudioNoiseBytes(bytesCopy.data(), 512, 658742122u);
  Check(bytesCopy != bytes, "byte path: a seed perturbs the data");
  bool clamped = true;
  for (size_t i = 0; i < bytes.size(); ++i) {
    const int d = static_cast<int>(bytesCopy[i]) - static_cast<int>(bytes[i]);
    if (d < -1 || d > 1) { clamped = false; break; }
  }
  Check(clamped, "byte path: adjustment stays within +/-1");

  // --- 8. no read/write past the buffer --------------------------------
  std::vector<float> guarded(64 + 8, 7.0f);
  camoufox::ApplyAudioNoise(guarded.data(), 64, 658742122u);
  bool tailIntact = true;
  for (size_t i = 64; i < guarded.size(); ++i) {
    if (guarded[i] != 7.0f) { tailIntact = false; break; }
  }
  Check(tailIntact, "writes stay inside the declared length");

  for (const uint32_t offset : {0u, 1u, 256u, 4000u}) {
    std::vector<float> slice(original.begin() + offset, original.begin() + offset + 128);
    camoufox::ApplyAudioNoise(slice.data(), slice.size(), 658742122u, offset);
    Check(std::equal(slice.begin(), slice.end(), a.begin() + offset),
          "partial read equals whole-channel slice at its absolute offset");
  }

  std::printf("\n%s (%d failure(s))\n", gFailures ? "FAILED" : "ALL PASS",
              gFailures);
  return gFailures ? 1 : 0;
}
