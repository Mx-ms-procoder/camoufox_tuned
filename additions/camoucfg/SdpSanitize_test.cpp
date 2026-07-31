// Proves the WebRTC SDP sanitizer no longer corrupts the DTLS fingerprint.
//
// The shipped sanitizer ran the ipv4/ipv6 regexes over the whole SDP blob.
// `a=fingerprint:sha-256 6D:BD:1D:...` is colon separated hex and therefore
// matches the ipv6 alternation, so chunks of the fingerprint were replaced by
// the spoofed address. Firefox then rejected the offer it had just generated:
//
//   OperationError: SIPCC Failed to parse SDP:
//   SDP Parse Error on line 5: Malformed fingerprint token
//
// Measured on build015: with a WebRTC IP configured (geoip=True) every
// setLocalDescription() threw and zero ICE candidates were produced. Test 1
// reproduces that with the exact ipv6 pattern from the patch; the rest prove
// the whitelist fixes it without weakening the actual IP masking.
//
// Build: g++ -std=c++17 -I. SdpSanitize_test.cpp -o sdp_test && ./sdp_test

#include "SdpSanitize.hpp"

#include <cstdio>
#include <regex>
#include <string>
#include <vector>

namespace {

int gFailures = 0;

void Check(bool ok, const char* what) {
  std::printf("%-64s %s\n", what, ok ? "PASS" : "FAIL");
  if (!ok) ++gFailures;
}

// Verbatim from patches/network/webrtc-ip-spoofing.patch.
const char* kIPv6Pattern =
    "(?:(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}|(?:[0-9A-Fa-f]{1,4}:){1,7}:|(?"
    ":[0-9A-Fa-f]{1,4}:){1,6}:[0-9A-Fa-f]{1,4}|(?:[0-9A-Fa-f]{1,4}:){1,5}(?::[0"
    "-9A-Fa-f]{1,4}){1,2}|(?:[0-9A-Fa-f]{1,4}:){1,4}(?::[0-9A-Fa-f]{1,4}){1,3}|"
    "(?:[0-9A-Fa-f]{1,4}:){1,3}(?::[0-9A-Fa-f]{1,4}){1,4}|(?:[0-9A-Fa-f]{1,4}:)"
    "{1,2}(?::[0-9A-Fa-f]{1,4}){1,5}|[0-9A-Fa-f]{1,4}:(?::[0-9A-Fa-f]{1,4}){1,6"
    "}|:(?::[0-9A-Fa-f]{1,4}){1,7}|::)";
const char* kIPv4Pattern =
    "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}"
    "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)";

const char* kSpoofV4 = "203.0.113.7";
const char* kSpoofV6 = "2001:db8::7";

// A real Firefox 152 offer, captured from build015 (createOffer + one gathered
// srflx candidate pair appended, as SetLocalDescription sees it after trickle).
const std::string kOffer =
    "v=0\r\n"
    "o=mozilla...THIS_IS_SDPARTA-99.0 4225292358310650573 0 IN IP4 0.0.0.0\r\n"
    "s=-\r\n"
    "t=0 0\r\n"
    "a=fingerprint:sha-256 6D:BD:1D:A0:8C:2D:15:2B:4A:79:C5:46:EA:F0:B4:18:B0:"
    "87:76:13:EF:ED:EC:20:55:F1:25:B1:4B:B3:04:9C\r\n"
    "a=group:BUNDLE 0\r\n"
    "a=ice-options:trickle\r\n"
    "a=msid-semantic:WMS *\r\n"
    "m=application 9 UDP/DTLS/SCTP webrtc-datachannel\r\n"
    "c=IN IP4 87.177.35.252\r\n"
    "a=sendrecv\r\n"
    "a=ice-pwd:fc953e297c93183e4a1c7b14f5ff6d7b\r\n"
    "a=ice-ufrag:158d66ec\r\n"
    "a=mid:0\r\n"
    "a=rtcp:9 IN IP4 87.177.35.252\r\n"
    "a=setup:actpass\r\n"
    "a=sctp-port:5000\r\n"
    "a=max-message-size:1073741823\r\n"
    "a=candidate:3 1 UDP 1685987327 87.177.35.252 50852 typ srflx raddr "
    "0.0.0.0 rport 0\r\n"
    "a=candidate:1 1 UDP 1686052607 2003:d4:8f3f:304e:cdd8:eb8c:4f10:bb80 "
    "50851 typ srflx raddr :: rport 0\r\n";

// Stand-in for PeerConnectionImpl::SpoofCandidateIP: same two regexes, same
// order, same "leave special addresses alone" rule.
bool IsSpecialIP(const std::string& ip) {
  return ip == "0.0.0.0" || ip == "127.0.0.1" || ip == "::" || ip == "::1" ||
         ip.compare(0, 8, "169.254.") == 0 || ip.compare(0, 4, "fe80") == 0;
}

std::string ReplaceIPs(const std::string& in, const char* pattern,
                       const char* mask) {
  std::string out;
  std::regex re(pattern);
  auto begin = std::sregex_iterator(in.begin(), in.end(), re);
  size_t last = 0;
  for (auto it = begin; it != std::sregex_iterator(); ++it) {
    const std::string hit = it->str();
    out.append(in, last, static_cast<size_t>(it->position()) - last);
    out.append(IsSpecialIP(hit) ? hit : mask);
    last = static_cast<size_t>(it->position() + it->length());
  }
  out.append(in, last, std::string::npos);
  return out;
}

std::string SpoofLine(const std::string& line) {
  return ReplaceIPs(ReplaceIPs(line, kIPv4Pattern, kSpoofV4), kIPv6Pattern,
                    kSpoofV6);
}

std::string FindLine(const std::string& sdp, const std::string& prefix) {
  size_t pos = 0;
  while (pos < sdp.size()) {
    size_t end = sdp.find("\r\n", pos);
    if (end == std::string::npos) end = sdp.size();
    if (sdp.compare(pos, prefix.size(), prefix) == 0) {
      return sdp.substr(pos, end - pos);
    }
    pos = end + 2;
  }
  return "";
}

size_t CountLines(const std::string& sdp) {
  size_t n = 0;
  for (size_t i = 0; i + 1 < sdp.size(); ++i) {
    if (sdp[i] == '\r' && sdp[i + 1] == '\n') ++n;
  }
  return n;
}

}  // namespace

int main() {
  const std::string kFingerprint = FindLine(kOffer, "a=fingerprint:");

  // --- 1. the old whole-blob pass really did corrupt the fingerprint -----
  Check(ReplaceIPs(kFingerprint, kIPv6Pattern, kSpoofV6) != kFingerprint,
        "regression: whole-blob ipv6 regex rewrites a=fingerprint");

  // --- 2. the whitelist never hands that line to the replacer ------------
  std::vector<std::string> seen;
  const std::string out = camoufox::SanitizeSdp(
      kOffer, [&seen](const std::string& l) {
        seen.push_back(l);
        return SpoofLine(l);
      });
  bool touchedForbidden = false;
  for (const std::string& l : seen) {
    if (l.compare(0, 14, "a=fingerprint:") == 0 ||
        l.compare(0, 9, "a=ice-pwd") == 0 ||
        l.compare(0, 11, "a=ice-ufrag") == 0) {
      touchedForbidden = true;
    }
  }
  Check(!touchedForbidden, "crypto lines are never passed to the replacer");
  Check(FindLine(out, "a=fingerprint:") == kFingerprint,
        "a=fingerprint survives byte for byte");

  // --- 3. masking still happens where it must ----------------------------
  Check(out.find("87.177.35.252") == std::string::npos,
        "real IPv4 gone from every line");
  Check(out.find("2003:d4:8f3f") == std::string::npos,
        "real IPv6 gone from every line");
  Check(FindLine(out, "c=").find(kSpoofV4) != std::string::npos,
        "c= line carries the spoofed IPv4");
  Check(FindLine(out, "a=rtcp:").find(kSpoofV4) != std::string::npos,
        "a=rtcp: line carries the spoofed IPv4");
  Check(FindLine(out, "a=candidate:3").find(kSpoofV4) != std::string::npos,
        "IPv4 candidate carries the spoofed IPv4");
  Check(FindLine(out, "a=candidate:1").find(kSpoofV6) != std::string::npos,
        "IPv6 candidate carries the spoofed IPv6");

  // --- 4. structure is preserved -----------------------------------------
  Check(CountLines(out) == CountLines(kOffer), "no line added or dropped");
  Check(out.find("\n\n") == std::string::npos &&
            out.find("\r\r") == std::string::npos,
        "terminators stay canonical CRLF");
  Check(FindLine(out, "a=ice-pwd:") ==
            "a=ice-pwd:fc953e297c93183e4a1c7b14f5ff6d7b",
        "a=ice-pwd untouched");
  Check(FindLine(out, "a=max-message-size:") == "a=max-message-size:1073741823",
        "numeric attributes untouched");
  Check(FindLine(out, "o=").find("0.0.0.0") != std::string::npos,
        "o= keeps the unspecified address (special IPs not masked)");
  Check(FindLine(out, "a=candidate:3").find("raddr 0.0.0.0") !=
            std::string::npos,
        "raddr 0.0.0.0 left alone");

  // --- 5. bare-LF input still round-trips (no line collapsing) -----------
  std::string lf = kOffer;
  for (size_t p = lf.find("\r\n"); p != std::string::npos;
       p = lf.find("\r\n", p + 1)) {
    lf.erase(p, 1);
  }
  const std::string lfOut = camoufox::SanitizeSdp(lf, SpoofLine);
  Check(CountLines(lfOut) == CountLines(kOffer),
        "bare-LF input is normalised to CRLF, nothing merged");

  // --- 6. an empty / trailing-newline SDP does not crash -----------------
  Check(camoufox::SanitizeSdp(std::string(""), SpoofLine).empty(),
        "empty SDP stays empty");

  std::printf("\n%s (%d failure(s))\n", gFailures ? "FAILED" : "ALL PASS",
              gFailures);
  return gFailures ? 1 : 0;
}
