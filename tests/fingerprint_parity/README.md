# Fingerprint Parity Harness

Runtime check that diffs Camoufox's exposed fingerprint surface
against a captured stock Firefox 150 baseline.

Added per audit T3.4 (2026-05-25): canvas/WebGL spoof claims are
empirically unverified until something actually loads the engine in
a real browser and looks at what `navigator`, `WebGLRenderingContext`,
`AudioContext`, `Intl`, and the canvas data URL produce.

## Files

- `harness.py` — captures probes, diffs against a baseline, exits
  non-zero on unexpected drift.
- `probes.html` — static page with deterministic JS that reads every
  fingerprint surface the engine claims to spoof or pass through.
- `baseline_stock_firefox_150.json` — reference values from a stock
  Firefox 150 install. **Currently PARTIAL** — see *Baseline status*
  and *Refreshing the baseline* below.

## Baseline status (Mittel-2)

A full baseline needs a live stock-FF150 capture, which this
environment can't produce. Rather than ship fabricated placeholder
numbers (which silently caused **false regressions** on non-allowlisted
fields like `webgl.extensions`, `webgl.version`, `plugins.length` and
`audio.state`), every runtime-dependent field is set to the sentinel
`"__CAPTURE_PENDING__"`. `harness.diff_probes()` **skips** any field whose
baseline value is that sentinel, so a partial baseline is safe to run in
CI — it can only fail on a field we actually have ground truth for.

Only three fields are asserted concretely, because they are hard,
source-verifiable facts for stock FF150 that Camoufox must also satisfy:

| field | value | why |
| ----- | ----- | --- |
| `navigator.webdriver` | `false` | stock and Camoufox both report false |
| `navigator.cookieEnabled` | `true` | default in both |
| `navigator.pdfViewerEnabled` | `true` | pdf.js enabled (camoufox.cfg keeps `pdfjs.disabled=false`) |

The native WebDriver shape is present: a boolean value and a prototype
property, with `false` in an ordinary unautomated browser. The independent
`harness.stealth_invariants()` checks expect that shape. Removing the property
would itself differ from ordinary Firefox.

The historical Firefox 150 reference remains partial. Pass
`--require-complete-baseline` to fail closed when fields are uncaptured.
A green comparison with skipped fields does not establish full parity.

## What counts as a regression

Fields listed in `ALLOWED_DRIFT_FIELDS` in `harness.py` may differ —
those are surfaces the engine deliberately spoofs (canvas hash,
audio sample rate noise, navigator UA, screen metrics, WebGL
vendor / renderer, etc.). Fields set to `"__CAPTURE_PENDING__"` in the
baseline are skipped entirely. Anything **outside** the allowlist that
differs *and* has a concrete (non-sentinel) baseline value is a parity
gap: Camoufox is now reachable through a fingerprint vector that stock
Firefox 150 does not expose, or vice versa. The harness exits 1 in that
case.

## Running the parity check

```bash
# From the repo root, with Camoufox + Playwright installed:
python -m tests.fingerprint_parity.harness \
    --browser camoufox \
    --baseline tests/fingerprint_parity/baseline_stock_firefox_150.json
```

## Refreshing the baseline

The baseline JSON shipped with the harness is a schema-shaped
placeholder. Regenerate it on a workstation with official Firefox 155.0.1
installed:

```bash
python -m tests.fingerprint_parity.harness \
    --browser stock \
    --executable /opt/firefox-155.0.1/firefox \
    --out tests/fingerprint_parity/baseline_stock_firefox_155.json
```

Stock capture uses a temporary profile and a loopback server. Official Firefox
does not provide Playwright's Juggler endpoint. The page posts its results to
the local collector; no patched browser is substituted for the reference.
Camoufox capture reads through the shared DOM, since Juggler's isolated world
does not share page globals. `--executable` also accepts a Camoufox binary.

Record the official binary hash, OS, GPU and headless/headed mode with each
reference. Hardware-dependent fields are not a universal Firefox fingerprint.
Commit the resulting JSON. Re-capture every time `upstream.sh` is
bumped to a new Firefox version (the `check_upstream_security.py`
job will tell you when that happens).

## CI wiring

This harness is not yet wired into `.github/workflows/build.yml`
because it requires a working Camoufox binary (which the apply-check
+ build matrix produces, but only on a successful build job). The
practical place to add it is after the build matrix, as a smoke test
on the resulting `camoufox-bin` — that requires more infra than this
audit pass touched. See the *Structural items still open* section of
`AUDIT_2026-05-18.md`.
