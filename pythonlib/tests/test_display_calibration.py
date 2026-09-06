from types import SimpleNamespace
from camoufox.device_profiles.coherence import _panel_exists, _dpr_os, COHERENCE_RULES, coherence_hints


def test_rotated_panel_and_linux_scaling_are_accepted():
    portrait = SimpleNamespace(screen_width=1080, screen_height=1920,
                               device_pixel_ratio=1, os_family='lin')
    assert _panel_exists(portrait)
    portrait.device_pixel_ratio = 4
    assert _dpr_os(portrait)


def test_unknown_panel_is_only_a_calibration_hint():
    profile = SimpleNamespace(screen_width=4567, screen_height=2345,
                              device_pixel_ratio=1, os_family='lin', gpu_renderer='llvmpipe')
    assert _panel_exists not in [rule for _, rule in COHERENCE_RULES]
    assert len(coherence_hints(profile)) == 2
