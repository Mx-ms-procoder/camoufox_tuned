/*
  EnvTruthy — shared helper for parsing CAMOU_* boolean environment
  variables.

  Both MaskConfig (CAMOU_MASKCFG_DEBUG, MOZ_CAMOUFOX_ALLOW_RUNTIME_SETTERS)
  and CamouTLSOverride (CAMOU_TLS_DEBUG) consume CAMOU_* flags. Before
  this header existed each had its own gate implementation with subtly
  different semantics: CamouTLSOverride::DebugEnabled() matched only
  literal "1" while MaskConfig::_IsTruthyEnv() accepted any of
  "1"/"true"/"yes"/"on" (case-insensitive). Operators who set
  CAMOU_TLS_DEBUG=true got no logging despite a documented-truthy
  value (see audit T1.4). This header is now the single source of
  truth — both call sites delegate here.
*/

#pragma once

#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

#ifdef _WIN32
#  include <windows.h>
#endif

namespace CamouEnv {

// Returns true iff the environment variable is set to a truthy value.
// Truthy: "1", "true", "yes", "on" (case-insensitive). Anything else
// (including "0", "false", empty string, unset) is falsy.
inline bool IsTruthyEnv(const char* name) {
  std::string value;
#ifdef _WIN32
  std::wstring wname(name, name + std::char_traits<char>::length(name));
  DWORD size = GetEnvironmentVariableW(wname.c_str(), nullptr, 0);
  if (size == 0) return false;
  std::vector<wchar_t> wbuf(size);
  // Race-safe: env var may grow between size probe and read; if got
  // >= size the buffer is truncated (not NUL-terminated) and we must
  // reject rather than read past it via WideCharToMultiByte.
  DWORD wgot = GetEnvironmentVariableW(wname.c_str(), wbuf.data(), size);
  if (wgot == 0 || wgot >= size) return false;
  int utf8Size = WideCharToMultiByte(CP_UTF8, 0, wbuf.data(), -1,
                                     nullptr, 0, nullptr, nullptr);
  if (utf8Size <= 1) return false;
  value.resize(static_cast<size_t>(utf8Size - 1), '\0');
  WideCharToMultiByte(CP_UTF8, 0, wbuf.data(), -1, value.data(), utf8Size,
                      nullptr, nullptr);
#else
  const char* raw = std::getenv(name);
  if (!raw || !*raw) return false;
  value = raw;
#endif
  std::transform(value.begin(), value.end(), value.begin(),
                 [](unsigned char c) { return std::tolower(c); });
  return value == "1" || value == "true" || value == "yes" || value == "on";
}

}  // namespace CamouEnv
