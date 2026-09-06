"""Recheck the reproduced audit failures against an unpacked release binary.

Run from the repository root:
python tests/release_smoke.py /path/to/camoufox.exe --out /path/to/results
All browser profiles and network endpoints used by the probes are disposable.
"""
import argparse
import asyncio
import importlib.util
import json
from pathlib import Path


async def main(executable: str, out: Path):
    root = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location(
        'audit_runtime', root / 'audits/2026-09-05/run_runtime_probes.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out.mkdir(parents=True, exist_ok=True)
    evidence = await module.main(executable, out / 'runtime-results.json', '155.0')
    checks = []

    def check(name, actual, expected, seed):
        checks.append({'name': name, 'seed': seed, 'passed': actual == expected,
                       'actual': actual, 'expected': expected})

    for run in evidence['runs']:
        seed = run['seed']
        check('browser launch and context creation', run.get('error'), None, seed)
        if run.get('error'):
            continue
        data = run.get('result') or {}
        check('probe completed', bool(data) and not data.get('error'), True, seed)
        if not data or data.get('error'):
            continue
        audio, gl = data.get('audio', {}), data.get('webgl', {})
        check('AudioBuffer offset consistency', audio.get('offsetMismatches'), 0, seed)
        check('AudioBuffer full/slice consistency', audio.get('fullSliceMatchesAfter'), True, seed)
        check('WebGL error-free', gl.get('error'), 0, seed)
        check('WebGL direct/PBO consistency', gl.get('directPboMismatches'), 0, seed)
        check('WebGL zero-size write preservation', gl.get('zeroSizeWrites'), 0, seed)
        check('WebGL pack-region preservation', gl.get('packWritesOutsideRequestedRectangle'), 0, seed)
        check('WebGL identical redraw stable', gl.get('directHash') == gl.get('identicalRedrawHash')
              and bool(gl.get('directHash')), True, seed)
        check('screen/CSS consistency', data.get('screen', {}).get('cssWidth'), True, seed)
        check('main-world init script', data.get('initMarker'), 'present', seed)
        check('main-world init after navigation', run.get('navigation_init_marker'), 'present', seed)
        check('native animation duration', data.get('animation', {}).get('computed'), 1000, seed)
        nav, worker = data.get('navigator', {}), data.get('worker', {})
        check('webdriver native boolean', nav.get('webdriverType'), 'boolean', seed)
        check('webdriver property present', nav.get('webdriverIn'), True, seed)
        check('no writable persona setters', nav.get('setters'), [], seed)
        for key in ('userAgent', 'platform', 'hardwareConcurrency', 'language', 'languages'):
            check(f'worker/window {key}', worker.get(key), nav.get(key), seed)
        check('worker timezone', worker.get('timezone'), 'Europe/Berlin', seed)
        check('worker winter offset', worker.get('offset'), -60, seed)
        locale = data.get('locale', {})
        check('summer offset', locale.get('julyOffset'), -120, seed)
        check('explicit Japanese locale', locale.get('explicitJapanese', {}).get('locale'), 'ja-JP', seed)
        check('WebRTC local offer accepted', data.get('webrtc', {}).get('localOfferAccepted'), True, seed)
        for name, headers in [('request', data.get('headers', {})), ('routed request', run.get('routed_headers', {}))]:
            headers = {k.lower(): v for k, v in headers.items()}
            check(f'{name} User-Agent', headers.get('user-agent'), nav.get('userAgent'), seed)
            check(f'{name} first Accept-Language', (headers.get('accept-language') or '').split(',')[0], 'de', seed)

    for section, field in [('webgl', 'directHash'), ('canvas', 'hash'), ('audio', 'afterHash')]:
        values = [(r.get('result') or {}).get(section, {}).get(field) for r in evidence['runs']]
        check(f'{section} seeds produce distinct output',
              len(set(v for v in values if v is not None)), 3, 'across seeds')
    failed = [c for c in checks if not c['passed']]
    summary = {'checks': checks, 'passed': len(checks) - len(failed), 'failed': len(failed),
               'binary_sha256': evidence['executable_sha256']}
    (out / 'smoke-summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': summary['passed'], 'failures': failed}, indent=2))
    return bool(failed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('executable')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.executable, args.out)))
