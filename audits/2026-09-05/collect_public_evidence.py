"""Fetch public primary-source evidence; never imports or launches the browser."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import urllib.request

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE / 'evidence'
OUT.mkdir(exist_ok=True)

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Camoufox-local-security-audit/1'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()

def evidence(item):
    name, url = item
    try:
        raw = fetch(url)
        (OUT / name).write_bytes(raw)
        return {'file': name, 'url': url, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    except Exception as error:
        return {'file': name, 'url': url, 'error': str(error)}

urls = [
    ('mozilla-advisories.html', 'https://www.mozilla.org/en-US/security/advisories/'),
    ('firefox-versions.json', 'https://product-details.mozilla.org/1.0/firefox_versions.json'),
    ('mfsa2026-68.html', 'https://www.mozilla.org/en-US/security/advisories/mfsa2026-68/'),
    ('mfsa2026-74.html', 'https://www.mozilla.org/en-US/security/advisories/mfsa2026-74/'),
    ('mfsa2026-67.html', 'https://www.mozilla.org/en-US/security/advisories/mfsa2026-67/'),
    ('mfsa2026-82.html', 'https://www.mozilla.org/en-US/security/advisories/mfsa2026-82/'),
]
for name in ['ClientWebGLContext.cpp', 'CanvasRenderingContext2D.cpp', 'OffscreenCanvas.cpp']:
    urls.append(('gecko152-' + name, 'https://hg.mozilla.org/releases/mozilla-release/raw-file/FIREFOX_152_0_4_RELEASE/dom/canvas/' + name))
urls.append(('gecko152-AudioBuffer.cpp', 'https://hg.mozilla.org/releases/mozilla-release/raw-file/FIREFOX_152_0_4_RELEASE/dom/media/webaudio/AudioBuffer.cpp'))
urls.append(('gecko152-nsMediaFeatures.cpp', 'https://hg.mozilla.org/releases/mozilla-release/raw-file/FIREFOX_152_0_4_RELEASE/layout/style/nsMediaFeatures.cpp'))

pins = re.findall(r'^([a-zA-Z0-9_.-]+)(?:\[[^\]]*\])?==([^\s;\\]+)', (REPO / 'requirements.lock').read_text(), re.M)
def package_check(pin):
    name, version = pin
    url = f'https://pypi.org/pypi/{name}/{version}/json'
    try:
        obj = json.loads(fetch(url))
        return {'name': name, 'version': version, 'url': url, 'vulnerabilities': obj.get('vulnerabilities', [])}
    except Exception as error:
        return {'name': name, 'version': version, 'url': url, 'error': str(error)}

with ThreadPoolExecutor(max_workers=8) as pool:
    manifest = list(pool.map(evidence, urls))
    packages = list(pool.map(package_check, pins))
(OUT / 'public-fetch-manifest.json').write_text(json.dumps({'retrieved_at': datetime.now(timezone.utc).isoformat(), 'sources': manifest}, indent=2), encoding='utf-8')
(OUT / 'dependency-advisories.json').write_text(json.dumps(packages, indent=2), encoding='utf-8')
print(json.dumps({'sources': manifest, 'packages_checked': len(packages), 'vulnerable_packages': [p['name'] for p in packages if p.get('vulnerabilities')], 'errors': [p for p in packages if p.get('error')]}, indent=2))
