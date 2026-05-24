from camoufox.device_profiles import build_font_list, sample_device_profile
from camoufox.identity import IdentityCoherenceEngine


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
