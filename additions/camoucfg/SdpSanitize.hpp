#ifndef CAMOUFOX_SDP_SANITIZE_HPP
#define CAMOUFOX_SDP_SANITIZE_HPP

#include <sstream>
#include <string>

namespace camoufox {

// The only SDP lines that can carry an IP literal (RFC 4566 / RFC 8839):
//   o=            origin, ends in "IN IP4|IP6 <addr>"
//   c=            connection data
//   a=candidate:  ICE candidate: connection address plus optional raddr
//   a=rtcp:       optional "IN IP4|IP6 <addr>" tail
// Every other line has to survive byte for byte.
//
// This whitelist is the entire point of the file. Running the IP regexes over
// the whole SDP blob rewrote `a=fingerprint:sha-256 6D:BD:1D:A0:...` — colon
// separated hex parses as an IPv6 literal — so Firefox could no longer parse
// the offer it had just generated ("SDP Parse Error: Malformed fingerprint
// token"). That killed WebRTC outright whenever a spoof IP was configured
// (i.e. under geoip) and handed detectors a one-line Camoufox check, since no
// real Firefox fails on its own offer. See SdpSanitize_test.cpp.
inline bool SdpLineCanCarryIP(const std::string& line) {
  return line.compare(0, 2, "o=") == 0 || line.compare(0, 2, "c=") == 0 ||
         line.compare(0, 12, "a=candidate:") == 0 ||
         line.compare(0, 7, "a=rtcp:") == 0;
}

// Rewrite only the IP-bearing lines through `replace`, re-emitting the SDP
// with canonical CRLF terminators (RFC 4566).
template <typename ReplaceFn>
inline std::string SanitizeSdp(const std::string& sdp, ReplaceFn replace) {
  std::istringstream iss(sdp);
  std::ostringstream oss;
  std::string line;

  while (std::getline(iss, line)) {
    // std::getline leaves the '\r' of a CRLF pair behind; strip it and re-emit
    // one canonical terminator below.
    if (!line.empty() && line.back() == '\r') {
      line.pop_back();
    }
    if (SdpLineCanCarryIP(line)) {
      line = replace(line);
    }
    oss << line << "\r\n";
  }
  return oss.str();
}

}  // namespace camoufox

#endif  // CAMOUFOX_SDP_SANITIZE_HPP
