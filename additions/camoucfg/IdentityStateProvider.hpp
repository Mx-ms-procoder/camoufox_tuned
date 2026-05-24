/*
Central accessors for session identity state.

The provider groups correlated spoofed values behind one contract so Gecko
patches no longer need to hardcode individual MaskConfig lookups all over the
tree. The backing store is still MaskConfig JSON today, but the interface is
structured so it can later be redirected to shared memory, IPC, or a generated
identity blob without rewriting each patch site.

All Get*State() accessors cache their result via std::call_once so the JSON
is parsed at most once per subsystem per process lifetime.
*/

#pragma once

#include "MaskConfig.hpp"
#include <array>
#include <cstdint>
#include <mutex>
#include <optional>
#include <string>
#include <tuple>
#include <vector>

namespace IdentityStateProvider {

// ── Subsystem state structs ─────────────────────────────────────────

struct NavigatorState {
  std::optional<std::string> userAgent;
  std::optional<std::string> appCodeName;
  std::optional<std::string> appName;
  std::optional<std::string> appVersion;
  std::optional<std::string> buildID;
  std::optional<std::string> language;
  std::vector<std::string> languages;
  std::optional<std::string> platform;
  std::optional<std::string> oscpu;
  std::optional<std::string> product;
  std::optional<std::string> productSub;
  std::optional<std::string> doNotTrack;
  std::optional<bool> globalPrivacyControl;
  std::optional<uint64_t> hardwareConcurrency;
  std::optional<uint32_t> maxTouchPoints;
};

struct DisplayState {
  std::optional<uint32_t> availLeft;
  std::optional<uint32_t> availTop;
  std::optional<int32_t> screenX;
  std::optional<int32_t> screenY;
  std::optional<uint32_t> width;
  std::optional<uint32_t> height;
  std::optional<uint32_t> availWidth;
  std::optional<uint32_t> availHeight;
  std::optional<uint32_t> outerWidth;
  std::optional<uint32_t> outerHeight;
  std::optional<uint32_t> innerWidth;
  std::optional<uint32_t> innerHeight;
  std::optional<int32_t> clientLeft;
  std::optional<int32_t> clientTop;
  std::optional<uint32_t> clientWidth;
  std::optional<uint32_t> clientHeight;
  std::optional<uint32_t> historyLength;
  std::optional<uint32_t> pixelDepth;
  std::optional<uint32_t> colorDepth;
  std::optional<double> devicePixelRatio;
  std::optional<int32_t> scrollMinX;
  std::optional<int32_t> scrollMinY;
  std::optional<int32_t> scrollMaxX;
  std::optional<int32_t> scrollMaxY;
  std::optional<double> pageXOffset;
  std::optional<double> pageYOffset;
};

struct AudioState {
  std::optional<uint32_t> sampleRate;
  std::optional<uint32_t> maxChannelCount;
  std::optional<double> outputLatency;
};

struct WebGLState {
  std::optional<std::string> vendor;
  std::optional<std::string> renderer;
  // Extended WebGL state for cross-subsystem coherence validation.
  // MAX_VIEWPORT_DIMS should never exceed the display resolution.
  std::optional<uint32_t> maxViewportWidth;
  std::optional<uint32_t> maxViewportHeight;
  bool webGl2Enabled = false;
};

struct CanvasState {
  std::optional<int32_t> aaOffset;
  std::optional<bool> aaCapOffset;
  std::optional<uint64_t> noiseSeed;
};

struct FontState {
  std::vector<std::string> fontList;
  std::optional<uint32_t> spacingSeed;
};

struct HeaderState {
  std::optional<std::string> userAgent;
  std::optional<std::string> acceptLanguage;
  std::optional<std::string> acceptEncoding;
};

// K-21 (AUDIT_2026-05-18.md): HTTP/2 fingerprint state. Mirrors the
// fields produced by `pythonlib/camoufox/tls_profiles.get_http2_config()`
// when the experimental opt-in is set. Consumers should treat each
// optional<> as "use upstream Firefox default when absent" — that way
// the same accessor is safe to call even on a build whose
// Http2Session.cpp has not yet been patched to honour the values.
struct Http2State {
  // SETTINGS frame values (RFC 7540 §6.5.2)
  std::optional<uint32_t> headerTableSize;       // SETTINGS_HEADER_TABLE_SIZE (id 0x1)
  std::optional<uint32_t> enablePush;            // SETTINGS_ENABLE_PUSH (id 0x2)
  std::optional<uint32_t> initialWindowSize;     // SETTINGS_INITIAL_WINDOW_SIZE (id 0x4)
  std::optional<uint32_t> maxFrameSize;          // SETTINGS_MAX_FRAME_SIZE (id 0x5)
  std::optional<uint32_t> maxConcurrentStreams;  // SETTINGS_MAX_CONCURRENT_STREAMS (id 0x3)
  std::optional<uint32_t> maxHeaderListSize;     // SETTINGS_MAX_HEADER_LIST_SIZE (id 0x6)

  // Initial connection-level WINDOW_UPDATE increment that Firefox emits
  // immediately after the preface + SETTINGS frame. Firefox 135 uses
  // 12517377; other versions may differ.
  std::optional<uint32_t> windowUpdate;

  // Default stream weight used for HEADERS-frame PRIORITY hints (RFC
  // 7540 §5.3.5 — value range 1..256 wire-encoded as N-1, Firefox uses 42).
  std::optional<uint32_t> priorityWeight;
};

struct BatteryState {
  std::optional<bool> charging;
  std::optional<double> chargingTime;
  std::optional<double> dischargingTime;
  std::optional<double> level;
};

struct MediaDeviceState {
  bool enabled = false;
  uint32_t microphones = 3;
  uint32_t webcams = 1;
  uint32_t speakers = 1;
};

struct VoiceState {
  std::optional<bool> blockIfNotDefined;
  std::optional<bool> fakeCompletion;
  std::optional<double> charsPerSecond;
  std::vector<std::tuple<std::string, std::string, std::string, bool, bool>>
      voices;
};

struct RuntimeState {
  std::optional<bool> enableRemoteSubframes;
  std::optional<bool> disableTheming;
};

// ── Aggregated identity blob ────────────────────────────────────────

struct IdentityBlob {
  std::optional<NavigatorState> navigator;
  std::optional<DisplayState> display;
  std::optional<AudioState> audio;
  std::optional<WebGLState> webgl;
  std::optional<CanvasState> canvas;
  std::optional<FontState> fonts;
  std::optional<HeaderState> headers;
  std::optional<Http2State> http2;
  std::optional<BatteryState> battery;
  std::optional<MediaDeviceState> mediaDevices;
  std::optional<VoiceState> voice;
  std::optional<RuntimeState> runtime;
};

// ── Cached accessors ────────────────────────────────────────────────
// Each accessor parses the MaskConfig JSON at most once and caches the
// result for the process lifetime.

namespace detail {

template <typename T>
struct CachedState {
  std::once_flag flag;
  std::optional<T> value;
};

}  // namespace detail

inline std::optional<NavigatorState> GetNavigatorState() {
  static detail::CachedState<NavigatorState> cache;
  std::call_once(cache.flag, []() {
    NavigatorState state{
        MaskConfig::GetString("navigator.userAgent"),
        MaskConfig::GetString("navigator.appCodeName"),
        MaskConfig::GetString("navigator.appName"),
        MaskConfig::GetString("navigator.appVersion"),
        MaskConfig::GetString("navigator.buildID"),
        MaskConfig::GetString("navigator.language"),
        MaskConfig::GetStringList("navigator.languages"),
        MaskConfig::GetString("navigator.platform"),
        MaskConfig::GetString("navigator.oscpu"),
        MaskConfig::GetString("navigator.product"),
        MaskConfig::GetString("navigator.productSub"),
        MaskConfig::GetString("navigator.doNotTrack"),
        MaskConfig::GetBool("navigator.globalPrivacyControl"),
        MaskConfig::GetUint64("navigator.hardwareConcurrency"),
        MaskConfig::GetUint32("navigator.maxTouchPoints"),
    };

    if (!state.userAgent && !state.appCodeName && !state.appName &&
        !state.appVersion && !state.buildID && !state.language &&
        state.languages.empty() && !state.platform && !state.oscpu &&
        !state.product && !state.productSub && !state.doNotTrack &&
        !state.globalPrivacyControl && !state.hardwareConcurrency &&
        !state.maxTouchPoints) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<DisplayState> GetDisplayState() {
  static detail::CachedState<DisplayState> cache;
  std::call_once(cache.flag, []() {
    DisplayState state{
        MaskConfig::GetUint32("screen.availLeft"),
        MaskConfig::GetUint32("screen.availTop"),
        MaskConfig::GetInt32("window.screenX"),
        MaskConfig::GetInt32("window.screenY"),
        MaskConfig::GetUint32("screen.width"),
        MaskConfig::GetUint32("screen.height"),
        MaskConfig::GetUint32("screen.availWidth"),
        MaskConfig::GetUint32("screen.availHeight"),
        MaskConfig::GetUint32("window.outerWidth"),
        MaskConfig::GetUint32("window.outerHeight"),
        MaskConfig::GetUint32("window.innerWidth"),
        MaskConfig::GetUint32("window.innerHeight"),
        MaskConfig::GetInt32("document.body.clientLeft"),
        MaskConfig::GetInt32("document.body.clientTop"),
        MaskConfig::GetUint32("document.body.clientWidth"),
        MaskConfig::GetUint32("document.body.clientHeight"),
        MaskConfig::GetUint32("window.history.length"),
        MaskConfig::GetUint32("screen.pixelDepth"),
        MaskConfig::GetUint32("screen.colorDepth"),
        MaskConfig::GetDouble("window.devicePixelRatio"),
        MaskConfig::GetInt32("window.scrollMinX"),
        MaskConfig::GetInt32("window.scrollMinY"),
        MaskConfig::GetInt32("window.scrollMaxX"),
        MaskConfig::GetInt32("window.scrollMaxY"),
        MaskConfig::GetDouble("screen.pageXOffset"),
        MaskConfig::GetDouble("screen.pageYOffset"),
    };

    if (!state.availLeft && !state.availTop && !state.screenX &&
        !state.screenY && !state.width && !state.height && !state.availWidth &&
        !state.availHeight && !state.outerWidth &&
        !state.outerHeight && !state.innerWidth && !state.innerHeight &&
        !state.clientLeft && !state.clientTop && !state.clientWidth &&
        !state.clientHeight && !state.historyLength && !state.pixelDepth &&
        !state.colorDepth && !state.devicePixelRatio && !state.scrollMinX &&
        !state.scrollMinY && !state.scrollMaxX && !state.scrollMaxY &&
        !state.pageXOffset && !state.pageYOffset) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<AudioState> GetAudioState() {
  static detail::CachedState<AudioState> cache;
  std::call_once(cache.flag, []() {
    AudioState state{
        MaskConfig::GetUint32("AudioContext:sampleRate"),
        MaskConfig::GetUint32("AudioContext:maxChannelCount"),
        MaskConfig::GetDouble("AudioContext:outputLatency"),
    };
    if (!state.sampleRate && !state.maxChannelCount && !state.outputLatency) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<WebGLState> GetWebGLState() {
  static detail::CachedState<WebGLState> cache;
  std::call_once(cache.flag, []() {
    WebGLState state{
        MaskConfig::GetString("webGl:vendor"),
        MaskConfig::GetString("webGl:renderer"),
        std::nullopt,  // maxViewportWidth — derived from display if needed
        std::nullopt,  // maxViewportHeight
        false,         // webGl2Enabled
    };

    // Cross-reference with display state: MAX_VIEWPORT_DIMS must be >= screen
    auto displayWidth = MaskConfig::GetUint32("screen.width");
    auto displayHeight = MaskConfig::GetUint32("screen.height");
    if (displayWidth) state.maxViewportWidth = displayWidth;
    if (displayHeight) state.maxViewportHeight = displayHeight;

    if (!state.vendor && !state.renderer) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<CanvasState> GetCanvasState() {
  static detail::CachedState<CanvasState> cache;
  std::call_once(cache.flag, []() {
    CanvasState state{
        MaskConfig::GetInt32("canvas:aaOffset"),
        MaskConfig::GetBool("canvas:aaCapOffset"),
        MaskConfig::GetUint64("canvas:noiseSeed"),
    };
    if (!state.aaOffset && !state.aaCapOffset && !state.noiseSeed) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<FontState> GetFontState() {
  static detail::CachedState<FontState> cache;
  std::call_once(cache.flag, []() {
    FontState state{
        MaskConfig::GetStringList("fonts"),
        MaskConfig::GetUint32("fonts:spacing_seed"),
    };
    if (state.fontList.empty() && !state.spacingSeed) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<HeaderState> GetHeaderState() {
  static detail::CachedState<HeaderState> cache;
  std::call_once(cache.flag, []() {
    HeaderState state{
        MaskConfig::GetString("headers.User-Agent"),
        MaskConfig::GetString("headers.Accept-Language"),
        MaskConfig::GetString("headers.Accept-Encoding"),
    };
    // C-3 partial fix: cross-fill from navigator.* so HTTP headers and
    // JS navigator.* stay consistent. The most common Cloudflare /
    // DataDome / fingerprintjs-pro detection vector is HTTP-UA differing
    // from navigator.userAgent. Same applies to Accept-Language vs
    // navigator.languages[0]. We only fall back — explicit `headers.*`
    // keys still take precedence, in case the operator intentionally
    // wants a divergent set (e.g. testing detection robustness).
    if (!state.userAgent) {
      if (auto ua = MaskConfig::GetString("navigator.userAgent")) {
        state.userAgent = std::move(ua);
      }
    }
    if (!state.acceptLanguage) {
      auto langs = MaskConfig::GetStringList("navigator.languages");
      if (!langs.empty()) {
        // Build Accept-Language with q-values matching Firefox's default
        // formatting: "primary, secondary;q=0.7, tertiary;q=0.3, ...".
        std::string al;
        for (size_t i = 0; i < langs.size(); ++i) {
          if (i > 0) al += ", ";
          al += langs[i];
          if (i > 0) {
            // q drops by 0.3 per step, floored at 0.1, mirroring
            // Firefox's nsHttpHandler::PrepareAcceptLanguages.
            double q = std::max(0.1, 1.0 - 0.3 * static_cast<double>(i));
            char buf[16];
            std::snprintf(buf, sizeof(buf), ";q=%.1f", q);
            al += buf;
          }
        }
        state.acceptLanguage = std::move(al);
      } else if (auto lang = MaskConfig::GetString("navigator.language")) {
        state.acceptLanguage = std::move(lang);
      }
    }
    if (!state.userAgent && !state.acceptLanguage && !state.acceptEncoding) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<Http2State> GetHttp2State() {
  // K-21 (AUDIT_2026-05-18.md). Reads the HTTP/2 SETTINGS / initial
  // WINDOW_UPDATE / default priority weight from MaskConfig. Returns
  // nullopt when no http2:* keys are present, so the caller in
  // Http2Session.cpp can short-circuit to upstream behaviour with one
  // check.
  static detail::CachedState<Http2State> cache;
  std::call_once(cache.flag, []() {
    Http2State state{
        MaskConfig::GetUint32("http2:headerTableSize"),
        MaskConfig::GetUint32("http2:enablePush"),
        MaskConfig::GetUint32("http2:initialWindowSize"),
        MaskConfig::GetUint32("http2:maxFrameSize"),
        MaskConfig::GetUint32("http2:maxConcurrentStreams"),
        MaskConfig::GetUint32("http2:maxHeaderListSize"),
        MaskConfig::GetUint32("http2:windowUpdate"),
        MaskConfig::GetUint32("http2:priorityWeight"),
    };
    if (!state.headerTableSize && !state.enablePush && !state.initialWindowSize &&
        !state.maxFrameSize && !state.maxConcurrentStreams &&
        !state.maxHeaderListSize && !state.windowUpdate && !state.priorityWeight) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<BatteryState> GetBatteryState() {
  static detail::CachedState<BatteryState> cache;
  std::call_once(cache.flag, []() {
    BatteryState state{
        MaskConfig::GetBool("battery:charging"),
        MaskConfig::GetDouble("battery:chargingTime"),
        MaskConfig::GetDouble("battery:dischargingTime"),
        MaskConfig::GetDouble("battery:level"),
    };
    if (!state.charging && !state.chargingTime && !state.dischargingTime &&
        !state.level) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<MediaDeviceState> GetMediaDeviceState() {
  static detail::CachedState<MediaDeviceState> cache;
  std::call_once(cache.flag, []() {
    if (!MaskConfig::GetBool("mediaDevices:enabled").has_value() &&
        !MaskConfig::GetUint32("mediaDevices:micros").has_value() &&
        !MaskConfig::GetUint32("mediaDevices:webcams").has_value() &&
        !MaskConfig::GetUint32("mediaDevices:speakers").has_value()) {
      cache.value = std::nullopt;
    } else {
      cache.value = MediaDeviceState{
          MaskConfig::GetBool("mediaDevices:enabled").value_or(false),
          MaskConfig::GetUint32("mediaDevices:micros").value_or(3),
          MaskConfig::GetUint32("mediaDevices:webcams").value_or(1),
          MaskConfig::GetUint32("mediaDevices:speakers").value_or(1),
      };
    }
  });
  return cache.value;
}

inline std::optional<VoiceState> GetVoiceState() {
  static detail::CachedState<VoiceState> cache;
  std::call_once(cache.flag, []() {
    VoiceState state{
        MaskConfig::GetBool("voices:blockIfNotDefined"),
        MaskConfig::GetBool("voices:fakeCompletion"),
        MaskConfig::GetDouble("voices:fakeCompletion:charsPerSecond"),
        MaskConfig::MVoices().value_or(
            std::vector<
                std::tuple<std::string, std::string, std::string, bool, bool>>{}),
    };
    if (!state.blockIfNotDefined && !state.fakeCompletion &&
        !state.charsPerSecond && state.voices.empty()) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

inline std::optional<RuntimeState> GetRuntimeState() {
  static detail::CachedState<RuntimeState> cache;
  std::call_once(cache.flag, []() {
    RuntimeState state{
        MaskConfig::GetBool("enableRemoteSubframes"),
        MaskConfig::GetBool("disableTheming"),
    };
    if (!state.enableRemoteSubframes && !state.disableTheming) {
      cache.value = std::nullopt;
    } else {
      cache.value = state;
    }
  });
  return cache.value;
}

// ── Aggregated blob accessor ────────────────────────────────────────

inline const IdentityBlob& GetIdentityBlob() {
  static detail::CachedState<IdentityBlob> cache;
  static IdentityBlob blob;
  std::call_once(cache.flag, []() {
    blob.navigator = GetNavigatorState();
    blob.display = GetDisplayState();
    blob.audio = GetAudioState();
    blob.webgl = GetWebGLState();
    blob.canvas = GetCanvasState();
    blob.fonts = GetFontState();
    blob.headers = GetHeaderState();
    blob.http2 = GetHttp2State();
    blob.battery = GetBatteryState();
    blob.mediaDevices = GetMediaDeviceState();
    blob.voice = GetVoiceState();
    blob.runtime = GetRuntimeState();
  });
  return blob;
}

}  // namespace IdentityStateProvider
