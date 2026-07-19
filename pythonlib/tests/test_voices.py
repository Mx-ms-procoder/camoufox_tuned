"""Voice-generation tests: shape MaskConfig::MVoices() requires, determinism,
per-OS URI backends, and locale-coherent default."""
from random import Random

from camoufox.voices import generate_voices

_FIELDS = {'lang', 'name', 'voiceUri', 'isDefault', 'isLocalService'}


def test_mvoices_object_shape():
    for tos in ('macos', 'windows', 'linux', 'win', 'mac', 'lin'):
        voices = generate_voices(tos, 'en-US', Random(7))
        assert voices, f'{tos} produced no voices'
        for v in voices:
            assert _FIELDS <= set(v), f'{tos} voice missing MVoices fields: {v}'


def test_seeded_selection_is_reproducible():
    a = generate_voices('macos', 'en-US', Random(42))
    b = generate_voices('macos', 'en-US', Random(42))
    assert a == b


def test_exactly_one_default():
    for tos in ('macos', 'windows', 'linux'):
        voices = generate_voices(tos, 'en-US', Random(1))
        assert sum(v['isDefault'] for v in voices) == 1


def test_default_prefers_locale_prefix():
    voices = generate_voices('linux', 'de-DE', Random(1))
    default = next(v for v in voices if v['isDefault'])
    assert default['lang'].lower().startswith('de')


def test_per_os_uri_backends():
    assert all(v['voiceUri'].startswith('urn:moz-tts:sapi:')
               for v in generate_voices('windows', 'en-US', Random(1)))
    assert all(v['voiceUri'].startswith('urn:moz-tts:osx:')
               for v in generate_voices('macos', 'en-US', Random(1)))
    assert all(v['voiceUri'].startswith('urn:moz-tts:speechd:')
               for v in generate_voices('linux', 'en-US', Random(1)))


def test_short_and_long_os_keys_agree():
    # The coherence engine passes 'win'/'mac'/'lin'; a mismatch must not silently
    # fall back to another OS's voice list (the bug this guards against).
    assert generate_voices('win', 'en-US', Random(3)) == \
        generate_voices('windows', 'en-US', Random(3))


def test_windows_ships_full_fixed_list():
    # SAPI list is fixed across installs — subsetting it would read as suspicious.
    assert len(generate_voices('windows', 'en-US', Random(9))) == 53
