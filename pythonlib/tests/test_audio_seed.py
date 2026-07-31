"""The audio fingerprint has to move with the identity.

AudioFingerprintManager::GetSeed() reads the per-context storage key first and
falls back to MaskConfig "audio:seed". Nothing ever wrote either -- the runtime
setter that fed the storage key was removed with the window.set* island, and the
launcher never set the config key -- so the seed was 0 and ApplyTransformation()
early-returned. Measured on build015 across identities 1111/2222/3333, the
OfflineAudioContext fingerprint came out byte-identical every time while the
profiles claimed an NVIDIA Windows box, an Intel machine and an Apple M1: a hard
cross-profile link, and an internal contradiction on top.

Goes through IdentityCoherenceEngine rather than launch_options(): the latter
runs validate_config(), which loads properties.json out of the *installed*
browser via pkgman.get_path(). CI has no matching install, so that path fails
there for reasons that have nothing to do with what this file is testing.
"""
import pytest

from camoufox.identity import IdentityCoherenceEngine

SEEDS = [1111, 2222, 3333, "abc", 99999999]


def _base_config():
    return {
        "navigator.userAgent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) "
            "Gecko/20100101 Firefox/152.0"
        ),
        "screen.width": 1920,
        "screen.height": 1080,
    }


def _config_for(seed):
    engine = IdentityCoherenceEngine()
    state = engine.build_from_base_config(
        base_config=_base_config(),
        target_os="win",
        webgl_enabled=False,
        fingerprint_seed=seed,
    )
    return state.config


@pytest.mark.parametrize("seed", SEEDS)
def test_audio_seed_is_set_and_usable(seed):
    value = _config_for(seed).get("audio:seed")
    assert value is not None, "audio:seed missing -> noise stays disabled"
    # GetSeed() treats 0 as "unset", and MaskConfig reads it as uint32.
    assert isinstance(value, int) and not isinstance(value, bool)
    assert 0 < value <= 0xFFFFFFFF


def test_audio_seed_differs_between_identities():
    values = [_config_for(s)["audio:seed"] for s in SEEDS]
    assert len(set(values)) == len(values), (
        f"identities share an audio seed -> shared audio fingerprint: {values}"
    )


def test_audio_seed_is_stable_for_one_identity():
    assert _config_for(4242)["audio:seed"] == _config_for(4242)["audio:seed"], (
        "the same seed must reproduce the same audio fingerprint"
    )


def test_audio_seed_independent_of_canvas_seed():
    """Both derive from the same digest; they must not collide into one value."""
    cfg = _config_for(777)
    assert cfg["audio:seed"] != cfg["canvas:noiseSeed"]


def test_scroll_offsets_are_not_pinned():
    """screen.pageXOffset/pageYOffset must not be emitted at all.

    GetScrollX/GetScrollY return the configured value *instead of* the live
    scroll position, so emitting them froze window.scrollY at 0 for the whole
    session while the page really scrolled.
    """
    cfg = _config_for(555)
    assert "screen.pageXOffset" not in cfg
    assert "screen.pageYOffset" not in cfg
