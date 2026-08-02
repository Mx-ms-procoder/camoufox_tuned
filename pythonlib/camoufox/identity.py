"""
Identity coherence engine for Camoufox.

The engine compiles a single session state that feeds all spoofed browser
surfaces. Instead of sampling BrowserForge, fonts, WebGL, screen, and audio
independently, it derives them from one deterministic identity seed and one
OS-scoped device profile.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from random import Random
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

import orjson

# Domain separation tag for fingerprint seed derivation. Bumping the tag
# invalidates every previously persisted seed → fingerprint mapping, so
# only change it when the derivation semantics genuinely shift.
_SEED_DOMAIN_TAG = b"camoufox-fingerprint-seed-v1\x00"


def _derive_seed_material(seed_input: Union[str, int, bytes, bytearray, memoryview]) -> bytes:
    """
    Normalise a user-supplied fingerprint seed into bytes suitable for
    SHA-256 hashing. Booleans are rejected on purpose — they pass
    isinstance(..., int) in Python and would silently collapse the seed
    space to {0, 1}.
    """
    if isinstance(seed_input, bool):
        raise TypeError("fingerprint_seed must not be a bool")
    if isinstance(seed_input, int):
        # Use signed two's-complement so negative ints round-trip cleanly.
        # 16 bytes covers the full int64 range with headroom for arbitrary
        # Python ints up to 2**127.
        return seed_input.to_bytes(16, "big", signed=True)
    if isinstance(seed_input, str):
        return seed_input.encode("utf-8")
    if isinstance(seed_input, (bytes, bytearray, memoryview)):
        return bytes(seed_input)
    raise TypeError(
        f"fingerprint_seed must be str, int, or bytes; got {type(seed_input).__name__}"
    )

from .device_profiles import DeviceProfile, build_font_list, sample_device_profile
from .device_profiles.coherence import validate_coherence
from .network_profile import NetworkProfile
from .tls_profiles import get_firefox_profile_for_version
from .voices import generate_voices

if TYPE_CHECKING:
    from browserforge.fingerprints import Fingerprint

_IDENTITY_PREFIXES = (
    "navigator.",
    "screen.",
    "window.",
    "document.body.",
    "AudioContext:",
    "webGl:",
    "webGl2:",
    "fonts",
    "fonts:",
    "canvas:",
    "headers.",
)

_CHROME_WIDTH_BOUNDS = {
    "win": (12, 32),
    "mac": (0, 24),
    "lin": (8, 32),
}

_CHROME_HEIGHT_BOUNDS = {
    "win": (72, 160),
    "mac": (64, 140),
    "lin": (72, 152),
}


@dataclass(frozen=True)
class WindowMetrics:
    screen_x: int
    screen_y: int
    outer_width: int
    outer_height: int
    inner_width: int
    inner_height: int
    client_width: int
    client_height: int
    page_x_offset: float = 0.0
    page_y_offset: float = 0.0

    def as_config(self) -> Dict[str, Any]:
        return {
            "window.screenX": self.screen_x,
            "window.screenY": self.screen_y,
            "window.outerWidth": self.outer_width,
            "window.outerHeight": self.outer_height,
            "window.innerWidth": self.inner_width,
            "window.innerHeight": self.inner_height,
            "document.body.clientLeft": 0,
            "document.body.clientTop": 0,
            "document.body.clientWidth": self.client_width,
            "document.body.clientHeight": self.client_height,
            # screen.pageXOffset / screen.pageYOffset are deliberately NOT
            # emitted. nsGlobalWindowInner::GetScrollX/GetScrollY return the
            # configured value *instead of* the live scroll position, and these
            # fields only ever held the BrowserForge snapshot value 0.0 — so
            # window.scrollY and window.pageYOffset stayed pinned at 0 for the
            # whole session while the page really did scroll
            # (document.scrollingElement.scrollTop reached 4550 in the same
            # run). Two consequences: every site that reads scrollY for sticky
            # headers, lazy loading, infinite scroll or a "scrolled to the
            # bottom?" consent gate behaves as if the user never scrolled, and
            # `scrollY === 0 && scrollingElement.scrollTop > 0` is a one-line
            # bot check. A scroll offset is session state, not a device
            # characteristic, so there is nothing to spoof here; the config
            # keys stay available for anyone who sets them explicitly.
        }


@dataclass(frozen=True)
class IdentityState:
    profile_id: str
    seed: int
    target_os: str
    device_profile: DeviceProfile
    window_metrics: WindowMetrics
    config: Dict[str, Any]
    firefox_user_prefs: Dict[str, Any]
    network_profile: NetworkProfile
    coherence_issues: Tuple[str, ...]
    manual_overrides: Tuple[str, ...]


def _clip(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _is_identity_key(key: str) -> bool:
    return key.startswith(_IDENTITY_PREFIXES) or key == "fonts"


class IdentityCoherenceEngine:
    """
    Compile one deterministic session identity for all spoofed surfaces.

    Derived values intentionally share the same seed so the final session can
    be regenerated without cross-surface drift.
    """

    def build(
        self,
        *,
        fingerprint: "Fingerprint",
        ff_version: str,
        target_os: str,
        user_config: Optional[Mapping[str, Any]] = None,
        window: Optional[Tuple[int, int]] = None,
        fonts: Optional[Sequence[str]] = None,
        custom_fonts_only: bool = False,
        webgl_enabled: bool = True,
        webgl_config: Optional[Tuple[str, str]] = None,
        fingerprint_seed: Optional[Union[str, int, bytes, bytearray, memoryview]] = None,
    ) -> IdentityState:
        from .fingerprints import from_browserforge

        return self.build_from_base_config(
            base_config=from_browserforge(fingerprint, ff_version),
            target_os=target_os,
            user_config=user_config,
            window=window,
            fonts=fonts,
            custom_fonts_only=custom_fonts_only,
            webgl_enabled=webgl_enabled,
            webgl_config=webgl_config,
            fingerprint_seed=fingerprint_seed,
        )

    def build_from_base_config(
        self,
        *,
        base_config: Mapping[str, Any],
        target_os: str,
        user_config: Optional[Mapping[str, Any]] = None,
        window: Optional[Tuple[int, int]] = None,
        fonts: Optional[Sequence[str]] = None,
        custom_fonts_only: bool = False,
        webgl_enabled: bool = True,
        webgl_config: Optional[Tuple[str, str]] = None,
        fingerprint_seed: Optional[Union[str, int, bytes, bytearray, memoryview]] = None,
    ) -> IdentityState:
        if fingerprint_seed is not None:
            # Persistent-seed mode: the digest is derived from the seed
            # material plus a domain-separation tag, decoupling the
            # deterministic identity from the rest of the user-supplied
            # configuration. Two callers with the same seed get the same
            # device profile / window metrics / canvas offsets, even when
            # other launch parameters differ.
            seed_bytes = _derive_seed_material(fingerprint_seed)
            digest = hashlib.sha256(_SEED_DOMAIN_TAG + seed_bytes).digest()
        else:
            payload = self._seed_payload(
                base_config=base_config,
                target_os=target_os,
                user_config=user_config,
                window=window,
                fonts=fonts,
                custom_fonts_only=custom_fonts_only,
                webgl_enabled=webgl_enabled,
                webgl_config=webgl_config,
            )
            digest = hashlib.sha256(
                orjson.dumps(payload, option=orjson.OPT_SORT_KEYS)
            ).digest()
        seed = int.from_bytes(digest[:8], "big")
        generator = Random(seed)

        screen_hint = self._screen_hint(base_config)
        device_profile = sample_device_profile(
            target_os,
            rng=generator,
            webgl_enabled=webgl_enabled,
            webgl_config=webgl_config,
            screen_hint=screen_hint,
        )
        window_metrics = self._resolve_window_metrics(
            base_config=base_config,
            device_profile=device_profile,
            requested_window=window,
            generator=generator,
        )

        compiled_config = dict(base_config)
        compiled_config.update(device_profile.to_camoufox_config())
        compiled_config.update(window_metrics.as_config())
        compiled_config["fonts"] = build_font_list(
            target_os,
            extra_fonts=fonts,
            custom_only=custom_fonts_only,
        )
        compiled_config["fonts:spacing_seed"] = (
            int.from_bytes(digest[8:12], "big") % 1_073_741_823
        )
        # NOTE: canvas:aaOffset currently has no effect on rendering. The C++
        # side reads it (IdentityStateProvider::GetCanvasState -> GetInt32) but
        # the only caller of GetCanvasState() is the diagnostic identity blob;
        # canvas-noise.patch, which does the actual pixel work, reads
        # canvas:noiseSeed and nothing else. Measured with the identity pinned
        # and only this key varied: aaOffset -20/0/7/24 all produced the same
        # pixel hash and the same toDataURL, while the control (noiseSeed
        # 111 vs 222) did differ -- so the measurement was sound and the key is
        # inert. Kept because it is part of the documented config surface and
        # the coherence check pairs it with noiseSeed; do not assume it
        # contributes entropy. This also answers upstream daijro/camoufox#421,
        # which asks for float instead of int: the type is irrelevant while
        # nothing consumes the value. scripts/check_seed_liveness.py carries a
        # probe so this surfaces if it is ever wired up.
        compiled_config["canvas:aaOffset"] = int(
            max(-24, min(24, round(generator.gauss(0.0, 8.0))))
        )
        compiled_config["canvas:aaCapOffset"] = True
        # T4.3: seed-derived canvas noise so the C++ side
        # (IdentityStateProvider::GetCanvasState — reads
        # canvas:noiseSeed via GetUint64) produces a stable hash per
        # identity. Previously this key was read but never set, so the
        # noise injector silently fell back to its empty default and
        # the aaOffset alone wasn't enough to break a canvas hash.
        compiled_config["canvas:noiseSeed"] = int.from_bytes(
            digest[14:22], "big"
        )
        # Same dead-path failure the canvas noise had: AudioFingerprintManager
        # ::GetSeed() reads the per-context RoverfoxStorage key first and falls
        # back to MaskConfig "audio:seed", but nothing ever wrote either --- the
        # runtime setter that fed the storage key was removed with the rest of
        # the window.set* island, and the launcher never set the config key. So
        # GetSeed() returned 0, ApplyTransformation() early-returned, and the
        # whole audio layer was inert: measured across three identities
        # (seeds 1111/2222/3333) the OfflineAudioContext fingerprint was
        # byte-identical (sum 35.749972093850374) while the claimed hardware
        # ranged from an NVIDIA Windows box to an Apple M1. That is a hard
        # cross-profile link *and* an internal contradiction. GetUint32, so
        # keep it in range.
        compiled_config["audio:seed"] = (
            int.from_bytes(digest[22:26], "big") % 0xFFFFFFFF
        ) + 1
        # window.history.length is deliberately NOT emitted, for the same
        # reason screen.pageXOffset/pageYOffset are not (see WindowMetrics
        # above). nsHistory::GetLength returns the configured value *instead
        # of* the live entry count, so it stayed frozen at one number for the
        # whole session: measured with fixed seeds, `history.length` read
        # [3, 3, 3, 3] and [1, 1, 1, 1] across four consecutive navigations
        # where a real browser counts 1, 2, 3, 4. Navigating and watching the
        # number not move is a one-line bot check, and it is the same
        # category error each time -- history depth is session state, not a
        # device characteristic. With browser.sessionhistory.max_entries no
        # longer pinned to 0 (settings/camoufox.cfg) the real counter works,
        # so there is nothing left to fake; the config key stays available
        # for anyone who sets it explicitly.
        #
        # prefers-color-scheme is handled in _tzhelper.config_color_scheme
        # rather than here. It deliberately does NOT get its own config key:
        # validate_config() checks every key against the properties.json
        # shipped *inside the browser package*, so a new key would raise
        # UnknownProperty on every launch until the next rebuild. It is
        # derived from canvas:noiseSeed instead, which is already part of
        # this same digest and therefore just as seed-stable.
        # Speech-synthesis voices: register a coherent per-OS voice set via
        # config so the browser side (MaskConfig::MVoices, consumed by
        # patches/media/voice-spoofing.patch) never enumerates the host
        # machine's real TTS voices. Seeded by the same generator as every
        # other surface and keyed to the spoofed navigator.language so the
        # default voice lines up with Intl locale (avoids voiceLangMismatch).
        compiled_config["voices"] = generate_voices(
            target_os,
            compiled_config.get("navigator.language"),
            rng=generator,
        )
        # Suppress the HOST machine's real TTS voices (measured leak: a Windows
        # host otherwise exposes "Microsoft Hedda - German" etc. through
        # speechSynthesis.getVoices(), contradicting a spoofed macOS/en-US
        # identity). With this set, nsSynthVoiceRegistry::AddVoice short-circuits
        # every platform-service voice, so only the config `voices` above are
        # ever enumerable. See patches/media/voice-spoofing.patch.
        compiled_config["voices:blockIfNotDefined"] = True
        self._apply_header_defaults(compiled_config)
        self._disable_webgl_null_blocking(compiled_config)

        firefox_user_prefs: Dict[str, Any] = {}
        if webgl_enabled:
            firefox_user_prefs.update(
                {
                    "webgl.enable-webgl2": device_profile.enable_webgl2,
                    "webgl.force-enabled": True,
                }
            )

        manual_overrides = self._manual_override_conflicts(
            compiled_config=compiled_config,
            user_config=user_config,
        )

        from ua_parser import user_agent_parser
        ua = (user_config or {}).get(
            "navigator.userAgent",
            base_config.get("navigator.userAgent", ""),
        )
        ua_parsed = user_agent_parser.ParseUserAgent(ua)
        
        # Camoufox is Firefox-only. Enforce pure Firefox profile even if user overrides UA.
        family_key = "firefox"
        try:
            major_version = int(ua_parsed.get("major", "135"))
        except ValueError:
            major_version = 135

        # Never fall back to the Firefox 135 capture: an unregistered version
        # gets a native-NSS profile for its OWN version instead, so the engine
        # keeps its real handshake rather than wearing a three-generation-old
        # one while the UA advertises the new number.
        network_profile = get_firefox_profile_for_version(major_version)

        # T1.3: device-profile coherence + cross-surface header/navigator
        # checks. The latter catches operators who set headers.User-Agent
        # or headers.Accept-Language directly while letting the engine
        # generate navigator.userAgent / navigator.languages — a classic
        # WAF tripwire because Firefox always sources both from the same
        # internal pref.
        profile_issues = list(validate_coherence(device_profile))
        header_issues = self._header_navigator_conflicts(
            compiled_config=compiled_config,
            user_config=user_config,
        )

        return IdentityState(
            profile_id=digest.hex()[:16],
            seed=seed,
            target_os=target_os,
            device_profile=device_profile,
            window_metrics=window_metrics,
            config=compiled_config,
            firefox_user_prefs=firefox_user_prefs,
            network_profile=network_profile,
            coherence_issues=tuple(profile_issues + header_issues),
            manual_overrides=tuple(manual_overrides),
        )

    def _seed_payload(
        self,
        *,
        base_config: Mapping[str, Any],
        target_os: str,
        user_config: Optional[Mapping[str, Any]],
        window: Optional[Tuple[int, int]],
        fonts: Optional[Sequence[str]],
        custom_fonts_only: bool,
        webgl_enabled: bool,
        webgl_config: Optional[Tuple[str, str]],
    ) -> Dict[str, Any]:
        return {
            "target_os": target_os,
            "base": {
                key: base_config[key]
                for key in sorted(base_config)
                if _is_identity_key(key)
            },
            "manual": {
                key: user_config[key]
                for key in sorted(user_config or {})
                if _is_identity_key(key)
            },
            "window": list(window) if window else None,
            "fonts": sorted(fonts or []),
            "custom_fonts_only": custom_fonts_only,
            "webgl_enabled": webgl_enabled,
            "webgl_config": list(webgl_config) if webgl_config else None,
        }

    def _screen_hint(
        self, base_config: Mapping[str, Any]
    ) -> Optional[Tuple[int, int]]:
        width = base_config.get("screen.width")
        height = base_config.get("screen.height")
        if isinstance(width, int) and isinstance(height, int):
            return width, height
        return None

    def _resolve_window_metrics(
        self,
        *,
        base_config: Mapping[str, Any],
        device_profile: DeviceProfile,
        requested_window: Optional[Tuple[int, int]],
        generator: Random,
    ) -> WindowMetrics:
        avail_width = device_profile.screen_width
        avail_height = max(device_profile.screen_height - device_profile.taskbar_height, 0)
        chrome_width = self._chrome_width(
            base_config=base_config,
            target_os=device_profile.os_family,
        )
        chrome_height = self._chrome_height(
            base_config=base_config,
            target_os=device_profile.os_family,
        )

        if requested_window:
            outer_width = max(640, min(requested_window[0], avail_width))
            outer_height = max(480, min(requested_window[1], max(avail_height, 480)))
        else:
            outer_width, outer_height = self._sample_window_size(
                base_config=base_config,
                device_profile=device_profile,
                avail_width=avail_width,
                avail_height=avail_height,
                generator=generator,
            )

        inner_width = max(200, outer_width - chrome_width)
        inner_height = max(200, outer_height - chrome_height)

        free_x = max(avail_width - outer_width, 0)
        free_y = max(avail_height - outer_height, 0)
        screen_x = int(round(free_x * (0.32 + (0.36 * generator.random()))))
        screen_y = int(round(free_y * (0.14 + (0.28 * generator.random()))))

        return WindowMetrics(
            screen_x=screen_x,
            screen_y=screen_y,
            outer_width=outer_width,
            outer_height=outer_height,
            inner_width=inner_width,
            inner_height=inner_height,
            client_width=inner_width,
            client_height=inner_height,
        )

    def _sample_window_size(
        self,
        *,
        base_config: Mapping[str, Any],
        device_profile: DeviceProfile,
        avail_width: int,
        avail_height: int,
        generator: Random,
    ) -> Tuple[int, int]:
        base_screen_width = int(base_config.get("screen.width", device_profile.screen_width) or 1)
        base_screen_height = int(base_config.get("screen.height", device_profile.screen_height) or 1)
        base_outer_width = int(base_config.get("window.outerWidth", 0) or 0)
        base_outer_height = int(base_config.get("window.outerHeight", 0) or 0)

        if base_outer_width > 0 and base_outer_height > 0:
            width_ratio = _clip(base_outer_width / max(base_screen_width, 1), 0.62, 0.95)
            height_ratio = _clip(base_outer_height / max(base_screen_height, 1), 0.58, 0.94)
        else:
            width_ratio = 0.72 + (0.18 * generator.random())
            height_ratio = 0.68 + (0.16 * generator.random())

        outer_width = min(avail_width, max(960, int(round(avail_width * width_ratio))))
        outer_height = min(avail_height, max(720, int(round(avail_height * height_ratio))))
        return outer_width, outer_height

    def _chrome_width(
        self, *, base_config: Mapping[str, Any], target_os: str
    ) -> int:
        delta = int(
            (base_config.get("window.outerWidth", 0) or 0)
            - (base_config.get("window.innerWidth", 0) or 0)
        )
        lower, upper = _CHROME_WIDTH_BOUNDS[target_os]
        return int(_clip(delta if delta > 0 else lower, lower, upper))

    def _chrome_height(
        self, *, base_config: Mapping[str, Any], target_os: str
    ) -> int:
        delta = int(
            (base_config.get("window.outerHeight", 0) or 0)
            - (base_config.get("window.innerHeight", 0) or 0)
        )
        lower, upper = _CHROME_HEIGHT_BOUNDS[target_os]
        return int(_clip(delta if delta > 0 else lower, lower, upper))

    def _manual_override_conflicts(
        self,
        *,
        compiled_config: Mapping[str, Any],
        user_config: Optional[Mapping[str, Any]],
    ) -> Sequence[str]:
        conflicts = []
        for key, value in (user_config or {}).items():
            if not _is_identity_key(key):
                continue
            if key in compiled_config and compiled_config[key] != value:
                conflicts.append(key)
        return conflicts

    def _apply_header_defaults(self, compiled_config: Dict[str, Any]) -> None:
        """Keep HTTP headers on the same identity as navigator.* by default."""
        if compiled_config.get("navigator.userAgent"):
            compiled_config.setdefault(
                "headers.User-Agent", compiled_config["navigator.userAgent"]
            )

        # Note: in the normal launch path this runs before handle_locales()'
        # `locale:all` is merged in, so neither branch below fires and the
        # header is filled in by launch_options() instead (see utils.py).
        if "headers.Accept-Language" not in compiled_config:
            languages = compiled_config.get("navigator.languages")
            if isinstance(languages, (list, tuple)) and languages:
                compiled_config["headers.Accept-Language"] = (
                    self._accept_language_header(languages)
                )
            elif compiled_config.get("navigator.language"):
                compiled_config["headers.Accept-Language"] = compiled_config[
                    "navigator.language"
                ]

        compiled_config.setdefault("headers.Accept-Encoding", "gzip, deflate, br, zstd")

    @staticmethod
    def _accept_language_header(languages: Sequence[Any]) -> str:
        """Build Accept-Language the way Gecko builds it.

        Gecko spreads the q-values evenly over the list -- nsHttpHandler::
        PrepareAcceptLanguages() gives entry i of n the value 1 - i/n, rounded
        to one decimal (half away from zero). Measured against a stock
        Firefox 146 on the wire:

            de, en-US, en        -> de,en-US;q=0.7,en;q=0.3
            fr, de, en-US, en    -> fr,de;q=0.8,en-US;q=0.5,en;q=0.3
            en-US, en            -> en-US,en;q=0.5

        Camoufox was emitting a fixed 0.1 decrement (0.9, 0.8, 0.7 ...), which
        is Chrome's pattern, on every request from a browser announcing itself
        as Firefox. An earlier audit cleared this by reading a
        "emulate chrome behavior" comment in the netwerk rust helper; the
        comparison above against a real Firefox contradicts that reading, so
        the value is now derived rather than assumed. scripts/
        check_accept_languages.py already guards the language *list*; this is
        the weighting on top of it.
        """
        langs = [str(language) for language in languages if str(language)]
        if not langs:
            return ""
        count = len(langs)
        parts = [langs[0]]
        for index, lang in enumerate(langs[1:], start=1):
            # round half away from zero: Gecko emits 0.3 for 0.25, not 0.2
            q = max(0.1, math.floor((1.0 - index / count) * 10 + 0.5) / 10)
            parts.append(f"{lang};q={q:.1f}")
        # No space after the comma: Gecko emits "de,en-US;q=0.7,en;q=0.3".
        # Header whitespace is on the wire byte-for-byte, so ", " would be its
        # own small deviation even once the weights are right.
        return ",".join(parts)

    def _disable_webgl_null_blocking(self, compiled_config: Dict[str, Any]) -> None:
        """Prefer native WebGL fallbacks over nulling unknown parameters."""
        for key in (
            "webGl:parameters:blockIfNotDefined",
            "webGl2:parameters:blockIfNotDefined",
            "webGl:shaderPrecisionFormats:blockIfNotDefined",
            "webGl2:shaderPrecisionFormats:blockIfNotDefined",
        ):
            compiled_config[key] = False

    def _header_navigator_conflicts(
        self,
        *,
        compiled_config: Mapping[str, Any],
        user_config: Optional[Mapping[str, Any]],
    ) -> List[str]:
        """
        Catch the case where a user sets a request header that contradicts
        the navigator surface the engine compiled. Both are emitted from
        the same Firefox internal pref, so any mismatch is itself a
        fingerprint.
        """
        issues: List[str] = []
        user_config = user_config or {}

        ua_header = user_config.get("headers.User-Agent")
        ua_nav = compiled_config.get("navigator.userAgent")
        if ua_header and ua_nav and ua_header != ua_nav:
            issues.append(
                f"headers.User-Agent ({ua_header!r}) != navigator.userAgent ({ua_nav!r})"
            )

        al_header = user_config.get("headers.Accept-Language")
        nav_langs = compiled_config.get("navigator.languages")
        if al_header and isinstance(nav_langs, (list, tuple)) and nav_langs:
            # Accept-Language: "en-US,en;q=0.5" — first token before ',' or ';'
            primary = str(al_header).split(",", 1)[0].split(";", 1)[0].strip()
            if primary and primary != str(nav_langs[0]):
                issues.append(
                    f"headers.Accept-Language primary ({primary!r}) "
                    f"!= navigator.languages[0] ({nav_langs[0]!r})"
                )

        nav_lang = compiled_config.get("navigator.language")
        if al_header and nav_lang:
            primary = str(al_header).split(",", 1)[0].split(";", 1)[0].strip()
            if primary and primary != str(nav_lang):
                issues.append(
                    f"headers.Accept-Language primary ({primary!r}) "
                    f"!= navigator.language ({nav_lang!r})"
                )

        return issues


def _extract_subsystem(config: Mapping[str, Any], prefix: str) -> Dict[str, Any]:
    """Extract all keys with the given prefix into a sub-dictionary."""
    result: Dict[str, Any] = {}
    for key, value in config.items():
        if key.startswith(prefix):
            sub_key = key[len(prefix):]
            result[sub_key] = value
    return result


def to_identity_blob(state: IdentityState) -> Dict[str, Any]:
    """
    Serialize the complete IdentityState as a single nested JSON structure
    (the "IdentityBlob") covering all spoofed subsystems.

    This blob is the canonical "source of truth" that feeds CAMOU_CONFIG
    and can be round-tripped or inspected for debugging.
    """
    config = state.config

    # Navigator subsystem
    navigator_keys = (
        "userAgent", "appCodeName", "appName", "appVersion", "buildID",
        "language", "languages", "platform", "oscpu", "product",
        "productSub", "doNotTrack", "globalPrivacyControl",
        "hardwareConcurrency", "maxTouchPoints",
    )
    navigator_blob: Dict[str, Any] = {}
    for key in navigator_keys:
        full_key = f"navigator.{key}"
        if full_key in config:
            navigator_blob[key] = config[full_key]

    # Display subsystem (screen + window + document.body)
    display_blob: Dict[str, Any] = {
        "screen": {},
        "window": {},
        "documentBody": {},
    }
    for key, value in config.items():
        if key.startswith("screen."):
            display_blob["screen"][key.split(".", 1)[1]] = value
        elif key.startswith("window."):
            display_blob["window"][key.split(".", 1)[1]] = value
        elif key.startswith("document.body."):
            display_blob["documentBody"][key.split(".", 2)[2]] = value

    # WebGL subsystem
    webgl_blob: Dict[str, Any] = {}
    for key, value in config.items():
        if key.startswith("webGl:"):
            webgl_blob[key[6:]] = value
    webgl2_blob: Dict[str, Any] = {}
    for key, value in config.items():
        if key.startswith("webGl2:"):
            webgl2_blob[key[7:]] = value

    # Audio subsystem
    audio_blob: Dict[str, Any] = {}
    for key, value in config.items():
        if key.startswith("AudioContext:"):
            audio_blob[key[13:]] = value

    # Canvas subsystem
    canvas_blob: Dict[str, Any] = {}
    for key, value in config.items():
        if key.startswith("canvas:"):
            canvas_blob[key[7:]] = value

    # Font subsystem
    fonts_blob: Dict[str, Any] = {
        "list": config.get("fonts", []),
    }
    if "fonts:spacing_seed" in config:
        fonts_blob["spacing_seed"] = config["fonts:spacing_seed"]

    # Network subsystem
    network_blob: Dict[str, Any] = {}
    if state.network_profile:
        network_blob = state.network_profile.to_metadata()

    # Meta
    meta_blob: Dict[str, Any] = {
        "profile_id": state.profile_id,
        "seed": state.seed,
        "target_os": state.target_os,
        "performance_tier": state.device_profile.performance_tier,
        "coherence_issues": list(state.coherence_issues),
        "manual_overrides": list(state.manual_overrides),
    }

    return {
        "navigator": navigator_blob,
        "display": display_blob,
        "webgl": webgl_blob,
        "webgl2": webgl2_blob,
        "audio": audio_blob,
        "canvas": canvas_blob,
        "fonts": fonts_blob,
        "network": network_blob,
        "meta": meta_blob,
    }


def validate_identity_blob(blob: Dict[str, Any]) -> List[str]:
    """
    Cross-subsystem coherence validation on a serialized IdentityBlob.

    Returns a list of human-readable issue descriptions.
    Empty list means the blob is fully coherent.
    """
    issues: List[str] = []

    display = blob.get("display", {})
    screen = display.get("screen", {})
    window = display.get("window", {})
    webgl = blob.get("webgl", {})
    navigator = blob.get("navigator", {})
    audio = blob.get("audio", {})
    network = blob.get("network", {})

    # 1. WebGL MAX_VIEWPORT_DIMS must be >= screen resolution
    screen_width = screen.get("width")
    screen_height = screen.get("height")
    if screen_width and screen_height:
        # Check webgl parameters for MAX_VIEWPORT_DIMS (pname 3386 = 0x0D3A)
        params = webgl.get("parameters", {})
        viewport_dims = params.get("3386")
        if isinstance(viewport_dims, list) and len(viewport_dims) >= 2:
            if viewport_dims[0] < screen_width or viewport_dims[1] < screen_height:
                issues.append(
                    f"WebGL MAX_VIEWPORT_DIMS ({viewport_dims}) < screen "
                    f"resolution ({screen_width}x{screen_height})"
                )

    # 2. inner dimensions must be <= outer dimensions
    inner_w = window.get("innerWidth")
    inner_h = window.get("innerHeight")
    outer_w = window.get("outerWidth")
    outer_h = window.get("outerHeight")
    if inner_w and outer_w and inner_w > outer_w:
        issues.append(
            f"innerWidth ({inner_w}) > outerWidth ({outer_w})"
        )
    if inner_h and outer_h and inner_h > outer_h:
        issues.append(
            f"innerHeight ({inner_h}) > outerHeight ({outer_h})"
        )

    # 3. outer dimensions must be <= screen dimensions
    if outer_w and screen_width and outer_w > screen_width:
        issues.append(
            f"outerWidth ({outer_w}) > screen.width ({screen_width})"
        )
    if outer_h and screen_height and outer_h > screen_height:
        issues.append(
            f"outerHeight ({outer_h}) > screen.height ({screen_height})"
        )

    # 4. availWidth/availHeight should be <= screen width/height
    avail_w = screen.get("availWidth")
    avail_h = screen.get("availHeight")
    if avail_w and screen_width and avail_w > screen_width:
        issues.append(
            f"screen.availWidth ({avail_w}) > screen.width ({screen_width})"
        )
    if avail_h and screen_height and avail_h > screen_height:
        issues.append(
            f"screen.availHeight ({avail_h}) > screen.height ({screen_height})"
        )

    # 5. Audio sample rate must be a standard value (R7: calibrated set,
    #    shared with device_profiles.coherence.STANDARD_AUDIO_SAMPLE_RATES
    #    so the two validators agree and neither false-positives on
    #    32000 / 88200 / 176400 / 192000 hardware).
    sample_rate = audio.get("sampleRate")
    if sample_rate:
        try:
            from .device_profiles.coherence import STANDARD_AUDIO_SAMPLE_RATES
        except Exception:
            STANDARD_AUDIO_SAMPLE_RATES = (
                8000, 11025, 16000, 22050, 32000, 44100, 48000,
                88200, 96000, 176400, 192000,
            )
        if sample_rate not in STANDARD_AUDIO_SAMPLE_RATES:
            issues.append(
                f"Non-standard audio sample rate: {sample_rate}"
            )

    # 6. Network profile family must match navigator UA
    ua = navigator.get("userAgent", "")
    net_family = network.get("browser_family", "")
    if ua and net_family:
        ua_lower = ua.lower()
        if net_family == "firefox" and "firefox" not in ua_lower:
            issues.append(
                f"Network profile is '{net_family}' but UA does not contain 'firefox'"
            )
        elif net_family == "chrome" and "chrome" not in ua_lower:
            issues.append(
                f"Network profile is '{net_family}' but UA does not contain 'chrome'"
            )

    # 7. Canvas seed should be present when canvas is configured
    canvas = blob.get("canvas", {})
    if canvas.get("aaOffset") is not None and canvas.get("noiseSeed") is None:
        issues.append("Canvas aaOffset is configured without canvas noiseSeed")

    return issues
