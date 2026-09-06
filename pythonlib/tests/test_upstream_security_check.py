"""Regression coverage for the security monitor's false all-clear (2026-09-05)."""
import importlib.util
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("camoufox_security_check", REPO / "scripts/check_upstream_security.py")
monitor = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = monitor
spec.loader.exec_module(monitor)

CURRENT = '''<h2>September  1, 2026</h2><ul>
<li><a href="/en-US/security/advisories/mfsa2026-82/"><span class="level high">MFSA 2026-82</span> Security Vulnerabilities fixed in Firefox 155</a></li>
<li><a href="/en-US/security/advisories/mfsa2026-67/"><span>MFSA 2026-67</span> Security Vulnerabilities fixed in Firefox 152.0.6</a></li>
<li><a href="/en-US/security/advisories/mfsa2026-85/"><span>MFSA 2026-85</span> Security Vulnerabilities fixed in Firefox ESR 999.0</a></li>
<li><a href="/en-US/security/advisories/mfsa2026-81/"><span>MFSA 2026-81</span> Security fixes for Firefox for iOS 999.0</a></li>
<li><a href="/en-US/security/advisories/mfsa2026-86/"><span>MFSA 2026-86</span> Security fixes for Thunderbird 999</a></li>
</ul>'''

def test_current_layout_extracts_desktop_versions_and_dates():
    records = monitor.parse_mfsa_index(CURRENT)
    assert [str(r.highest_firefox) for r in records] == ["155.0.0", "152.0.6"]
    assert records[0].date == "September 1, 2026"

def test_major_version_and_suffix_parsing():
    assert monitor.FirefoxVersion.parse("155").as_tuple() == (155, 0, 0)
    assert monitor.FirefoxVersion.parse("152.0.4-beta.27").as_tuple() == (152, 0, 4)
    assert monitor.FirefoxVersion.parse("140.15.0esr").as_tuple() == (140, 15, 0)
    assert monitor.FirefoxVersion.parse("155.bad") is None

def test_historical_table_layout():
    rows = monitor.parse_mfsa_index('<tr><td><a href="/en-US/security/advisories/mfsa2026-67/">MFSA 2026-67</a></td><td>July 14, 2026</td><td>Firefox 152.0.6, Firefox ESR 140.12</td></tr>')
    assert str(rows[0].highest_firefox) == "152.0.6"

def run_cli(monkeypatch, html):
    monkeypatch.setattr(monitor, "fetch_mfsa_index", lambda **kwargs: html)
    monkeypatch.setattr(monitor, "read_pinned_version", lambda path: monitor.FirefoxVersion(152, 0, 4))
    return monitor.main(["--json"])

def test_drift_is_failure(monkeypatch, capsys):
    assert run_cli(monkeypatch, CURRENT) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "outdated"
    assert result["newer_major_advisories"][0]["id"] == "2026-82"
    assert result["newer_advisories"][0]["id"] == "2026-67"

def test_empty_and_redesigned_response_is_unknown(monkeypatch, capsys):
    for html in ["", "<h1>Temporary maintenance</h1>"]:
        assert run_cli(monkeypatch, html) == 2
        assert json.loads(capsys.readouterr().out)["status"] == "error"

def test_network_failure_is_not_all_clear(monkeypatch, capsys):
    def fail(**kwargs): raise OSError("offline")
    monkeypatch.setattr(monitor, "fetch_mfsa_index", fail)
    assert monitor.main(["--json"]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "error"

def test_equal_release_is_current(monkeypatch, capsys):
    html = '<h2>July 3, 2026</h2><a href="/en-US/security/advisories/mfsa2026-62/">MFSA 2026-62 Security Vulnerabilities fixed in Firefox 152.0.4</a>'
    assert run_cli(monkeypatch, html) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "ok"
