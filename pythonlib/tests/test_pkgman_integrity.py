"""Installer failures must never discard the last usable browser."""
import hashlib
import io
from pathlib import Path
from zipfile import ZipFile

import pytest

from camoufox import pkgman


def fetcher(monkeypatch, tmp_path, *, corrupt=False, fail_download=False):
    monkeypatch.setattr(pkgman, 'INSTALL_DIR', tmp_path / 'browser')
    monkeypatch.setattr(pkgman, 'OS_NAME', 'win')
    old = pkgman.INSTALL_DIR
    old.mkdir()
    (old / 'camoufox.exe').write_bytes(b'old working browser')
    data = io.BytesIO()
    with ZipFile(data, 'w') as archive:
        archive.writestr('camoufox.exe', b'new browser')
    payload = data.getvalue()
    f = object.__new__(pkgman.CamoufoxFetcher)
    f.github_repo = pkgman.DEFAULT_RELEASE_REPOSITORY
    f._url = 'https://github.com/' + f.github_repo + '/releases/download/build-0.21/test.zip'
    f._sha256 = '0' * 64 if corrupt else hashlib.sha256(payload).hexdigest()
    f._version_obj = pkgman.Version('beta.31', '155.0.1')

    def download(file, url):
        if fail_download:
            raise OSError('interrupted download')
        file.write(payload)
        file.seek(0)
        return file

    monkeypatch.setattr(f, 'download_file', download)
    return f, old


@pytest.mark.parametrize('failure', ['digest', 'network'])
def test_failed_download_preserves_installation(monkeypatch, tmp_path, failure):
    f, old = fetcher(monkeypatch, tmp_path, corrupt=failure == 'digest',
                     fail_download=failure == 'network')
    with pytest.raises(OSError):
        f.install()
    assert (old / 'camoufox.exe').read_bytes() == b'old working browser'
    assert not list(tmp_path.glob('.camoufox-install-*'))


def test_success_replaces_only_after_verification(monkeypatch, tmp_path):
    f, old = fetcher(monkeypatch, tmp_path)
    f.install()
    assert (old / 'camoufox.exe').read_bytes() == b'new browser'
    assert pkgman.Version.from_path(old).full_string == '155.0.1-beta.31'
    assert f._sha256 in (old / 'download.json').read_text()
    assert not list(tmp_path.glob('.camoufox-install-*'))


def test_commit_failure_rolls_back(monkeypatch, tmp_path):
    f, old = fetcher(monkeypatch, tmp_path)
    rename = Path.rename

    def fail_new(self, target):
        if self.name == 'new':
            raise OSError('commit failed')
        return rename(self, target)

    monkeypatch.setattr(Path, 'rename', fail_new)
    with pytest.raises(OSError, match='commit failed'):
        f.install()
    assert (old / 'camoufox.exe').read_bytes() == b'old working browser'


def test_asset_requires_digest_and_exact_name(monkeypatch):
    monkeypatch.setattr(pkgman.CamoufoxFetcher, 'fetch_latest', lambda self: None)
    f = pkgman.CamoufoxFetcher()
    assert f.github_repo == 'Mx-ms-procoder/camoufox_tuned'
    asset = {'name': f'camoufox-155.0.1-beta.31-{pkgman.OS_NAME}.{f.arch}.zip',
             'browser_download_url': f'https://github.com/{f.github_repo}/releases/download/build-0.21/browser.zip'}
    with pytest.raises(pkgman.MissingRelease, match='digest'):
        f.check_asset(asset)
    asset['digest'] = 'sha256:' + 'a' * 64
    assert f.check_asset(asset)[2] == 'a' * 64
    asset['name'] += '.untrusted'
    assert f.check_asset(asset) is None


def test_bad_repository_cannot_change_download_host():
    with pytest.raises(ValueError):
        pkgman.CamoufoxFetcher('../unexpected/owner')


def test_install_lock_excludes_concurrent_commit_and_recovers(tmp_path):
    path = tmp_path / '.camoufox-install.lock'
    with pytest.raises(RuntimeError, match='interrupted'):
        with pkgman._installation_lock(path):
            with pytest.raises(OSError):
                with pkgman._installation_lock(path):
                    pytest.fail('a second installer obtained the lock')
            raise RuntimeError('interrupted')
    with pkgman._installation_lock(path):
        assert path.is_file()
