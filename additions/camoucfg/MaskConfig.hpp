/*
Helper to extract values from the CAMOU_CONFIG environment variable(s).
Written by daijro.
*/

#pragma once
#include "json.hpp"
#include <memory>
#include <string>
#include <tuple>
#include <optional>
#include "mozilla/glue/Debug.h"
#include <cstdlib>
#include <cstdio>
#include <mutex>
#include <variant>
#include <cstddef>
#include <vector>
#include <algorithm>
#include <cctype>

#ifdef _WIN32
#  include <windows.h>
#endif

namespace MaskConfig {

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
// Previously this checked only the length of the value on Windows
// (size == 2), which incorrectly returned true for *any* single-byte
// value such as "0", "x", or " ". See remediation note for §1.4.
inline bool _IsTruthyEnv(const char* name) {
  std::string value;
#ifdef _WIN32
  std::wstring wname(name, name + std::char_traits<char>::length(name));
  DWORD size = GetEnvironmentVariableW(wname.c_str(), nullptr, 0);
  if (size == 0) return false;
  std::vector<wchar_t> wbuf(size);
  // got >= size means env var grew between calls; the buffer is truncated
  // and NOT NUL-terminated, so WideCharToMultiByte would read past it.
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

inline bool DebugEnabled() {
  return _IsTruthyEnv("CAMOU_MASKCFG_DEBUG");
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
  std::string result(utf8Size - 1, '\0');
  WideCharToMultiByte(CP_UTF8, 0, wValue.c_str(), -1,
                      result.data(), utf8Size, nullptr, nullptr);
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
      if (auto fileContents = read_file_utf8(*pathOpt); fileContents) {
        jsonString = *fileContents;
      } else {
        // Fatal: the operator explicitly asked for file-based transport
        // but the file is unreadable. Surface this loudly — silently
        // falling back to env vars would mask a misconfiguration.
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
  return data[key].get<std::string>();
}

inline std::vector<std::string> GetStringList(const std::string& key) {
  std::vector<std::string> result;
  const auto& data = GetJson();
  if (!HasKey(key, data)) return {};
  for (const auto& item : data[key]) {
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
  if (data[key].is_number_unsigned()) return data[key].get<T>();
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
  if (data[key].is_number_integer()) return data[key].get<int32_t>();
  CAMOU_MASKCFG_LOG("MaskConfig: value for key '%s' is not an integer\n",
                    key.c_str());
  return std::nullopt;
}

inline std::optional<double> GetDouble(const std::string& key) {
  const auto& data = GetJson();
  if (!HasKey(key, data)) return std::nullopt;
  if (data[key].is_number_float()) return data[key].get<double>();
  if (data[key].is_number_unsigned() || data[key].is_number_integer())
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
          height.c_str(), width.c_str());
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
  auto data = GetJson();
  if (!data.contains(domain)) return std::nullopt;

  if (!data[domain].contains(keyStr)) return std::nullopt;

  return data[domain][keyStr];
}

template <typename T>
inline std::optional<T> GetAttribute(const std::string attrib, bool isWebGL2) {
  auto value = MaskConfig::GetNested(
      isWebGL2 ? "webGl2:contextAttributes" : "webGl:contextAttributes",
      attrib);
  if (!value) return std::nullopt;
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
    return std::array<int32_t, 3U>{data["rangeMin"].get<int32_t>(),
                                   data["rangeMax"].get<int32_t>(),
                                   data["precision"].get<int32_t>()};
  }
  return std::nullopt;
}

inline std::optional<
    std::vector<std::tuple<std::string, std::string, std::string, bool, bool>>>
MVoices() {
  auto data = GetJson();
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

    voices.emplace_back(
        voice["lang"].get<std::string>(), voice["name"].get<std::string>(),
        voice["voiceUri"].get<std::string>(), voice["isDefault"].get<bool>(),
        voice["isLocalService"].get<bool>());
  }
  return voices;
}

}  // namespace MaskConfig
