import pytest

from camoufox.device_profiles import build_font_list, sample_device_profile
from camoufox.identity import IdentityCoherenceEngine, _derive_seed_material


def test_sample_device_profile_is_os_coherent():
    profile = sample_device_profile("mac", webgl_enabled=False)

    assert profile.os_family == "mac"
    assert profile.device_pixel_ratio >= 1.5
    assert profile.platform == "MacIntel"
    assert profile.hardware_concurrency >= 4
    assert "Segoe UI" not in profile.fonts


def test_build_font_list_respects_custom_only():
    fonts = build_font_list("win", extra_fonts=["Fira Code"], custom_only=True)

    assert fonts == ["Fira Code"]


def test_identity_engine_produces_coherent_window_state():
    engine = IdentityCoherenceEngine()
    state = engine.build_from_base_config(
        base_config={
            "navigator.userAgent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) "
                "Gecko/20100101 Firefox/135.0"
            ),
            "window.outerWidth": 1512,
            "window.outerHeight": 982,
            "window.innerWidth": 1440,
            "window.innerHeight": 900,
            "screen.width": 1680,
            "screen.height": 1050,
        },
        target_os="mac",
        webgl_enabled=False,
    )

    assert state.config["screen.height"] >= state.config["window.outerHeight"]
    assert state.config["screen.width"] >= state.config["window.outerWidth"]
    assert state.config["window.outerWidth"] >= state.config["window.innerWidth"]
    assert state.config["window.outerHeight"] >= state.config["window.innerHeight"]
    assert state.config["document.body.clientWidth"] == state.config["window.innerWidth"]
    assert state.config["document.body.clientHeight"] == state.config["window.innerHeight"]
    assert state.config["fonts:spacing_seed"] >= 0
    assert -24 <= state.config["canvas:aaOffset"] <= 24
    assert state.config["mediaDevices:enabled"] is True
    assert state.config["mediaDevices:micros"] >= 1


def test_identity_engine_tracks_manual_override_conflicts():
    engine = IdentityCoherenceEngine()
    state = engine.build_from_base_config(
        base_config={
            "navigator.userAgent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) "
                "Gecko/20100101 Firefox/135.0"
            ),
            "screen.width": 1920,
            "screen.height": 1080,
        },
        target_os="win",
        user_config={"navigator.platform": "Linux x86_64"},
        webgl_enabled=False,
    )

    assert "navigator.platform" in state.manual_overrides


def test_identity_engine_matches_network_profile_to_effective_user_agent():
    engine = IdentityCoherenceEngine()
    state = engine.build_from_base_config(
        base_config={
            "navigator.userAgent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) "
                "Gecko/20100101 Firefox/135.0"
            ),
            "screen.width": 1920,
            "screen.height": 1080,
        },
        target_os="win",
        user_config={
            "navigator.userAgent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) "
                "Gecko/20100101 Firefox/150.0"
            )
        },
        webgl_enabled=False,
    )

    assert state.network_profile.major_version == 150


def _base_config_for_seed_test():
    return {
        "navigator.userAgent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) "
            "Gecko/20100101 Firefox/135.0"
        ),
        "screen.width": 1920,
        "screen.height": 1080,
    }


def test_fingerprint_seed_is_deterministic_across_runs():
    engine = IdentityCoherenceEngine()
    state_a = engine.build_from_base_config(
        base_config=_base_config_for_seed_test(),
        target_os="win",
        webgl_enabled=False,
        fingerprint_seed="my-persistent-seed",
    )
    state_b = engine.build_from_base_config(
        base_config=_base_config_for_seed_test(),
        target_os="win",
        webgl_enabled=False,
        fingerprint_seed="my-persistent-seed",
    )

    assert state_a.seed == state_b.seed
    assert state_a.profile_id == state_b.profile_id
    assert state_a.config["canvas:aaOffset"] == state_b.config["canvas:aaOffset"]
    assert state_a.config["fonts:spacing_seed"] == state_b.config["fonts:spacing_seed"]


def test_fingerprint_seed_differs_between_seeds():
    engine = IdentityCoherenceEngine()
    state_a = engine.build_from_base_config(
        base_config=_base_config_for_seed_test(),
        target_os="win",
        webgl_enabled=False,
        fingerprint_seed="seed-one",
    )
    state_b = engine.build_from_base_config(
        base_config=_base_config_for_seed_test(),
        target_os="win",
        webgl_enabled=False,
        fingerprint_seed="seed-two",
    )

    assert state_a.profile_id != state_b.profile_id


def test_fingerprint_seed_accepts_int_and_bytes():
    engine = IdentityCoherenceEngine()
    state_int = engine.build_from_base_config(
        base_config=_base_config_for_seed_test(),
        target_os="win",
        webgl_enabled=False,
        fingerprint_seed=42,
    )
    state_bytes = engine.build_from_base_config(
        base_config=_base_config_for_seed_test(),
        target_os="win",
        webgl_enabled=False,
        fingerprint_seed=b"\x2a",
    )

    # int and bytes hash differently — the int path zero-pads to 16 bytes
    # while bytes pass through verbatim. Same value, different encoding.
    assert state_int.profile_id != state_bytes.profile_id


def test_fingerprint_seed_rejects_bool():
    with pytest.raises(TypeError, match="must not be a bool"):
        _derive_seed_material(True)


def test_fingerprint_seed_rejects_unsupported_type():
    with pytest.raises(TypeError, match="must be str, int, or bytes"):
        _derive_seed_material(3.14)  # type: ignore[arg-type]


def test_fingerprint_seed_signed_int_roundtrip():
    # Negative ints must derive a distinct seed from their positive
    # counterpart; signed two's-complement gives them different bytes.
    assert _derive_seed_material(-1) != _derive_seed_material(1)
    assert _derive_seed_material(0) != _derive_seed_material(-1)


def test_fingerprint_seed_decouples_from_user_config():
    # Different base configs with the same seed should still resolve to
    # the same deterministic core identity (device profile, canvas
    # offset, font spacing). User-provided base_config still flows
    # through to merged output, but the random sampling is seed-driven.
    engine = IdentityCoherenceEngine()
    base_a = _base_config_for_seed_test()
    base_b = dict(base_a)
    base_b["screen.height"] = 1440  # change base config

    state_a = engine.build_from_base_config(
        base_config=base_a,
        target_os="win",
        webgl_enabled=False,
        fingerprint_seed="locked",
    )
    state_b = engine.build_from_base_config(
        base_config=base_b,
        target_os="win",
        webgl_enabled=False,
        fingerprint_seed="locked",
    )

    assert state_a.seed == state_b.seed
    assert state_a.config["canvas:aaOffset"] == state_b.config["canvas:aaOffset"]
    assert state_a.config["fonts:spacing_seed"] == state_b.config["fonts:spacing_seed"]
