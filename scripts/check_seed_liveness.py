#!/usr/bin/env python3
"""Catch dead spoofing paths: surfaces that ignore the fingerprint seed.

The same defect has now shipped three times in this repo -- canvas noise,
WebRTC IP spoofing and audio noise. Each time the C++ side read a config key
that nothing ever wrote, so the layer silently did nothing: no exception, no
log line, every test still green, and the observable value byte-identical
across identities that claimed completely different hardware. Each was found
by accident, months apart.

All three would have been caught the first day by one question:

    if I change the seed, does the observable value change?

That is what this does. It launches the browser once per seed, reads each
fingerprint surface *as a page sees it* -- never the config that was meant to
drive it, since the whole failure mode is config that reaches nothing -- and
flags any surface that comes back identical for every identity. It also
re-runs the first seed to confirm the surface is stable when the seed does not
change, because a value that varies run-to-run is not a working spoof either,
it is noise that breaks profile persistence.

Two failure modes, opposite directions:

  DEAD    same value for every seed          -> the spoof is not wired up
  UNSTABLE different value for the same seed -> not reproducible

Exits non-zero if any surface is either. Needs a working browser, so it is a
scripts/ check rather than a unit test.

Run it against a browser built from THIS tree. Several surfaces are spoofed by
C++ patches, so pointing it at an upstream or older package reports those as
DEAD when the only thing missing is the patch -- e.g. speech.voices comes back
empty on stock 152.0.4-beta.27, which ships without media/voice-spoofing.patch.
Confirm any DEAD result by checking whether the config carries the key
(launch_options -> CAMOU_CONFIG_FILE): config written + page empty is a real
dead path, config missing is a launcher bug, and neither is a browser bug if
the consuming patch is not in the build under test.

Usage:
    python scripts/check_seed_liveness.py [--seeds N] [--headful] [-v]
"""

import argparse
import sys
from collections import defaultdict

try:
    from camoufox.sync_api import Camoufox
except ImportError:  # pragma: no cover
    sys.exit("camoufox pythonlib not importable -- run from the repo root")


# Each probe returns a value that must differ between identities. Keep them
# cheap and synchronous; anything needing a real network round-trip belongs in
# the acceptance harness, not here.
PROBES = {
    # --- the three that shipped dead ---
    "canvas.toDataURL": """() => {
        const c = document.createElement('canvas'); c.width = 220; c.height = 60;
        const x = c.getContext('2d');
        x.textBaseline = 'top'; x.font = '14px Arial';
        x.fillStyle = '#f60'; x.fillRect(10, 5, 180, 30);
        x.fillStyle = '#069'; x.fillText('Camoufox canvas 42', 12, 10);
        x.strokeStyle = 'rgba(0,80,200,0.6)'; x.arc(60, 30, 25, 0, Math.PI * 2); x.stroke();
        return c.toDataURL();
    }""",
    "canvas.getImageData": """() => {
        const c = document.createElement('canvas'); c.width = 64; c.height = 64;
        const x = c.getContext('2d');
        x.fillStyle = '#3a7'; x.fillRect(0, 0, 64, 64);
        x.fillStyle = '#d21'; x.fillText('seed', 4, 32);
        const d = x.getImageData(0, 0, 64, 64).data;
        let h = 0;
        for (let i = 0; i < d.length; i++) h = ((h * 31) + d[i]) >>> 0;
        return String(h);
    }""",
    # Summed inside a page-injected <script> rather than in the evaluate
    # callback: Playwright evaluates behind an Xray wrapper, and reading
    # getChannelData()'s Float32Array element-by-element through one throws
    # "Accessing TypedArray data over Xrays is slow, and forbidden". The
    # reduction has to happen in the content scope; only the string comes back.
    "audio.offlineContext": """async () => {
        const out = document.createElement('div');
        out.id = 'camou-audio-probe';
        document.documentElement.appendChild(out);
        const s = document.createElement('script');
        s.textContent = `(async () => {
            const el = document.getElementById('camou-audio-probe');
            try {
                const ctx = new OfflineAudioContext(1, 5000, 44100);
                const osc = ctx.createOscillator();
                osc.type = 'triangle'; osc.frequency.value = 10000;
                const comp = ctx.createDynamicsCompressor();
                osc.connect(comp); comp.connect(ctx.destination);
                osc.start(0);
                const buf = await ctx.startRendering();
                const ch = buf.getChannelData(0);
                let sum = 0;
                for (let i = 0; i < ch.length; i++) sum += Math.abs(ch[i]);
                el.textContent = sum.toFixed(12);
            } catch (e) { el.textContent = 'ERROR:' + e.name; }
        })();`;
        document.documentElement.appendChild(s);
        for (let i = 0; i < 100 && !out.textContent; i++)
            await new Promise(r => setTimeout(r, 50));
        return out.textContent || 'ERROR:timeout';
    }""",
    # --- other surfaces that are supposed to be identity-bound ---
    "webgl.renderer": """() => {
        const gl = document.createElement('canvas').getContext('webgl');
        if (!gl) return 'NO_WEBGL';
        const e = gl.getExtension('WEBGL_debug_renderer_info');
        return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) + '|' +
                   gl.getParameter(e.UNMASKED_VENDOR_WEBGL) : 'NO_EXT';
    }""",
    "webgl.readback": """() => {
        const c = document.createElement('canvas'); c.width = 32; c.height = 32;
        const gl = c.getContext('webgl');
        if (!gl) return 'NO_WEBGL';
        gl.clearColor(0.25, 0.5, 0.75, 1); gl.clear(gl.COLOR_BUFFER_BIT);
        const px = new Uint8Array(32 * 32 * 4);
        gl.readPixels(0, 0, 32, 32, gl.RGBA, gl.UNSIGNED_BYTE, px);
        let h = 0;
        for (let i = 0; i < px.length; i++) h = ((h * 31) + px[i]) >>> 0;
        return String(h);
    }""",
    "navigator.userAgent": "() => navigator.userAgent",
    "navigator.hardwareConcurrency": "() => String(navigator.hardwareConcurrency)",
    "screen.metrics": "() => [screen.width, screen.height, screen.availWidth, "
                      "screen.availHeight, devicePixelRatio].join('x')",
    "window.metrics": "() => [innerWidth, innerHeight, outerWidth, outerHeight].join('x')",
    "fonts.textMetrics": """() => {
        const x = document.createElement('canvas').getContext('2d');
        const out = [];
        for (const f of ['12px Arial', '14px Georgia', '16px "Times New Roman"',
                         '13px Verdana', '15px Tahoma']) {
            x.font = f;
            out.push(x.measureText('MMMMMMMMMMlliii...WWW').width.toFixed(4));
        }
        return out.join(',');
    }""",
    # getVoices() is populated asynchronously and returns [] before the list
    # lands -- an earlier audit already chased that empty array as a leak and
    # found it was the measurement, not the browser. Wait for voiceschanged.
    "speech.voices": """async () => {
        let v = speechSynthesis.getVoices();
        if (!v.length) {
            await new Promise(resolve => {
                const done = () => resolve();
                speechSynthesis.addEventListener('voiceschanged', done, {once: true});
                setTimeout(done, 3000);
            });
            v = speechSynthesis.getVoices();
        }
        return v.length ? v.map(o => o.name + ':' + o.lang).sort().join('|') : 'EMPTY';
    }""",
    "prefersColorScheme": "() => matchMedia('(prefers-color-scheme: dark)').matches "
                          "? 'dark' : 'light'",
}

# Surfaces that legitimately repeat across identities often enough that a small
# sample proves nothing. They are still measured and reported, just not failed
# on: the value space is small, so collisions are expected rather than dead.
LOW_CARDINALITY = {
    "navigator.hardwareConcurrency",  # a handful of plausible core counts
    "prefersColorScheme",             # two values by definition
    "webgl.renderer",                 # small pool of plausible GPUs
}

# Config keys that are written by the launcher and read by C++, but whose
# effect on the page is checked separately by holding the identity fixed and
# varying only that key. A seed sweep cannot see these because several keys
# move at once. Each entry is (config key, values to try, probe name).
SINGLE_KEY_PROBES = [
    # daijro/camoufox#421 asks for float instead of int here. Measured inert:
    # with the identity pinned, -20/0/7/24 all give the same canvas output,
    # while varying canvas:noiseSeed does change it. GetCanvasState() is only
    # consumed by the diagnostic blob; canvas-noise.patch reads noiseSeed only.
    ("canvas:aaOffset", [-20, 0, 7, 24], "canvas.getImageData"),
]


def measure(seed, headless, verbose):
    """Read every probe under one identity."""
    results = {}
    with Camoufox(headless=headless, fingerprint_seed=seed,
                  i_know_what_im_doing=True) as browser:
        page = browser.new_page()
        page.goto("data:text/html,<body>seed-liveness</body>")
        # getVoices() populates asynchronously
        page.wait_for_timeout(500)
        for name, js in PROBES.items():
            try:
                value = page.evaluate(js)
            except Exception as exc:
                value = f"ERROR:{type(exc).__name__}"
            results[name] = str(value)
            if verbose:
                shown = results[name]
                if len(shown) > 70:
                    shown = shown[:67] + "..."
                print(f"    {name:32} {shown}")
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seeds", type=int, default=3,
                    help="distinct identities to compare (default 3)")
    ap.add_argument("--headful", action="store_true", help="run headful")
    ap.add_argument("-v", "--verbose", action="store_true", help="print every value")
    args = ap.parse_args()

    if args.seeds < 2:
        sys.exit("need at least 2 seeds to compare")

    seeds = [f"liveness-{i}" for i in range(args.seeds)]
    headless = not args.headful

    by_probe = defaultdict(list)
    for seed in seeds:
        print(f"  measuring seed {seed!r} ...")
        for name, value in measure(seed, headless, args.verbose).items():
            by_probe[name].append(value)

    # Re-run the first seed: same seed must reproduce the same values.
    print(f"  re-measuring seed {seeds[0]!r} for stability ...")
    repeat = measure(seeds[0], headless, args.verbose)

    # Single-key sweeps: identity pinned, one config key varied.
    single_key = []
    for key, values, probe in SINGLE_KEY_PROBES:
        seen = set()
        for value in values:
            with Camoufox(headless=headless, fingerprint_seed=seeds[0],
                          i_know_what_im_doing=True, config={key: value}) as browser:
                page = browser.new_page()
                page.goto("data:text/html,<body>seed-liveness</body>")
                try:
                    seen.add(str(page.evaluate(PROBES[probe])))
                except Exception as exc:
                    seen.add(f"ERROR:{type(exc).__name__}")
        single_key.append((key, probe, len(values), len(seen)))
        print(f"  single-key {key}: {len(seen)} distinct {probe} over "
              f"{len(values)} values")

    dead, unstable, errored, ok = [], [], [], []
    for name, values in by_probe.items():
        if values[0].startswith("ERROR:") or values[0] in ("NO_WEBGL", "NO_EXT"):
            errored.append((name, values[0]))
            continue
        if repeat[name] != values[0]:
            unstable.append(name)
        elif len(set(values)) == 1:
            (ok if name in LOW_CARDINALITY else dead).append(name)
        else:
            ok.append(name)

    print()
    for name in sorted(ok):
        note = " (low-cardinality, not failed on)" if name in LOW_CARDINALITY else ""
        print(f"  OK       {name}{note}")
    for name, why in sorted(errored):
        print(f"  SKIP     {name}: {why}")
    for name in sorted(dead):
        print(f"  DEAD     {name}: identical across all {len(seeds)} seeds")
    for name in sorted(unstable):
        print(f"  UNSTABLE {name}: same seed produced a different value")

    for key, probe, n_values, n_distinct in single_key:
        if n_distinct <= 1:
            print(f"  INERT    {key}: {n_values} different values, one {probe} result")
        else:
            print(f"  OK       {key}: affects {probe}")

    print(f"\n{len(ok)} ok, {len(dead)} dead, {len(unstable)} unstable, "
          f"{len(errored)} skipped, "
          f"{sum(1 for _k, _p, _v, d in single_key if d <= 1)} inert key(s)")

    if dead or unstable:
        print("\nA DEAD surface means the spoof is not reaching the page -- the "
              "config key is\nprobably read by C++ but never written, the failure "
              "mode that shipped three\ntimes already. An UNSTABLE surface breaks "
              "profile persistence.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
