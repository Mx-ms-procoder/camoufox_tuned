"""The WebGL renderer must be possible on the OS the identity claims.

ANGLE is Chrome's GL-over-Direct3D translator and Direct3D is a Windows API,
so either token under a macOS or Linux user agent contradicts that user agent
in a way any page can check in one line.

This is not hypothetical: the shipped webgl_data.db carries two rows where an
`ANGLE (NVIDIA, ... Direct3D11 ...)` renderer has a non-zero macOS weight
(0.004, against 0.22 for Windows) -- almost certainly a misparsed user agent in
the upstream data. Out of only six macOS rows that was enough to hand roughly
one macOS identity in fifteen a Windows GPU string.
"""
import pytest

from camoufox.webgl.sample import sample_webgl

WINDOWS_ONLY = ("ANGLE (", "Direct3D", "D3D11")


@pytest.mark.parametrize("os_family", ["mac", "lin"])
def test_no_windows_renderer_on_other_platforms(os_family):
    for seed in range(300):
        state = sample_webgl(os_family, seed=seed)
        renderer = state.get("webGl:renderer", "")
        for token in WINDOWS_ONLY:
            assert token.lower() not in renderer.lower(), (
                f"{os_family} identity (seed {seed}) got a Windows-only "
                f"renderer: {renderer}"
            )


def test_windows_still_gets_angle():
    """The filter must not strip Windows' own renderers."""
    seen = {sample_webgl("win", seed=s).get("webGl:renderer", "") for s in range(60)}
    assert any("ANGLE" in r for r in seen), seen


@pytest.mark.parametrize("os_family", ["win", "mac", "lin"])
def test_pool_never_filtered_empty(os_family):
    """Every OS must still yield a usable renderer."""
    state = sample_webgl(os_family, seed=1)
    assert state.get("webGl:renderer")
    assert state.get("webGl:vendor")
