#!/usr/bin/env python3
"""
fingerprint_parity/harness.py — diff Camoufox's runtime fingerprint
surface against a stock-Firefox baseline.

T3.4 (audit 2026-05-25): canvas/WebGL/audio spoofing claims need a
runtime check, not just a code review. This harness loads the
``probes.html`` page in a Camoufox instance, captures every probed
field, and compares the result against a pre-recorded baseline JSON
captured from stock Firefox 150.

Workflow
--------

1. Capture a stock-Firefox baseline (one-off, on a workstation with
   the same FF150 build the fork targets)::

       python -m tests.fingerprint_parity.harness \\
           --browser stock \\
           --executable /path/to/firefox-150.0.3/firefox \\
           --out baseline_stock_firefox_150.json

2. Run the parity check in CI or locally against Camoufox::

       python -m tests.fingerprint_parity.harness \\
           --browser camoufox \\
           --baseline baseline_stock_firefox_150.json

3. Exit code is 0 when only *expected* spoof fields drift (canvas
   sha256, audio sample rate noise, etc.) and 1 when an
   *unexpected* field drifts (e.g. WebGL extension list differs
   from FF150) — the latter is a real fingerprint surface that
   Camoufox is not maintaining parity on.

The "expected to drift" allowlist is conservative on purpose: every
field added here is one that anti-bot systems cannot use to tell
Camoufox from stock Firefox precisely *because* the engine
randomises it. New spoof targets should be added to the allowlist
when they ship; everything else is a regression.

The harness does not require both browsers on the same host — the
baseline is a JSON file that round-trips. CI typically only runs
step 2 (baseline is committed alongside the harness).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
PROBE_PAGE = HERE / "probes.html"
DEFAULT_BASELINE = HERE / "baseline_stock_firefox_150.json"

# Sentinel for baseline fields we do NOT yet have ground truth for. The
# committed FF150 baseline is partial (a full capture needs a running stock
# FF150 — see README): every runtime-dependent field is set to this marker
# instead of a fabricated placeholder. diff_probes() SKIPS such fields, so an
# incomplete baseline never produces false regressions. A real capture via
# `--out` overwrites these with concrete values and the checks light up.
CAPTURE_PENDING = "__CAPTURE_PENDING__"

# Fields where Camoufox is *expected* to differ from stock Firefox
# because the engine deliberately spoofs them. Format: dotted path
# from the root probe object (e.g. ``canvas.sha256``).
ALLOWED_DRIFT_FIELDS: Tuple[str, ...] = (
    # Canvas spoof: aaOffset + canvas:noiseSeed make the SHA differ.
    "canvas.sha256",
    "canvas.dataURL",
    "canvas.length",
    # Audio spoof: sampleRate/latency are sampled per identity.
    "audio.sampleRate",
    "audio.baseLatency",
    "audio.outputLatency",
    "audio.maxChannelCount",
    # Window metrics are operator-controlled.
    "window.innerWidth",
    "window.innerHeight",
    "window.outerWidth",
    "window.outerHeight",
    "screen.width",
    "screen.height",
    "screen.availWidth",
    "screen.availHeight",
    "screen.colorDepth",
    "screen.pixelDepth",
    "screen.devicePixelRatio",
    # Navigator surface is the whole point of the engine.
    "navigator.userAgent",
    "navigator.appVersion",
    "navigator.platform",
    "navigator.oscpu",
    "navigator.language",
    "navigator.languages",
    "navigator.hardwareConcurrency",
    "navigator.maxTouchPoints",
    # Intl follows locale, which the launcher sets.
    "intl.resolvedLocale",
    "intl.timeZone",
    # WebGL is spoofed (vendor/renderer + masked unmasked-vendor).
    "webgl.vendor",
    "webgl.renderer",
    "webgl.unmaskedVendor",
    "webgl.unmaskedRenderer",
    "webgl.maxTextureSize",
    "webgl.maxRenderbufferSize",
    "webgl.maxViewportDims",
)

# Fields whose absence/presence we tolerate: a missing key on either
# side just means the stock baseline was captured on a slightly
# different build. The harness treats "missing on one side" as a
# warning rather than a failure for these.
TOLERATE_MISSING: Tuple[str, ...] = (
    "navigator.oscpu",
    "navigator.pdfViewerEnabled",
    "webgl.unmaskedVendor",
    "webgl.unmaskedRenderer",
)


def _flatten(obj: Any, prefix: str = "") -> Dict[str, Any]:
    """Flatten ``{'a': {'b': 1}}`` into ``{'a.b': 1}``."""
    out: Dict[str, Any] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            out.update(_flatten(v, key))
    else:
        out[prefix] = obj
    return out


def diff_probes(
    captured: Dict[str, Any],
    baseline: Dict[str, Any],
    allowed: Tuple[str, ...] = ALLOWED_DRIFT_FIELDS,
    tolerated: Tuple[str, ...] = TOLERATE_MISSING,
) -> Tuple[List[str], List[str], List[str]]:
    """
    Return (regressions, allowed_drift, warnings).

    * regressions — same field, different value, NOT on the allowlist.
      Indicates a fingerprint surface Camoufox is no longer matching.
    * allowed_drift — same field, different value, on the allowlist.
      Reported for transparency but does not fail the run.
    * warnings — field present on one side but not the other (and not
      in TOLERATE_MISSING). Non-fatal.
    """
    flat_c = _flatten(captured)
    flat_b = _flatten(baseline)

    regressions: List[str] = []
    allowed_drift: List[str] = []
    warnings: List[str] = []

    all_keys = set(flat_c) | set(flat_b)
    for key in sorted(all_keys):
        # Ground truth not captured yet — skip rather than compare against a
        # placeholder (see CAPTURE_PENDING). This keeps a partial baseline
        # usable in CI without emitting spurious regressions.
        if flat_b.get(key) == CAPTURE_PENDING:
            continue
        if key not in flat_b:
            if key not in tolerated:
                warnings.append(f"only in captured: {key} = {flat_c[key]!r}")
            continue
        if key not in flat_c:
            if key not in tolerated:
                warnings.append(f"only in baseline: {key} = {flat_b[key]!r}")
            continue
        if flat_c[key] == flat_b[key]:
            continue
        line = f"{key}: captured={flat_c[key]!r} baseline={flat_b[key]!r}"
        if key in allowed:
            allowed_drift.append(line)
        else:
            regressions.append(line)
    return regressions, allowed_drift, warnings


def stealth_invariants(captured: Dict[str, Any]) -> List[str]:
    """Hard stealth assertions that should hold regardless of stock drift."""
    navigator = captured.get("navigator", {})
    issues: List[str] = []
    if navigator.get("webdriver") is not False:
        issues.append("navigator.webdriver must be false")
    if navigator.get("webdriverType") != "boolean":
        issues.append("typeof navigator.webdriver must be 'boolean'")
    if navigator.get("webdriverOnPrototype") is not True:
        issues.append("Navigator.prototype must retain the native webdriver getter")
    return issues


async def capture_probes(
    browser_kind: str,
    executable: Optional[str] = None,
    headless: bool = True,
) -> Dict[str, Any]:
    """
    Launch ``browser_kind`` ('camoufox' or 'stock'), load probes.html,
    and return the captured ``window.__fingerprintProbes`` object.
    """
    from playwright.async_api import async_playwright  # local import

    if browser_kind == "stock":
        from .stock_capture import capture
        if not executable:
            raise ValueError('--browser stock requires --executable pointing to official Firefox')
        return await asyncio.to_thread(capture, executable, PROBE_PAGE, headless)

    page_url = PROBE_PAGE.resolve().as_uri()

    async with async_playwright() as pw:
        if browser_kind == "camoufox":
            from camoufox.async_api import AsyncNewBrowser
            kwargs = {"headless": headless}
            if executable:
                kwargs["executable_path"] = executable
            browser = await AsyncNewBrowser(pw, **kwargs)
        else:
            raise ValueError(f"unknown browser kind: {browser_kind!r}")

        try:
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(page_url, wait_until="networkidle")
            # DOM is shared with the isolated automation world; page globals
            # are deliberately not. Read the serialized result through DOM.
            result = await page.wait_for_function(
                "() => { const t = document.getElementById('output').textContent; "
                "if (t.startsWith('ERR:')) throw new Error(t); "
                "return t.trim().startsWith('{') ? JSON.parse(t) : null; }",
                timeout=10_000,
            )
            data = await result.json_value()
            return data
        finally:
            await browser.close()


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--browser", choices=("camoufox", "stock"), required=True,
                   help="which browser to launch for capture")
    p.add_argument("--executable",
                   help="path to a Firefox or Camoufox binary")
    p.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE,
                   help="baseline JSON to diff against (default: alongside harness)")
    p.add_argument("--out", type=Path,
                   help="if set, write the captured probes here (use to refresh baseline)")
    p.add_argument("--headed", action="store_true",
                   help="open the browser window (default: headless)")
    p.add_argument("--json", action="store_true",
                   help="emit machine-readable JSON diff instead of text")
    p.add_argument("--require-complete-baseline", action="store_true",
                   help="fail if any reference field is still capture-pending")
    args = p.parse_args(argv)

    captured = asyncio.run(capture_probes(
        browser_kind=args.browser,
        executable=args.executable,
        headless=not args.headed,
    ))

    if args.out:
        args.out.write_text(
            json.dumps(captured, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {len(json.dumps(captured))} bytes to {args.out}")
        return 0

    if not args.baseline.exists():
        print(f"ERROR: baseline {args.baseline} not found. Run with --out to create it.",
              file=sys.stderr)
        return 2

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    pending = sorted(k for k, v in _flatten(baseline).items() if v == CAPTURE_PENDING)
    if pending and args.require_complete_baseline:
        print(f'ERROR: baseline has {len(pending)} uncaptured fields', file=sys.stderr)
        return 2
    regressions, allowed_drift, warnings = diff_probes(captured, baseline)
    if args.browser == "camoufox":
        regressions.extend(stealth_invariants(captured))
    if pending:
        print(
            f"NOTE: {len(pending)} baseline field(s) are capture-pending and "
            f"were skipped. Regenerate against a stock FF150 (--out) for full "
            f"coverage."
        )

    if args.json:
        json.dump({
            "regressions": regressions,
            "allowed_drift": allowed_drift,
            "warnings": warnings,
        }, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1 if regressions else 0

    if regressions:
        print(f"FAIL: {len(regressions)} unexpected fingerprint drift(s):")
        for r in regressions:
            print(f"  ✗ {r}")
    else:
        print("OK: no unexpected fingerprint drift.")

    if allowed_drift:
        print(f"\nallowlist drift ({len(allowed_drift)} field(s) — expected):")
        for r in allowed_drift[:10]:
            print(f"  · {r}")
        if len(allowed_drift) > 10:
            print(f"  · … {len(allowed_drift) - 10} more")

    if warnings:
        print(f"\nwarnings ({len(warnings)}):")
        for r in warnings[:5]:
            print(f"  ! {r}")
        if len(warnings) > 5:
            print(f"  ! … {len(warnings) - 5} more")

    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
