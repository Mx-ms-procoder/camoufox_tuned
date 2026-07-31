"""The audio fingerprint has to move with the identity.

AudioFingerprintManager::GetSeed() reads the per-context storage key first and
falls back to MaskConfig "audio:seed". Nothing ever wrote either -- the runtime
setter that fed the storage key was removed with the window.set* island, and the
launcher never set the config key -- so the seed was 0 and ApplyTransformation()
early-returned. Measured on build015 across identities 1111/2222/3333, the
OfflineAudioContext fingerprint came out byte-identical every time while the
profiles claimed an NVIDIA Windows box, an Intel machine and an Apple M1: a hard
cross-profile link, and an internal contradiction on top.
"""
import json
import warnings

import pytest

from camoufox.utils import launch_options

SEEDS = [1111, 2222, 3333, "abc", 99999999]


def _config_for(seed):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        opts = launch_options(
            fingerprint_seed=seed, headless=True, humanize=True,
            i_know_what_im_doing=True,
        )
    path = opts["env"]["CAMOU_CONFIG_FILE"]
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.mark.parametrize("seed", SEEDS)
def test_audio_seed_is_set_and_usable(seed):
    cfg = _config_for(seed)
    value = cfg.get("audio:seed")
    assert value is not None, "audio:seed missing -> noise stays disabled"
    # GetSeed() treats 0 as "unset", and MaskConfig reads it as uint32.
    assert isinstance(value, int)
    assert 0 < value <= 0xFFFFFFFF


def test_audio_seed_differs_between_identities():
    values = [_config_for(s)["audio:seed"] for s in SEEDS]
    assert len(set(values)) == len(values), (
        f"identities share an audio seed -> shared audio fingerprint: {values}"
    )


def test_audio_seed_is_stable_for_one_identity():
    a = _config_for(4242)["audio:seed"]
    b = _config_for(4242)["audio:seed"]
    assert a == b, "the same seed must reproduce the same audio fingerprint"


def test_audio_seed_independent_of_canvas_seed():
    """Both derive from the same digest; they must not collide into one value."""
    cfg = _config_for(777)
    assert cfg["audio:seed"] != cfg["canvas:noiseSeed"]
