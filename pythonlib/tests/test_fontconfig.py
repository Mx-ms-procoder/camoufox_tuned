"""
Regression test for the Linux fontconfig wiring.

Before this, `get_env_vars` set FONTCONFIG_PATH to `<install>/fontconfig/<lin>`
while scripts/package.py ships `<install>/fontconfigs/<linux>`, and the shipped
fonts.conf pointed at `<dir prefix="cwd">fonts</dir>`. Both were wrong, so on
Linux fontconfig fell back to /etc/fonts and the bundled font set — the whole
point of the Linux bundle — was never used.
"""

import os

import pytest

from camoufox import utils


FONTS_CONF = (
    '<?xml version="1.0"?>\n'
    "<fontconfig>\n"
    '\t<dir prefix="cwd">fonts</dir>\n'
    "</fontconfig>\n"
)


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    """A fake Camoufox install laid out the way scripts/package.py ships it."""
    install = tmp_path / "install"
    (install / "fontconfigs" / "linux").mkdir(parents=True)
    (install / "fontconfigs" / "linux" / "fonts.conf").write_text(FONTS_CONF)
    (install / "fonts" / "linux").mkdir(parents=True)

    monkeypatch.setattr(utils, "get_path", lambda f: str(install / f))
    monkeypatch.setattr(utils, "INSTALL_DIR", tmp_path / "cache")
    return install


def test_resolves_the_fontconfigs_directory_and_absolute_font_dir(bundle):
    conf = utils._runtime_fontconfig("lin")

    assert os.path.exists(conf), "the runtime config must actually be written"
    content = open(conf, encoding="utf-8").read()
    assert 'prefix="cwd"' not in content, "relative font dir must be rewritten"
    assert f"<dir>{bundle / 'fonts'}</dir>" in content


def test_is_content_addressed_and_stable(bundle):
    assert utils._runtime_fontconfig("lin") == utils._runtime_fontconfig("lin")


def test_written_outside_the_browser_bundle(bundle):
    # The bundle is commonly baked into an image as root and run as non-root.
    assert not str(utils._runtime_fontconfig("lin")).startswith(str(bundle))


def test_incomplete_bundle_is_loud(bundle):
    (bundle / "fontconfigs" / "linux" / "fonts.conf").unlink()
    with pytest.raises(FileNotFoundError):
        utils._runtime_fontconfig("lin")
