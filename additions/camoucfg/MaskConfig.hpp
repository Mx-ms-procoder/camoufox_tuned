/*
Helper to extract values from the CAMOU_CONFIG environment variable(s).
Written by daijro.
*/

#pragma once
#include "json.hpp"
#include "EnvTruthy.hpp"
#include <memory>
#include <string>
#include <tuple>
#include <optional>
#include "mozilla/glue/Debug.h"
#include <cstdlib>
#include <cstdio>
#include <mutex>
#include <thread>
#include <chrono>
#include <variant>
#include <cstddef>
#include <vector>
#include <algorithm>
#include <cctype>
#include <array>
#include <limits>
#include <type_traits>

#ifdef _WIN32
#  include <windows.h>
#endif

namespace MaskConfig {

template <typename T>
struct IsStdArray : std::false_type {};

template <typename T, size_t N>
struct IsStdArray<std::array<T, N>> : std::true_type {};

template <typename T>
struct StdArrayTraits {};

template <typename T, size_t N>
struct StdArrayTraits<std::array<T, N>> {
  using ValueType = T;
  static constexpr size_t Size = N;
};

template <typename T>
inline bool JsonScalarMatches(const nlohmann::json& value) {
  if constexpr (std::is_same_v<T, bool>) {
    return value.is_boolean();
  } else if constexpr (std::is_same_v<T, std::string>) {
    return value.is_string();
  } else if constexpr (std::is_floating_point_v<T>) {
    return value.is_number();
  } else if constexpr (std::is_integral_v<T> && std::is_unsigned_v<T>) {
    return value.is_number_unsigned();
  } else if constexpr (std::is_integral_v<T> && std::is_signed_v<T>) {
    return value.is_number_integer();
  } else {
    return true;
  }
}

template <typename T>
inline bool JsonValueMatches(const nlohmann::json& value) {
  if constexpr (IsStdArray<T>::value) {
    if (!value.is_array() || value.size() != StdArrayTraits<T>::Size) {
      return false;
    }
    for (const auto& item : value) {
      if (!JsonScalarMatches<typename StdArrayTraits<T>::ValueType>(item)) {
        return false;
      }
    }
    return true;
  } else {
    return JsonScalarMatches<T>(value);
  }
}

// ── Debug gate ─────────────────────────────────────────────────────
//
// All non-fatal parse-error prints below are gated on
// CAMOU_MASKCFG_DEBUG=1. Without the gate, an upstream identity blob
// with one wrong type leaked the parse error to stderr, which on a
// release Firefox build goes to the crash reporter — observable from
// outside the process. Fatal errors (corrupt JSON, no config at all)
// still print because they signal a launcher misconfiguration the
// operator must see. See K-10 in AUDIT_2026-05-18.md.
// Returns true iff the environment variable is set to a truthy value.
// Truthy: "1", "true", "yes", "on" (case-insensitive). Anything else
// (including "0", "false", empty, unset) is falsy.
//
// Kept under MaskConfig:: because several Firefox-source patches call
// it as ::MaskConfig::_IsTruthyEnv(...). Implementation lives in
// EnvTruthy.hpp so CamouTLSOverride uses the same semantics — before
// consolidation, CAMOU_TLS_DEBUG=true silently disabled debug there
// because that gate matched only literal "1".
inline bool _IsTruthyEnv(const char* name) {
  return CamouEnv::IsTruthyEnv(name);
}

inline bool DebugEnabled() {
  return CamouEnv::IsTruthyEnv("CAMOU_MASKCFG_DEBUG");
}

#define CAMOU_MASKCFG_LOG(...)               \
  do {                                       \
    if (::MaskConfig::DebugEnabled()) {      \
      printf_stderr(__VA_ARGS__);            \
    }                                        \
  } while (0)

// Reads a file at the given UTF-8 path and returns its contents as a
// UTF-8 string. Used by GetJson() to optionally accept the identity
// blob via a private file instead of chunked env vars (see K-18 /
// S-B in AUDIT_2026-05-18.md).
inline std::optional<std::string> read_file_utf8(const std::string& path) {
  if (path.empty()) return std::nullopt;
#ifdef _WIN32
  // The path may contain non-ASCII characters; convert UTF-8 → UTF-16
  // before opening so paths on localised Windows installs still work.
  int wlen = MultiByteToWideChar(CP_UTF8, 0, path.c_str(), -1, nullptr, 0);
  if (wlen <= 0) return std::nullopt;
  std::vector<wchar_t> wpath(static_cast<size_t>(wlen));
  MultiByteToWideChar(CP_UTF8, 0, path.c_str(), -1, wpath.data(), wlen);
  FILE* f = nullptr;
  if (_wfopen_s(&f, wpath.data(), L"rb") != 0 || !f) return std::nullopt;
#else
  FILE* f = std::fopen(path.c_str(), "rb");
  if (!f) return std::nullopt;
#endif
  if (std::fseek(f, 0, SEEK_END) != 0) { std::fclose(f); return std::nullopt; }
  long size = std::ftell(f);
  if (size < 0) { std::fclose(f); return std::nullopt; }
  if (std::fseek(f, 0, SEEK_SET) != 0) { std::fclose(f); return std::nullopt; }
  std::string contents(static_cast<size_t>(size), '\0');
  size_t got = (size == 0) ? 0
      : std::fread(contents.data(), 1, static_cast<size_t>(size), f);
  std::fclose(f);
  if (got != static_cast<size_t>(size)) return std::nullopt;
  return contents;
}

// Function to get the value of an environment variable as a UTF-8 string.
inline std::optional<std::string> get_env_utf8(const std::string& name) {
#ifdef _WIN32
  std::wstring wName(name.begin(), name.end());
  DWORD size = GetEnvironmentVariableW(wName.c_str(), nullptr, 0);
  if (size == 0) return std::nullopt;  // Environment variable not found

  std::vector<wchar_t> buffer(size);
  // Race-safe: if the env var grew between calls, `got` will equal `size`
  // (truncated, not NUL-terminated) and we must abort instead of reading
  // uninitialised tail bytes via wValue() ctor.
  DWORD got = GetEnvironmentVariableW(wName.c_str(), buffer.data(), size);
  if (got == 0 || got >= size) return std::nullopt;
  std::wstring wValue(buffer.data());

  // Convert UTF-16 to UTF-8 using Win32 (std::wstring_convert removed in C++26)
  int utf8Size = WideCharToMultiByte(CP_UTF8, 0, wValue.c_str(), -1,
                                     nullptr, 0, nullptr, nullptr);
  if (utf8Size <= 0) return std::nullopt;
  // Allocate the full utf8Size so WideCharToMultiByte can safely write
  // the NUL terminator; then shrink to exclude it.
  std::string result(static_cast<size_t>(utf8Size), '\0');
  int written = WideCharToMultiByte(CP_UTF8, 0, wValue.c_str(), -1,
                                    result.data(), utf8Size, nullptr, nullptr);
  if (written <= 0) return std::nullopt;
  result.resize(static_cast<size_t>(written - 1));
  return result;
#else
  const char* value = std::getenv(name.c_str());
  if (!value) return std::nullopt;
  return std::string(value);
#endif
}

inline const nlohmann::json& GetJson() {
  static std::once_flag initFlag;
  static nlohmann::json jsonConfig;

  std::call_once(initFlag, []() {
    std::string jsonString;

    // K-18 / S-B (AUDIT_2026-05-18.md): prefer the file-based transport
    // when CAMOU_CONFIG_FILE is set. The launcher writes the identity
    // JSON to a 0600 temp file and points us at the path, instead of
    // chunking the blob into CAMOU_CONFIG_1..N where any same-UID
    // process can read it via /proc/<pid>/environ on Linux. The file
    // path is still visible in environ, but the *contents* are no
    // longer there. Firefox subprocesses inherit the same env var, so
    // the launcher must keep the file alive for the lifetime of the
    // browser session and remove it on shutdown.
    if (auto pathOpt = get_env_utf8("CAMOU_CONFIG_FILE"); pathOpt) {
      // The launcher writes this file just before spawning the browser, but a
      // process can occasionally reach GetJson() during a brief window where the
      // file is not yet readable to it. Because this result is memoised via
      // std::call_once, a single transient failure used to be cached for the
      // whole process lifetime — silently disabling EVERY parent-side MaskConfig
      // feature (e.g. speech-synth voice registration, so getVoices() == 0).
      // Retry briefly (bounded, ~200ms worst case; zero delay on the common
      // path where the first read succeeds) so a transient not-yet-readable
      // window resolves instead of poisoning the process.
      std::optional<std::string> fileContents;
      for (int attempt = 0; attempt < 8; ++attempt) {
        fileContents = read_file_utf8(*pathOpt);
        if (fileContents) break;
        std::this_thread::sleep_for(std::chrono::milliseconds(25));
      }
      if (fileContents) {
        jsonString = *fileContents;
      } else {
        // Still unreadable after retries: the operator explicitly asked for
        // file-based transport but the file is unreadable. Surface this loudly —
        // silently falling back to env vars would mask a misconfiguration.
        printf_stderr(
            "ERROR: CAMOU_CONFIG_FILE set but could not read '%s'.\n",
            pathOpt->c_str());
        jsonConfig = nlohmann::json{};
        return;
      }
    }

    if (jsonString.empty()) {
      int index = 1;
      while (true) {
        std::string envName = "CAMOU_CONFIG_" + std::to_string(index);
        auto partialConfig = get_env_utf8(envName);
        if (!partialConfig) break;

        jsonString += *partialConfig;
        index++;
      }
    }

    if (jsonString.empty()) {
      // Check for the original CAMOU_CONFIG as fallback
      auto originalConfig = get_env_utf8("CAMOU_CONFIG");
      if (originalConfig) jsonString = *originalConfig;
    }

    if (jsonString.empty()) {
      jsonConfig = nlohmann::json{};
      return;
    }

    // Validate
    if (!nlohmann::json::accept(jsonString)) {
      printf_stderr("ERROR: Invalid JSON passed to CAMOU_CONFIG!\n");
      jsonConfig = nlohmann::json{};
      return;
    }

    jsonConfig = nlohmann::json::parse(jsonString);
  });

  return jsonConfig;
}

inline bool HasKey(const std::string& key, const nlohmann::json& data) {
  return data.contains(key);
}

inline std::optional<std::string> GetString(const std::string& key) {
  const auto& data = GetJson();
  if (!HasKey(key, data)) return std::nullopt;
  if (!data[key].is_string()) {
    CAMOU_MASKCFG_LOG("MaskConfig: value for key '%s' is not a string\n",
                      key.c_str());
    return std::nullopt;
  }
  return data[key].get<std::string>();
}

inline std::vector<std::string> GetStringList(const std::string& key) {
  std::vector<std::string> result;
  const auto& data = GetJson();
  if (!HasKey(key, data)) return {};
  if (!data[key].is_array()) {
    CAMOU_MASKCFG_LOG("MaskConfig: value for key '%s' is not a string list\n",
                      key.c_str());
    return {};
  }
  for (const auto& item : data[key]) {
    if (!item.is_string()) {
      CAMOU_MASKCFG_LOG("MaskConfig: skipping non-string item in '%s'\n",
                        key.c_str());
      continue;
    }
    result.push_back(item.get<std::string>());
  }
  return result;
}

inline std::vector<std::string> GetStringListLower(const std::string& key) {
  std::vector<std::string> result = GetStringList(key);
  for (auto& str : result) {
    std::transform(str.begin(), str.end(), str.begin(),
                   [](unsigned char c) { return std::tolower(c); });
  }
  return result;
}

template <typename T>
inline std::optional<T> GetUintImpl(const std::string& key) {
  const auto& data = GetJson();
  if (!HasKey(key, data)) return std::nullopt;
  if (data[key].is_number_unsigned()) {
    uint64_t value = data[key].get<uint64_t>();
    if (value <= std::numeric_limits<T>::max()) {
      return static_cast<T>(value);
    }
    CAMOU_MASKCFG_LOG("MaskConfig: value for key '%s' is out of range\n",
                      key.c_str());
    return std::nullopt;
  }
  CAMOU_MASKCFG_LOG("MaskConfig: value for key '%s' is not an unsigned integer\n",
                    key.c_str());
  return std::nullopt;
}

inline std::optional<uint64_t> GetUint64(const std::string& key) {
  return GetUintImpl<uint64_t>(key);
}

inline std::optional<uint32_t> GetUint32(const std::string& key) {
  return GetUintImpl<uint32_t>(key);
}

inline std::optional<int32_t> GetInt32(const std::string& key) {
  const auto& data = GetJson();
  if (!HasKey(key, data)) return std::nullopt;
  if (data[key].is_number_integer()) {
    int64_t value = data[key].get<int64_t>();
    if (value >= std::numeric_limits<int32_t>::min() &&
        value <= std::numeric_limits<int32_t>::max()) {
      return static_cast<int32_t>(value);
    }
    CAMOU_MASKCFG_LOG("MaskConfig: value for key '%s' is out of range\n",
                      key.c_str());
    return std::nullopt;
  }
  CAMOU_MASKCFG_LOG("MaskConfig: value for key '%s' is not an integer\n",
                    key.c_str());
  return std::nullopt;
}

inline std::optional<double> GetDouble(const std::string& key) {
  const auto& data = GetJson();
  if (!HasKey(key, data)) return std::nullopt;
  if (data[key].is_number_float()) return data[key].get<double>();
  if (data[key].is_number_unsigned())
    return static_cast<double>(data[key].get<uint64_t>());
  if (data[key].is_number_integer())
    return static_cast<double>(data[key].get<int64_t>());
  CAMOU_MASKCFG_LOG("MaskConfig: value for key '%s' is not a double\n",
                    key.c_str());
  return std::nullopt;
}

inline std::optional<bool> GetBool(const std::string& key) {
  const auto& data = GetJson();
  if (!HasKey(key, data)) return std::nullopt;
  if (data[key].is_boolean()) return data[key].get<bool>();
  CAMOU_MASKCFG_LOG("MaskConfig: value for key '%s' is not a boolean\n",
                    key.c_str());
  return std::nullopt;
}

inline bool CheckBool(const std::string& key) {
  return GetBool(key).value_or(false);
}

inline std::optional<std::array<uint32_t, 4>> GetRect(
    const std::string& left, const std::string& top, const std::string& width,
    const std::string& height) {
  std::array<std::optional<uint32_t>, 4> values = {
      GetUint32(left).value_or(0), GetUint32(top).value_or(0), GetUint32(width),
      GetUint32(height)};

  if (!values[2].has_value() || !values[3].has_value()) {
    if (values[2].has_value() ^ values[3].has_value())
      CAMOU_MASKCFG_LOG(
          "MaskConfig: both %s and %s must be provided. Using default.\n",
          width.c_str(), height.c_str());
    return std::nullopt;
  }

  std::array<uint32_t, 4> result;
  std::transform(values.begin(), values.end(), result.begin(),
                 [](const auto& value) { return value.value(); });

  return result;
}

inline std::optional<std::array<int32_t, 4>> GetInt32Rect(
    const std::string& left, const std::string& top, const std::string& width,
    const std::string& height) {
  if (auto optValue = GetRect(left, top, width, height)) {
    std::array<int32_t, 4> result;
    for (const auto& val : *optValue) {
      if (val > static_cast<uint32_t>(std::numeric_limits<int32_t>::max())) {
        CAMOU_MASKCFG_LOG(
            "MaskConfig: rectangle value is out of int32 range. Using default.\n");
        return std::nullopt;
      }
    }
    std::transform(optValue->begin(), optValue->end(), result.begin(),
                   [](const auto& val) { return static_cast<int32_t>(val); });
    return result;
  }
  return std::nullopt;
}

// Helpers for WebGL and bulk extraction

inline std::optional<nlohmann::json> GetNestedObject(const std::string& domain) {
  const auto& data = GetJson();
  if (!data.contains(domain)) return std::nullopt;
  if (!data[domain].is_object()) return std::nullopt;
  return data[domain];
}

inline std::optional<nlohmann::json> GetNested(const std::string& domain,
                                               std::string keyStr) {
  // Use a reference (not a copy) to GetJson(). GetJson() returns a const
  // reference to a process-static nlohmann::json owned by std::call_once;
  // the previous `auto data = GetJson();` copied the entire identity blob
  // on every call. GetNested() is the hot path for every WebGL parameter
  // lookup (MParamGL, MParamGLVector, MShaderData, GetAttribute), which
  // can run hundreds of times per rendered frame on WebGL-heavy sites.
  const auto& data = GetJson();
  if (!data.contains(domain)) return std::nullopt;

  const auto& domainObj = data.at(domain);
  if (!domainObj.contains(keyStr)) return std::nullopt;

  return domainObj.at(keyStr);
}

template <typename T>
inline std::optional<T> GetAttribute(const std::string attrib, bool isWebGL2) {
  auto value = MaskConfig::GetNested(
      isWebGL2 ? "webGl2:contextAttributes" : "webGl:contextAttributes",
      attrib);
  if (!value) return std::nullopt;
  if (!JsonValueMatches<T>(value.value())) {
    CAMOU_MASKCFG_LOG("MaskConfig: context attribute '%s' has wrong type\n",
                      attrib.c_str());
    return std::nullopt;
  }
  return value.value().get<T>();
}

inline std::optional<
    std::variant<int64_t, bool, double, std::string, std::nullptr_t>>
GLParam(uint32_t pname, bool isWebGL2) {
  auto value =
      MaskConfig::GetNested(isWebGL2 ? "webGl2:parameters" : "webGl:parameters",
                            std::to_string(pname));
  if (!value) return std::nullopt;
  auto data = value.value();
  if (data.is_null()) return std::nullptr_t();
  if (data.is_number_integer()) return data.get<int64_t>();
  if (data.is_boolean()) return data.get<bool>();
  if (data.is_number_float()) return data.get<double>();
  if (data.is_string()) return data.get<std::string>();
  return std::nullopt;
}

template <typename T>
inline T MParamGL(uint32_t pname, T defaultValue, bool isWebGL2) {
  if (auto value = MaskConfig::GetNested(
          isWebGL2 ? "webGl2:parameters" : "webGl:parameters",
          std::to_string(pname));
      value.has_value()) {
    if (!JsonValueMatches<T>(value.value())) {
      CAMOU_MASKCFG_LOG("MaskConfig: GL parameter '%u' has wrong type\n",
                        pname);
      return defaultValue;
    }
    return value.value().get<T>();
  }
  return defaultValue;
}

template <typename T>
inline std::vector<T> MParamGLVector(uint32_t pname,
                                     std::vector<T> defaultValue,
                                     bool isWebGL2) {
  if (auto value = MaskConfig::GetNested(
          isWebGL2 ? "webGl2:parameters" : "webGl:parameters",
          std::to_string(pname));
      value.has_value()) {
    if (value.value().is_array()) {
      for (const auto& item : value.value()) {
        if (!JsonScalarMatches<T>(item)) {
          CAMOU_MASKCFG_LOG("MaskConfig: GL vector parameter '%u' has wrong type\n",
                            pname);
          return defaultValue;
        }
      }
      return value.value().get<std::vector<T>>();
    }
  }
  return defaultValue;
}

inline std::optional<std::array<int32_t, 3UL>> MShaderData(
    uint32_t shaderType, uint32_t precisionType, bool isWebGL2) {
  std::string valueName =
      std::to_string(shaderType) + "," + std::to_string(precisionType);
  if (auto value =
          MaskConfig::GetNested(isWebGL2 ? "webGl2:shaderPrecisionFormats"
                                         : "webGl:shaderPrecisionFormats",
                                valueName)) {
    // Convert {rangeMin: int, rangeMax: int, precision: int} to array
    auto data = value.value();
    // Assert rangeMin, rangeMax, and precision are present
    if (!data.contains("rangeMin") || !data.contains("rangeMax") ||
        !data.contains("precision")) {
      return std::nullopt;
    }
    if (!data["rangeMin"].is_number_integer() ||
        !data["rangeMax"].is_number_integer() ||
        !data["precision"].is_number_integer()) {
      return std::nullopt;
    }
    int64_t rangeMin = data["rangeMin"].get<int64_t>();
    int64_t rangeMax = data["rangeMax"].get<int64_t>();
    int64_t precision = data["precision"].get<int64_t>();
    if (rangeMin < std::numeric_limits<int32_t>::min() ||
        rangeMin > std::numeric_limits<int32_t>::max() ||
        rangeMax < std::numeric_limits<int32_t>::min() ||
        rangeMax > std::numeric_limits<int32_t>::max() ||
        precision < std::numeric_limits<int32_t>::min() ||
        precision > std::numeric_limits<int32_t>::max()) {
      return std::nullopt;
    }
    return std::array<int32_t, 3U>{static_cast<int32_t>(rangeMin),
                                   static_cast<int32_t>(rangeMax),
                                   static_cast<int32_t>(precision)};
  }
  return std::nullopt;
}

inline std::optional<
    std::vector<std::tuple<std::string, std::string, std::string, bool, bool>>>
MVoices() {
  // Reference, not a copy: GetJson() returns a process-static blob and the
  // previous `auto data =` deep-copied the entire identity JSON on the one
  // call that builds the cached VoiceState. Read-only access below.
  const auto& data = GetJson();
  if (!data.contains("voices") || !data["voices"].is_array()) {
    return std::nullopt;
  }

  std::vector<std::tuple<std::string, std::string, std::string, bool, bool>>
      voices;
  for (const auto& voice : data["voices"]) {
    // Check if voice has all required fields
    if (!voice.contains("lang") || !voice.contains("name") ||
        !voice.contains("voiceUri") || !voice.contains("isDefault") ||
        !voice.contains("isLocalService")) {
      continue;
    }
    if (!voice["lang"].is_string() || !voice["name"].is_string() ||
        !voice["voiceUri"].is_string() || !voice["isDefault"].is_boolean() ||
        !voice["isLocalService"].is_boolean()) {
      continue;
    }

    voices.emplace_back(
        voice["lang"].get<std::string>(), voice["name"].get<std::string>(),
        voice["voiceUri"].get<std::string>(), voice["isDefault"].get<bool>(),
        voice["isLocalService"].get<bool>());
  }
  return voices;
}

}  // namespace MaskConfig
