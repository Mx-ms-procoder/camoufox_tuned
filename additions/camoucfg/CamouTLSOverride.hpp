/*
  CamouTLSOverride — apply CAMOU_TLS_* environment variable overrides to NSS.

  This header is consumed from nsNSSComponent.cpp after NSS is initialized.
  It reads process-level env vars set by the Python orchestration layer
  (see pythonlib/camoufox/tls_profiles.py) and calls the public NSS/SSL
  APIs to *enable/disable* cipher suites, named groups, and signature
  algorithms.

  Honest contract (see K-1 in AUDIT_2026-05-18.md):

    • SSL_CipherPrefSetDefault enables/disables cipher suites globally;
      it does NOT control the order in which suites appear in the
      ClientHello. NSS keeps a hard-coded internal preference order
      (see Mozilla bug 1267894 and the introduction of the per-socket
      SSL_CipherSuiteOrderSet API in NSS 3.47). Earlier comments in this
      file claimed that the enable-call order set the ClientHello order
      — that was incorrect and has been removed.

    • Because the launcher derives a Firefox-version-correct profile,
      and because the NSS default order already matches the Firefox
      family, the cipher-suite *order* in the ClientHello is correct
      without any further intervention. What this override actually
      adds is the ability to *narrow* the enabled set to match a
      historical Firefox release that disabled some legacy suites.

    • Named groups and signature algorithms use the documented NSS
      ordering APIs (SSL_NamedGroupConfig, SSL_SignatureSchemePrefSet)
      and CAN be ordered globally. Those overrides remain.

    • Extension ordering is NOT overridden here because NSS does not
      expose a public API for it. Firefox's default extension order is
      already correct for the Firefox family.

  Env vars consumed:
    CAMOU_TLS_CIPHERS   – comma-separated hex cipher codes; the override
                           ENABLES only these and disables everything else.
                           NSS's internal preference order determines the
                           on-wire ClientHello cipher order.
    CAMOU_TLS_GROUPS    – comma-separated hex named group codes (ordered,
                           passed to SSL_NamedGroupConfig).
    CAMOU_TLS_SIGALGS   – comma-separated hex signature scheme codes
                           (ordered, passed to SSL_SignatureSchemePrefSet).
    CAMOU_TLS_ALPN      – comma-separated ALPN protocols. ALPN is per-socket
                           and Firefox already sets it via preferences; this
                           variable is informational only and is logged
                           rather than applied.
*/

#pragma once

#include <cstdint>
#include <cerrno>
#include <cstdlib>
#include <cstring>
#include <climits>
#include <optional>
#include <sstream>
#include <string>
#include <vector>

#include "mozilla/glue/Debug.h"
#include "EnvTruthy.hpp"

// NSS public headers
#include "ssl.h"
#include "sslproto.h"
#include "sslerr.h"

#ifdef _WIN32
#  include <windows.h>
#endif

namespace CamouTLSOverride {

// ── Debug gate ─────────────────────────────────────────────────────
//
// All TLS-override diagnostics are gated on CAMOU_TLS_DEBUG to avoid
// leaking the operational mode of the browser to stderr in production
// runs (see AUDIT_2026-05-18.md). When the flag is unset the overrides
// still run silently; only the gate decides whether to print.
//
// Truthy semantics ("1", "true", "yes", "on" — case-insensitive)
// shared with MaskConfig via CamouEnv::IsTruthyEnv. Previously this
// gate matched only literal "1", so CAMOU_TLS_DEBUG=true silently
// disabled logging — see audit T1.4.
inline bool DebugEnabled() {
  return CamouEnv::IsTruthyEnv("CAMOU_TLS_DEBUG");
}

#define CAMOU_TLS_LOG(...)                                  \
  do {                                                      \
    if (::CamouTLSOverride::DebugEnabled()) {               \
      printf_stderr(__VA_ARGS__);                           \
    }                                                       \
  } while (0)

// ── Env-var reader ──────────────────────────────────────────────────

inline std::optional<std::string> ReadEnv(const char* name) {
#ifdef _WIN32
  // Windows: read UTF-16, convert to UTF-8
  std::wstring wName(name, name + strlen(name));
  DWORD size = GetEnvironmentVariableW(wName.c_str(), nullptr, 0);
  if (size == 0) return std::nullopt;
  std::vector<wchar_t> buf(size);
  // Race-safe: env var could grow between the size probe and the read;
  // got >= size means truncated/unterminated and we must reject.
  DWORD got = GetEnvironmentVariableW(wName.c_str(), buf.data(), size);
  if (got == 0 || got >= size) return std::nullopt;
  // Simple ASCII conversion (env var values are hex/ASCII)
  std::string result;
  result.reserve(got);
  for (DWORD i = 0; i < got; ++i) {
    result.push_back(static_cast<char>(buf[i]));
  }
  return result;
#else
  const char* val = std::getenv(name);
  if (!val || val[0] == '\0') return std::nullopt;
  return std::string(val);
#endif
}

// ── Parser helpers ──────────────────────────────────────────────────

inline std::vector<uint16_t> ParseHexList(const std::string& csv) {
  std::vector<uint16_t> result;
  std::istringstream stream(csv);
  std::string token;
  while (std::getline(stream, token, ',')) {
    // Trim whitespace
    size_t start = token.find_first_not_of(" \t");
    size_t end = token.find_last_not_of(" \t");
    if (start == std::string::npos) continue;
    token = token.substr(start, end - start + 1);
    if (token.empty()) continue;

    // Parse hex (with or without 0x prefix). Firefox builds with C++
    // exceptions disabled, so avoid std::stoul here.
    errno = 0;
    char* parseEnd = nullptr;
    unsigned long val = std::strtoul(token.c_str(), &parseEnd, 16);
    if (errno == 0 && parseEnd != token.c_str() && *parseEnd == '\0' &&
        val <= 0xFFFFUL) {
      result.push_back(static_cast<uint16_t>(val));
    } else {
      CAMOU_TLS_LOG(
          "CamouTLSOverride: failed to parse hex value '%s'\n",
          token.c_str());
    }
  }
  return result;
}

inline std::vector<std::string> ParseCSV(const std::string& csv) {
  std::vector<std::string> result;
  std::istringstream stream(csv);
  std::string token;
  while (std::getline(stream, token, ',')) {
    size_t start = token.find_first_not_of(" \t");
    size_t end = token.find_last_not_of(" \t");
    if (start == std::string::npos) continue;
    token = token.substr(start, end - start + 1);
    if (!token.empty()) {
      result.push_back(token);
    }
  }
  return result;
}

// ── Cipher suite enable/disable ─────────────────────────────────────
//
// The full list of NSS cipher suite constants is defined in sslt.h.
// We first disable ALL cipher suites, then re-enable only the ones
// in the CAMOU_TLS_CIPHERS list.
//
// IMPORTANT: this controls the ENABLED SET, not the ClientHello order.
// SSL_CipherPrefSetDefault is documented as enable/disable only; NSS
// emits its hard-coded internal preference order on the wire (see
// Mozilla bug 1267894 and K-1 in AUDIT_2026-05-18.md). The previously
// claimed "enable-order becomes wire-order" behaviour is not true.
//
// That is fine in practice because the Python launcher hands us a
// Firefox-version-correct enabled set, and NSS's default order already
// matches the Firefox family. The override exists so a launcher
// targeting an older Firefox profile can disable later-added suites.

// List of all NSS cipher suite macro values that could be enabled.
// This is intentionally exhaustive so we don't miss any.
static const uint16_t kAllNSSCiphers[] = {
    // TLS 1.3
    TLS_AES_128_GCM_SHA256,           // 0x1301
    TLS_CHACHA20_POLY1305_SHA256,     // 0x1303
    TLS_AES_256_GCM_SHA384,           // 0x1302

    // ECDHE suites
    TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,     // 0xc02b
    TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,        // 0xc02f
    TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256, // 0xcca9
    TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,   // 0xcca8
    TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,     // 0xc02c
    TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,        // 0xc030
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,         // 0xc00a
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,         // 0xc009
    TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,           // 0xc013
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,           // 0xc014

    // RSA suites
    TLS_RSA_WITH_AES_128_GCM_SHA256,              // 0x009c
    TLS_RSA_WITH_AES_256_GCM_SHA384,              // 0x009d
    TLS_RSA_WITH_AES_128_CBC_SHA,                 // 0x002f
    TLS_RSA_WITH_AES_256_CBC_SHA,                 // 0x0035

    // DHE suites (Firefox includes these)
    TLS_DHE_RSA_WITH_AES_128_GCM_SHA256,          // 0x009e
    TLS_DHE_RSA_WITH_AES_256_GCM_SHA384,          // 0x009f
    TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256,    // 0xccaa
    TLS_DHE_RSA_WITH_AES_128_CBC_SHA,             // 0x0033
    TLS_DHE_RSA_WITH_AES_256_CBC_SHA,             // 0x0039

    // ECDHE with SHA256/SHA384 CBC (newer)
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,      // 0xc023
    TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256,         // 0xc027
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384,      // 0xc024

    // RSA CBC SHA256
    TLS_RSA_WITH_AES_128_CBC_SHA256,              // 0x003c
    TLS_RSA_WITH_AES_256_CBC_SHA256,              // 0x003d

    // 3DES (legacy)
    TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,          // 0xc012
    TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA,        // 0xc008
    TLS_RSA_WITH_3DES_EDE_CBC_SHA,                // 0x000a
};

inline void ApplyCipherOverride() {
  auto env = ReadEnv("CAMOU_TLS_CIPHERS");
  if (!env) return;

  auto ciphers = ParseHexList(*env);
  if (ciphers.empty()) return;

  CAMOU_TLS_LOG("CamouTLSOverride: applying %zu cipher suite overrides\n",
                ciphers.size());

  // Phase 1: Disable ALL known cipher suites
  for (uint16_t cipher : kAllNSSCiphers) {
    SSL_CipherPrefSetDefault(cipher, PR_FALSE);
  }

  // Phase 2: Enable only the requested ciphers.
  // The call order does NOT control ClientHello order — NSS uses its own
  // hard-coded internal preference ordering on the wire (see header comment).
  int enabled = 0;
  for (uint16_t cipher : ciphers) {
    SECStatus rv = SSL_CipherPrefSetDefault(cipher, PR_TRUE);
    if (rv == SECSuccess) {
      ++enabled;
    } else {
      CAMOU_TLS_LOG(
          "CamouTLSOverride: SSL_CipherPrefSetDefault(0x%04x) failed\n",
          cipher);
    }
  }

  CAMOU_TLS_LOG("CamouTLSOverride: enabled %d/%zu cipher suites\n",
                enabled, ciphers.size());
}

// ── Named group override ────────────────────────────────────────────
//
// SSL_NamedGroupConfig() sets the preference order for elliptic curves
// and finite-field groups used in key exchange. This directly affects
// the supported_groups TLS extension and the key_share extension.

inline void ApplyNamedGroupOverride() {
  auto env = ReadEnv("CAMOU_TLS_GROUPS");
  if (!env) return;

  auto groups = ParseHexList(*env);
  if (groups.empty()) return;

  CAMOU_TLS_LOG("CamouTLSOverride: applying %zu named group overrides\n",
                groups.size());

  // Convert uint16_t codes to SSLNamedGroup enum values.
  // NSS's SSLNamedGroup is typedef'd to uint16_t internally.
  std::vector<SSLNamedGroup> nssGroups;
  nssGroups.reserve(groups.size());
  for (uint16_t code : groups) {
    nssGroups.push_back(static_cast<SSLNamedGroup>(code));
  }

  SECStatus rv = SSL_NamedGroupConfig(
      nullptr,  // nullptr = set process-wide default
      nssGroups.data(),
      static_cast<unsigned int>(nssGroups.size()));

  if (rv != SECSuccess) {
    CAMOU_TLS_LOG("CamouTLSOverride: SSL_NamedGroupConfig() failed\n");
  }
}

// ── Signature algorithm override ────────────────────────────────────
//
// SSL_SignatureSchemePrefSet() sets the preference order for signature
// algorithms in the signature_algorithms TLS extension.

inline void ApplySignatureAlgorithmOverride() {
  auto env = ReadEnv("CAMOU_TLS_SIGALGS");
  if (!env) return;

  auto sigalgs = ParseHexList(*env);
  if (sigalgs.empty()) return;

  CAMOU_TLS_LOG(
      "CamouTLSOverride: applying %zu signature algorithm overrides\n",
      sigalgs.size());

  // Convert to SSLSignatureScheme
  std::vector<SSLSignatureScheme> schemes;
  schemes.reserve(sigalgs.size());
  for (uint16_t code : sigalgs) {
    schemes.push_back(static_cast<SSLSignatureScheme>(code));
  }

  SECStatus rv = SSL_SignatureSchemePrefSet(
      nullptr,  // nullptr = process-wide default
      schemes.data(),
      static_cast<unsigned int>(schemes.size()));

  if (rv != SECSuccess) {
    CAMOU_TLS_LOG(
        "CamouTLSOverride: SSL_SignatureSchemePrefSet() failed\n");
  }
}

// ── ALPN override ───────────────────────────────────────────────────
//
// ALPN is configured per-socket in NSS, not globally. However, Firefox's
// nsHttpHandler already sets ALPN via preferences. We store the desired
// ALPN list so it can be retrieved by nsHttpHandler patches if needed.
// For now, Firefox's default "h2,http/1.1" is correct.

inline void ApplyALPNOverride() {
  auto env = ReadEnv("CAMOU_TLS_ALPN");
  if (!env) return;

  auto protocols = ParseCSV(*env);
  if (protocols.empty()) return;

  // ALPN cannot be set globally via SSL_* APIs — it's per-socket.
  // We log it for debugging; actual enforcement happens in nsHttpHandler
  // which already reads the IdentityStateProvider ALPN config.
  if (DebugEnabled()) {
    printf_stderr("CamouTLSOverride: ALPN override requested: ");
    for (size_t i = 0; i < protocols.size(); ++i) {
      printf_stderr("%s%s", protocols[i].c_str(),
                    i + 1 < protocols.size() ? "," : "\n");
    }
  }
}

// ── Master apply function ───────────────────────────────────────────

inline void ApplyAll() {
  // Check if any CAMOU_TLS_* env vars are present
  bool hasCiphers = ReadEnv("CAMOU_TLS_CIPHERS").has_value();
  bool hasGroups = ReadEnv("CAMOU_TLS_GROUPS").has_value();
  bool hasSigAlgs = ReadEnv("CAMOU_TLS_SIGALGS").has_value();
  bool hasALPN = ReadEnv("CAMOU_TLS_ALPN").has_value();

  if (!hasCiphers && !hasGroups && !hasSigAlgs && !hasALPN) {
    // No overrides requested — use NSS defaults
    return;
  }

  CAMOU_TLS_LOG(
      "CamouTLSOverride: applying TLS fingerprint overrides "
      "(ciphers=%s groups=%s sigalgs=%s alpn=%s)\n",
      hasCiphers ? "yes" : "no",
      hasGroups ? "yes" : "no",
      hasSigAlgs ? "yes" : "no",
      hasALPN ? "yes" : "no");

  if (hasCiphers) ApplyCipherOverride();
  if (hasGroups) ApplyNamedGroupOverride();
  if (hasSigAlgs) ApplySignatureAlgorithmOverride();
  if (hasALPN) ApplyALPNOverride();
}

}  // namespace CamouTLSOverride
