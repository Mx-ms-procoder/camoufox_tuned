"""
CAPTCHA Master-Scanner v9 — multi-frame + early-inject reliability fixes.

EXPERIMENTAL — see scripts_macros/captcha/__init__.py and K-19 in
AUDIT_2026-05-18.md. Selectors target third-party sites that change
frequently; treat this scanner as a starting point, not a contract.

Changes vs. v8 (Chrome-Reliability):
  * scan_page() iterates ALL page.frames (not just main_frame). Chrome's
    Site Isolation puts each cross-origin frame in its own process; the
    previous single-frame evaluate missed reCAPTCHA/hCaptcha/Turnstile
    that live in their own iframes.
  * _inject_observer() walks every frame too, so the GeeTest triad
    observer is installed in sub-frames as well.
  * live_scan() calls context.add_init_script(JS_INJECT_OBSERVERS) so
    the observer runs at document_start on every frame BEFORE the page's
    own JavaScript executes — fixes the race where late-loaded captchas
    mounted before our scanner was installed.
  * live_scan() now hooks page.on("response") on captcha-related URLs
    (CAPTCHA_URL_HINTS) and triggers a delayed re-scan. Catches XHR-
    lazy-mounted captchas that DOM-MutationObserver would only see after
    the mount completes.
  * live_scan() hooks page.on("framenavigated") + page.on("load") for
    re-scans on navigation events.
  * auto_solve_captcha() uses a declarative _SOLVER_ROUTES registry
    instead of the brittle if/elif name-substring chain.
  * Three new providers: DataDome, AWS WAF CAPTCHA, Yandex SmartCaptcha.

Changes in v8 (retained):
  * TikTok refactored into three provider classes
    (Rotate / Slide / 3D Objects) with a shared container helper and
    cross-type negative filters.

Camoufox usage — recommended (uses convenience helpers):
    import os, asyncio
    os.environ["CAMOUFOX_ENABLE_CAPTCHA"] = "1"  # MUST be set before import
    from scripts_macros.captcha import scanner

    # (a) One-shot scan + auto-solve, blocks until Ctrl-C:
    asyncio.run(scanner.run_with_camoufox(
        "https://accounts.google.com",
        headless=False,
        # any additional Camoufox launch kwarg (proxy, locale, …)
    ))

    # (b) Pure one-shot scan (sync, returns results immediately):
    results = scanner.scan_with_camoufox_sync(
        "https://example.com/page-with-captcha",
        headless=False,
    )
    for cap in results:
        print(cap["name"], "solved:", cap.get("solved"))

Camoufox usage — manual (if you already have a context):
    import os
    os.environ["CAMOUFOX_ENABLE_CAPTCHA"] = "1"
    from playwright.async_api import async_playwright
    from camoufox.async_api import AsyncNewBrowser
    from scripts_macros.captcha import scanner

    async def main():
        async with async_playwright() as pw:
            browser = await AsyncNewBrowser(pw, headless=False)
            context = await browser.new_context()
            page    = await context.new_page()
            await page.goto("https://example.com")

            # One-shot multi-frame scan:
            results = await scanner.scan_page(page)

            # Or continuous monitoring (blocks; run as task if needed):
            await scanner.live_scan(context, auto_solve=True)

    asyncio.run(main())

Legacy CDP path (Chrome-only, broken on Camoufox/Firefox — Juggler ≠ CDP):
    Not supported. live_scan_cdp() is a no-op stub kept only for import
    compatibility with old callers.

Requires:  pip install playwright camoufox  (camoufox optional if you use
           the manual flow with raw Playwright Firefox)
"""

from __future__ import annotations

import sys
import os
import time
import json
import secrets
import asyncio
import urllib.request
from datetime import datetime
from typing import Any, Callable, Optional
from weakref import WeakKeyDictionary

# ══════════════════════════════════════════════════════════════════
#  Configuration
# ══════════════════════════════════════════════════════════════════

CDP_PORT         = int(os.environ.get("CDP_PORT", 9222))
CDP_HOST         = os.environ.get("CDP_HOST", "127.0.0.1")
SCAN_INTERVAL    = 15.0
CDP_RECV_TIMEOUT = 6
CDP_RECV_RETRIES = 10

# Internal: tracks which pages already have the observer injected
# (page_id -> URL).
_observer_injected: WeakKeyDictionary[Any, str] = WeakKeyDictionary()


# ══════════════════════════════════════════════════════════════════
#  Per-page marker randomization (T1.1 / T1.5 / R1 / R3)
# ══════════════════════════════════════════════════════════════════
#
# Previously the scanner used fixed marker names — window.__CSI_KEY__,
# window.__INJECTED_KEY__ — plus a Playwright expose_binding() callback
# on window (__REPORT_BINDING__) and a hard-coded 800 ms debounce. Any
# page that enumerated window properties or pattern-matched against
# those constants could detect the automation harness in a single line,
# and the bound function was a textbook Playwright tell.
#
# Now: (R3) each *page* gets its own random window-property names and a
# random console-channel prefix, sampled lazily in _markers_for_page, so
# no marker is a process-wide or cross-page constant; and (R1) newly
# detected captchas are reported over console.debug(prefix + json),
# parsed by a page.on("console") listener — nothing is bound onto
# window. The MutationObserver debounce is also resampled per render.

def _gen_marker() -> str:
    # Underscore prefix keeps the name a legal JS identifier; 16 hex
    # chars (64 bits) is enough entropy that bruteforce-enumeration
    # against window is not a credible discovery path.
    return "_" + secrets.token_hex(8)


def _new_marker_set() -> dict:
    """Generate a fresh, unique set of JS markers for ONE page.

    `csi` / `injected` are window-property names; `report` is the
    console-message prefix used by the detection channel (see
    _on_console in live_scan). Giving every page its own set means the
    automation surface is never a process-wide constant that two pages
    — or two colluding sites in the same process — could correlate on
    (R3: per-page markers instead of per-process).
    """
    return {
        "csi": _gen_marker(),
        "injected": _gen_marker(),
        # Console-message prefix for the reporting channel (R1). Not a
        # window property, so it does not need to be a JS identifier;
        # the trailing ':' keeps Python-side prefix matching unambiguous.
        "report": _gen_marker() + ":",
    }


# Per-page marker store. WeakKeyDictionary so entries vanish when the
# page is garbage-collected — no manual cleanup, no leak.
_page_markers: "WeakKeyDictionary[Any, dict]" = WeakKeyDictionary()


def _markers_for_page(page) -> dict:
    """Return the marker set bound to `page`, creating one on first use."""
    m = _page_markers.get(page)
    if m is None:
        m = _new_marker_set()
        try:
            _page_markers[page] = m
        except TypeError:
            # Page not weak-referenceable (shouldn't happen for real
            # Playwright pages) — fall back to a fresh per-call set.
            pass
    return m


def _regenerate_session_markers() -> None:
    """Deprecated no-op kept for import stability.

    Markers used to be process-global and this rotated them between
    runs. They are now per-page (see _markers_for_page), so rotation is
    automatic and this does nothing. golden_flow.py still imports it.
    """
    return None


def _render(template: str, markers: dict) -> str:
    """Substitute marker / debounce placeholders in a JS template.

    `markers` is a per-page set from _markers_for_page() so that
    `__CSI_KEY__` / `__INJECTED_KEY__` (window properties) and
    `__REPORT_PREFIX__` (console-channel prefix) are unique per page.
    Phase-1 inject and Phase-2 scan for the same page resolve markers
    from the same page object, so they always agree. `__SCAN_DEBOUNCE_MS__`
    is sampled per render in [600, 1000] so the MutationObserver timing
    is not a constant fingerprint either.
    """
    debounce_ms = 600 + secrets.randbelow(401)
    return (template
        .replace("__CSI_KEY__", markers["csi"])
        .replace("__INJECTED_KEY__", markers["injected"])
        .replace("__REPORT_PREFIX__", markers["report"])
        .replace("__SCAN_DEBOUNCE_MS__", str(debounce_ms)))


# ══════════════════════════════════════════════════════════════════
#  Phase 1: observer injection (once per page/URL)
# ══════════════════════════════════════════════════════════════════

JS_INJECT_OBSERVERS = r"""
(function() {
if (window.__CSI_KEY__) return "already_injected";

window.__CSI_KEY__ = {
    geetest: { solved: false, ts: 0, challenge: "", validate: "", seccode: "" },
};

function checkGeeTestTriad() {
    const c = document.querySelector('input[name="geetest_challenge"]');
    const v = document.querySelector('input[name="geetest_validate"]');
    const s = document.querySelector('input[name="geetest_seccode"]');
    if (c && v && s && c.value && v.value && s.value) {
        window.__CSI_KEY__.geetest = {
            solved: true, ts: Date.now(),
            challenge: c.value, validate: v.value, seccode: s.value,
        };
    } else if (window.__CSI_KEY__.geetest.solved && !(c || v || s)) {
        window.__CSI_KEY__.geetest = { solved: false, ts: 0, challenge: "", validate: "", seccode: "" };
    }
}

const obs = new MutationObserver(() => {
    checkGeeTestTriad();
});
obs.observe(document.documentElement, {
    childList: true, subtree: true,
});

checkGeeTestTriad();

return "injected";
})();
"""


# ══════════════════════════════════════════════════════════════════
#  Phase 2: deep scan (runs once per scan interval)
# ══════════════════════════════════════════════════════════════════

JS_DEEP_SCAN = r"""
(function() {
"use strict";

// ════════════════════════════════════════
//  UTILITY
// ════════════════════════════════════════

function isVisible(el) {
    if (!el) return false;
    try {
        const s = window.getComputedStyle(el);
        if (s.display === "none" || s.visibility === "hidden") return false;
        if (parseFloat(s.opacity) < 0.05) return false;
        if (el.getAttribute("aria-hidden") === "true") return false;
        const r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
    } catch(e) { return true; }
}

function deepQuery(root, sel) {
    try { const el = root.querySelector(sel); if (el) return el; } catch(e) {}
    try {
        for (const el of root.querySelectorAll("*")) {
            if (el.shadowRoot) { const f = deepQuery(el.shadowRoot, sel); if (f) return f; }
        }
    } catch(e) {}
    return null;
}

function deepQueryVisible(root, sel) {
    try { for (const el of root.querySelectorAll(sel)) { if (isVisible(el)) return el; } } catch(e) {}
    try {
        for (const el of root.querySelectorAll("*")) {
            if (el.shadowRoot) { const f = deepQueryVisible(el.shadowRoot, sel); if (f) return f; }
        }
    } catch(e) {}
    return null;
}

function collectDocs(win, depth) {
    // Recursion depth bumped from 1 to 4 so deeply-nested captcha
    // iframes (e.g. Cloudflare Turnstile inside an ad iframe inside a
    // login modal iframe) are reachable from this JS-side deep scan.
    // The Python-side find_selector_in_frames() iterates page.frames
    // with no depth limit; keeping the two sides aligned avoids
    // false-negatives where the Python solver could reach a captcha
    // that the JS detector missed. 4 is a safety cap against
    // pathological frame trees and same-origin recursive iframes.
    if (depth > 4) return [];
    let docs = [];
    try { if (win.document) docs.push(win.document); } catch(e) {}
    try {
        for (let i = 0; i < win.frames.length; i++) {
            try { docs = docs.concat(collectDocs(win.frames[i], depth + 1)); } catch(e) {}
        }
    } catch(e) {}
    return docs;
}

// ── Einmalige Datensammlung ──────────────────────────────────────

var allDocs = [];
var iframeSrcs = [];
var scriptSrcs = [];
var allText = "";
let currentPath = "";
let currentHostname = "";

function updateGlobals() {
    allDocs = collectDocs(window, 0);
    iframeSrcs = [];
    scriptSrcs = [];
    allText = document.body ? document.body.textContent.toLowerCase() : "";
    for (const doc of allDocs) {
        try {
            for (const fr of doc.querySelectorAll("iframe[src]")) {
                const s = (fr.src || "").toLowerCase();
                if (s) iframeSrcs.push(s);
            }
            for (const s of doc.querySelectorAll("script[src]")) {
                const src = (s.src || "").toLowerCase();
                if (src) scriptSrcs.push(src);
            }
        } catch(e) {}
    }
    currentPath = window.location.pathname.toLowerCase();
    currentHostname = window.location.hostname.toLowerCase();
}

const iframeHas     = p  => iframeSrcs.some(s => s.includes(p));
const scriptHas     = p  => scriptSrcs.some(s => s.includes(p));
// Regex-Prüfung auf Iframe-URLs verhindert Substring-Fehlmatches
const iframeMatchRe = re => iframeSrcs.some(s => re.test(s));

// Observer-State (von Phase 1 injiziert)
const csi = window.__CSI_KEY__ || {
    geetest: { solved: false },
};


// ════════════════════════════════════════
//  BASE PROVIDER
// ════════════════════════════════════════

class CaptchaProvider {
    constructor(name) { this.name = name; }
    detect() { return null; }
    result(extra) {
        return { name: this.name, solved: false, description: "", ...extra };
    }
}


// ════════════════════════════════════════
//  PROVIDER: Microsoft HIP / Press & Hold
//  Priorität 1 – muss VOR FunCaptcha laufen
// ════════════════════════════════════════

class MicrosoftHIPProvider extends CaptchaProvider {
    constructor() { super("Microsoft HIP"); }

    detect() {
        const hasMsIframe = ["challenges.microsoft.com","client.hip.live.com","account.microsoft.com/captcha"]
            .some(d => iframeHas(d));

        let hasMsDOM = false;
        for (const doc of allDocs) {
            for (const sel of ["#hipTemplateDiv","#captchaContainer",".atsl-captcha",
                               "div[data-ms-captcha]","#HipImgContainer","#hipImageInput"]) {
                if (deepQuery(doc, sel)) { hasMsDOM = true; break; }
            }
            if (hasMsDOM) break;
        }

        const msPhrases = ["halten sie die schaltfläche","press and hold",
                           "zugängliche herausforderung","hipaction","hip.live.com","hiptemplatediv"];
        const docText = document.body ? document.body.textContent.toLowerCase() : "";
        const hasMsText = msPhrases.some(p => docText.includes(p));

        const onMsDomain = /\.(microsoft|live|microsoftonline|xbox)\.com$/.test(currentHostname);
        const hasMsCaptchaText = ["lassen sie uns beweisen, dass sie menschlich sind",
                                  "prove you're not a robot","menschlich sind"]
            .some(t => docText.includes(t));

        if (!hasMsIframe && !hasMsDOM && !hasMsText && !(onMsDomain && hasMsCaptchaText)) return null;

        let subtype = "HIP";
        if (docText.includes("halten sie die schaltfläche") || docText.includes("press and hold")) {
            subtype = "Press & Hold";
        } else if (hasMsDOM && deepQuery(allDocs[0], "#HipImgContainer")) {
            subtype = "Bild-CAPTCHA";
        }

        return this.result({
            name: `Microsoft HIP – ${subtype}`,
            description: `Microsoft HIP CAPTCHA – Variante: ${subtype}.\n  ➜ Schaltfläche halten bis 100%.`,
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: reCAPTCHA v3 / Invisible
// ════════════════════════════════════════

class ReCaptchaV3Provider extends CaptchaProvider {
    constructor() { super("reCAPTCHA v3 / Invisible"); }

    detect() {
        let hasGrecaptchaHTML = false;
        try { hasGrecaptchaHTML = document.documentElement.outerHTML.includes("grecaptcha.execute("); } catch(e) {}
        const hasV3Script =
            scriptHas("recaptcha/api.js?render=") ||
            scriptHas("recaptcha.net/recaptcha/api.js?render=") ||
            hasGrecaptchaHTML;

        let hasBadge = false;
        for (const doc of allDocs) {
            if (deepQueryVisible(doc, ".grecaptcha-badge")) { hasBadge = true; break; }
        }
        if (!hasV3Script && !hasBadge) return null;

        // v3 zurückziehen wenn v2-Anchor sichtbar
        for (const doc of allDocs) {
            if (deepQuery(doc, "#recaptcha-anchor, .rc-anchor-container")) return null;
        }
        return this.result({
            description: "reCAPTCHA v3 / Invisible – Score-basiert, läuft im Hintergrund.",
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: reCAPTCHA v2
//  Dreistufige Erkennungs-Hierarchie:
//    [A] Iframe von google.com/recaptcha/(api2|enterprise)/ oder recaptcha.net
//        → Regex-Prüfung verhindert Substring-Matches auf falschen Domains
//    [B] #recaptcha-anchor / .rc-anchor-container im DOM
//        → erscheinen nur in echten reCAPTCHA-Frames
//    [C] .g-recaptcha[data-sitekey] mit Google-Sitekey-Präfix "6L" + Script
//        → hCaptcha nutzt manchmal g-recaptcha-Klasse → expliziter Ausschluss
//  Negativfilter: Fake-CAPTCHA-Sites (Win+R Malware)
// ════════════════════════════════════════

class ReCaptchaV2Provider extends CaptchaProvider {
    constructor() { super("reCAPTCHA v2"); }

    detect() {
        const FAKE = ["win + r","windows + r","ctrl + v","press windows",
                      "paste into run","paste in run","type into run","open run dialog","winkey + r"];
        const docText = document.body ? document.body.textContent.toLowerCase() : "";
        if (FAKE.some(s => docText.includes(s))) return null;

        // [A] Authentischer Google-Iframe (exakter Pfad-Regex)
        const IFRAME_RE = /\/(google\.com|recaptcha\.net)\/recaptcha\/(api2|enterprise)\//;
        const hasAuthoritativeIframe = iframeMatchRe(IFRAME_RE);

        // [B] Anchor-Element (entsteht nur in echten reCAPTCHA-Frames)
        let hasAnchor = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, "#recaptcha-anchor") || deepQuery(doc, ".rc-anchor-container")) {
                hasAnchor = true; break;
            }
        }

        // [C] Div mit verifiziertem Sitekey + reCAPTCHA-Script
        let divWithValidSitekey = false;
        const hCaptchaPresent = iframeHas("hcaptcha.com") || scriptHas("hcaptcha.com");
        if (!hCaptchaPresent) {
            const hasRcScript = scriptHas("google.com/recaptcha/api.js") ||
                                scriptHas("recaptcha.net/recaptcha/api.js");
            if (hasRcScript) {
                for (const doc of allDocs) {
                    const divs = doc.querySelectorAll
                        ? doc.querySelectorAll(".g-recaptcha[data-sitekey]") : [];
                    for (const div of divs) {
                        if ((div.getAttribute("data-sitekey") || "").startsWith("6L") && isVisible(div)) {
                            divWithValidSitekey = true; break;
                        }
                    }
                    if (divWithValidSitekey) break;
                }
            }
        }

        if (!hasAuthoritativeIframe && !hasAnchor && !divWithValidSitekey) return null;

        let solved = false;
        for (const doc of allDocs) {
            const anchor = deepQuery(doc, "#recaptcha-anchor");
            if (anchor?.getAttribute("aria-checked") === "true") { solved = true; break; }
            const resp = deepQuery(doc, "textarea[name='g-recaptcha-response']");
            if (resp?.value?.length > 20) { solved = true; break; }
        }

        return this.result({
            solved,
            description: "reCAPTCHA v2 – Checkbox oder Bild-Rätsel (Google).\n  ➜ Checkbox klicken; bei Rätsel alle passenden Felder auswählen.",
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: hCaptcha
// ════════════════════════════════════════

class HCaptchaProvider extends CaptchaProvider {
    constructor() { super("hCaptcha"); }

    detect() {
        const hasHCIframe = iframeHas("hcaptcha.com");
        const hasHCScript = scriptHas("hcaptcha.com/1/api.js") || scriptHas("js.hcaptcha.com");
        let hasHCDiv = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, ".h-captcha[data-sitekey]") ||
                deepQuery(doc, "div[data-hcaptcha-widget-id]")) { hasHCDiv = true; break; }
        }
        if (!hasHCIframe && !hasHCScript && !hasHCDiv) return null;

        let solved = false;
        for (const doc of allDocs) {
            const r = deepQuery(doc, "textarea[name='h-captcha-response']");
            if (r?.value?.length > 20) { solved = true; break; }
        }
        return this.result({
            solved,
            description: "hCaptcha – Checkbox oder Bild-Rätsel.\n  ➜ Checkbox klicken → Bild-Rätsel lösen.",
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: Cloudflare Turnstile
// ════════════════════════════════════════

class TurnstileProvider extends CaptchaProvider {
    constructor() { super("Cloudflare Turnstile"); }

    detect() {
        const hasTsIframe = iframeHas("challenges.cloudflare.com/turnstile");
        const hasTsScript = scriptHas("challenges.cloudflare.com/turnstile");
        let hasTsDiv = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, ".cf-turnstile, div[data-cf-turnstile]")) { hasTsDiv = true; break; }
        }
        if (!hasTsIframe && !hasTsScript && !hasTsDiv) return null;

        let solved = false;
        for (const doc of allDocs) {
            const r = deepQuery(doc, "input[name='cf-turnstile-response']");
            if (r?.value?.length > 20) { solved = true; break; }
        }
        return this.result({
            solved,
            description: "Cloudflare Turnstile – Verhaltensbasiertes Widget.",
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: Cloudflare Challenge (klassisch)
// ════════════════════════════════════════

class CfChallengeProvider extends CaptchaProvider {
    constructor() { super("Cloudflare Challenge"); }

    detect() {
        let found = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, "div#challenge-form, form[action*='__cf_chl'], #challenge-running, #challenge-spinner")) {
                found = true; break;
            }
        }
        if (!found) return null;
        return this.result({
            description: "Cloudflare Security Challenge.\n  ➜ Kurz warten – löst sich meist von selbst.",
        });
    }
}


// ArkoseProvider (FunCaptcha) entfernt – nicht mehr unterstützt.


// ════════════════════════════════════════════════════════════════════
//  TIKTOK CAPTCHA – Drei vollständig getrennte Provider
//
//  Mechanismus-Überblick:
//
//  ┌─────────────────────────────────────────────────────────────┐
//  │ Typ           │ Struktur                  │ Interaktion     │
//  ├─────────────────────────────────────────────────────────────┤
//  │ Rotate        │ Zwei konzentrische Bilder │ Slider → Drehen │
//  │               │ (inner + outer, kreisförmig)│               │
//  ├─────────────────────────────────────────────────────────────┤
//  │ Puzzle Slide  │ Puzzleteil + Hintergrund  │ Slider → Ziehen │
//  │               │ mit Lücke (rechteckig)    │                 │
//  ├─────────────────────────────────────────────────────────────┤
//  │ 3D Objects    │ Ein Bild mit 3D-Objekten  │ Direkte Klicks  │
//  │               │ (Buchstaben/Zahlen/Formen)│ + Submit-Button │
//  └─────────────────────────────────────────────────────────────┘
//
//  Wichtig: Alle drei Typen teilen #captcha-verify-image.
//  Differenzierung ausschließlich über Slider-Präsenz, Bild-Struktur
//  und Submit-Button. Rotate wird zuerst geprüft (eindeutigste Signale),
//  dann Slide (Slider + Puzzleteil), zuletzt 3D Objects (Submit, kein Slider).
//
//  Jeder Provider wird einzeln im Orchestrator registriert.
//  Falls mehrere matchen (sollte nicht vorkommen), gilt die Priorität
//  der Provider-Liste: Rotate > Slide > 3D Objects.
// ════════════════════════════════════════════════════════════════════


// ────────────────────────────────────────
//  Hilfsfunktion: TikTok-Container vorhanden?
//  Wird von allen drei TikTok-Providern aufgerufen, um
//  Mehrfach-Traversal zu vermeiden.
// ────────────────────────────────────────
function _tikTokContainerPresent() {
    // Iframe-Prüfung (ByteDance CDN / TikTok eigene Domains)
    if (iframeHas("tiktok.com/captcha") ||
        iframeHas("verification.bytedance.com") ||
        iframeHas("verify.bytedance.com") ||
        iframeHas("verify.tiktok.com")) return true;

    // DOM-Container: V1 (.captcha-disable-scroll) oder V2 (.captcha-verify-container)
    const containerSelectors = [
        ".captcha-disable-scroll",
        ".captcha-verify-container",
        ".captcha_verify_container",
        "div[id*='tiktok-captcha']",
        "div[class*='secsdk_captcha']",
        "div[class*='TUXCaptcha']",
    ];
    for (const doc of allDocs) {
        for (const sel of containerSelectors) {
            if (deepQueryVisible(doc, sel)) return true;
        }
    }
    return false;
}


// ════════════════════════════════════════
//  PROVIDER: TikTok Rotate CAPTCHA
//
//  Mechanismus:
//    Zwei konzentrische, kreisförmige Bilder werden überlagert.
//    Das innere Bild ist rotiert (falsch ausgerichtet), der Nutzer
//    muss über einen Slider das innere Bild in die korrekte Position
//    zurückdrehen. Das äußere Bild dient als statische Referenz.
//
//  Eindeutige DOM-Merkmale:
//    – ZWEI Bilder (inner + outer) im selben Container
//    – Slider-Element zum Drehen (kein Puzzleteil-Bild!)
//    – V1: data-testid="whirl-inner-img" / "whirl-outer-img"
//    – V2: img.cap-absolute (inneres Bild überlagert erstes Bild)
//
//  Abgrenzung zu Puzzle Slide:
//    Rotate hat zwei überlagerte Bild-Elemente im kreisförmigen
//    Container, kein img.captcha_verify_img_slide (Puzzleteil).
//
//  Selektoren:
//    V1 inneres Bild : [data-testid=whirl-inner-img]
//    V1 äußeres Bild : [data-testid=whirl-outer-img]
//    V1 Slider       : .secsdk-captcha-drag-icon
//    V2 inneres Bild : .captcha-verify-container > div > div > div > img.cap-absolute
//    V2 äußeres Bild : .captcha-verify-container > div > div > div > img:first-child
//    V2 Slider       : .captcha-verify-container div[draggable=true]
//    Klassen-Fallback: div[class*='captcha_verify_rotate'], .secsdk_captcha_rotate
// ════════════════════════════════════════

class TikTokRotateProvider extends CaptchaProvider {
    constructor() { super("TikTok CAPTCHA (Rotate)"); }

    detect() {
        if (!_tikTokContainerPresent()) return null;

        for (const doc of allDocs) {
            // ── V1: data-testid-Selektoren (Legacy-API) ──────────────
            const innerV1 = deepQueryVisible(doc, "[data-testid='whirl-inner-img']");
            const outerV1 = deepQueryVisible(doc, "[data-testid='whirl-outer-img']");
            const sliderV1 = deepQueryVisible(doc, ".secsdk-captcha-drag-icon") ||
                             deepQueryVisible(doc, ".secsdk_captcha_rotate");
            const classRotate = deepQueryVisible(doc, "div[class*='captcha_verify_rotate']");

            // V1: beide Bild-Testids → eindeutig Rotate
            if (innerV1 && outerV1) {
                return this.result({
                    description: [
                        "Rotate CAPTCHA (V1) – Inneres Bild ist rotiert.",
                        "  ➜ Slider (.secsdk-captcha-drag-icon) horizontal ziehen bis",
                        "    das innere Bild [data-testid=whirl-inner-img] korrekt ausgerichtet ist.",
                        "  ➜ Lösungsweg: Screenshot CAPTCHA-Element → NVIDIA NIM Vision",
                        "    schätzt Rotationswinkel → Slider um entsprechenden Pixel-Offset verschieben.",
                    ].join("\n"),
                });
            }

            // V1: Klassen-Fallback (ältere Implementierung ohne testids)
            if (classRotate && sliderV1) {
                return this.result({
                    description: [
                        "Rotate CAPTCHA (V1 Klassen-Fallback) – Rotiertes Kreisbild.",
                        "  ➜ Slider (.secsdk-captcha-drag-icon) ziehen.",
                        "  ➜ Container: div[class*='captcha_verify_rotate']",
                    ].join("\n"),
                });
            }

            // ── V2: cap-absolute-Selektor (aktuelle API) ─────────────
            // Das innere (rotierende) Bild liegt als img.cap-absolute
            // über dem ersten img-Element (äußeres Bild) im Container.
            const innerV2 = deepQueryVisible(doc,
                ".captcha-verify-container > div > div > div > img.cap-absolute");
            const outerV2 = deepQueryVisible(doc,
                ".captcha-verify-container > div > div > div > img:first-child");
            const sliderV2 = deepQueryVisible(doc,
                ".captcha-verify-container div[draggable='true']");

            if (innerV2 && outerV2 && sliderV2) {
                return this.result({
                    description: [
                        "Rotate CAPTCHA (V2) – Zwei überlagerte Kreisbilder.",
                        "  ➜ Slider (.captcha-verify-container div[draggable=true]) ziehen.",
                        "  ➜ Inneres Bild: img.cap-absolute  |  Äußeres: img:first-child",
                        "  ➜ Lösungsweg: Screenshot CAPTCHA-Element → NVIDIA NIM Vision →",
                        "    humanized_drag(knob → target_x)",
                    ].join("\n"),
                });
            }

            // V2 Fallback: inneres Bild vorhanden + Slider (äußeres nicht sicher erkannt)
            if (innerV2 && sliderV2) {
                return this.result({
                    description: [
                        "Rotate CAPTCHA (V2 Partial) – Inneres Bild + Slider erkannt.",
                        "  ➜ Slider (.captcha-verify-container div[draggable=true]) ziehen.",
                    ].join("\n"),
                });
            }
        }
        return null;
    }
}


// ════════════════════════════════════════
//  PROVIDER: TikTok Puzzle Slide CAPTCHA
//
//  Mechanismus:
//    Ein rechteckiges Hintergrundbild hat eine Lücke (Puzzleform).
//    Ein separates Puzzleteil-Bild muss per Slider horizontal
//    über die Lücke geschoben werden. Slider + Puzzleteil sind
//    das eindeutige Merkmal – KEIN Submit-Button.
//
//  Eindeutige DOM-Merkmale:
//    – Puzzleteil als separates img-Element (captcha_verify_img_slide)
//    – Hintergrundbild mit Lücke (#captcha-verify-image)
//    – Slider zum horizontalen Verschieben (.secsdk-captcha-drag-icon)
//    – V2: draggable-div als Puzzleteil-Container
//    – KEIN .verify-captcha-submit-button
//    – KEIN whirl-inner/outer-img (kein konzentrisches Bild)
//
//  Abgrenzung zu Rotate:
//    Kein konzentrisches Doppelbild; Puzzleteil ist ein eigenes
//    img-Element neben dem Hintergrund (nicht überlagert).
//
//  Selektoren:
//    V1 Puzzleteil   : img.captcha_verify_img_slide
//    V1 Hintergrund  : #captcha-verify-image
//    V1 Slider       : .secsdk-captcha-drag-icon
//    V2 Puzzleteil   : .captcha-verify-container .cap-absolute img
//    V2 Hintergrund  : #captcha-verify-image
//    V2 Slider       : .secsdk-captcha-drag-icon (gleiches Element)
//    Klassen-Fallback: div[class*='captcha_verify_slide'], .secsdk_captcha_slide
// ════════════════════════════════════════

class TikTokSlideProvider extends CaptchaProvider {
    constructor() { super("TikTok CAPTCHA (Puzzle Slide)"); }

    detect() {
        if (!_tikTokContainerPresent()) return null;

        for (const doc of allDocs) {
            // Slider-Präsenz ist Grundbedingung (trennt von 3D Objects)
            const hasSlider =
                deepQueryVisible(doc, ".secsdk-captcha-drag-icon") ||
                deepQueryVisible(doc, ".captcha-verify-container div[draggable='true']");
            if (!hasSlider) continue;

            // ── V1: Klassisches Puzzleteil-img ───────────────────────
            // img.captcha_verify_img_slide ist exklusiv für Puzzle Slide –
            // Rotate nutzt whirl-inner/outer-img stattdessen.
            const puzzlePieceV1 = deepQueryVisible(doc, "img.captcha_verify_img_slide");
            const bgImageV1     = deepQueryVisible(doc, "#captcha-verify-image");
            const classSlide    = deepQueryVisible(doc, "div[class*='captcha_verify_slide']") ||
                                  deepQueryVisible(doc, ".secsdk_captcha_slide");

            if (puzzlePieceV1 && bgImageV1) {
                return this.result({
                    description: [
                        "Puzzle Slide CAPTCHA (V1) – Puzzleteil in Lücke schieben.",
                        "  ➜ Puzzleteil: img.captcha_verify_img_slide",
                        "  ➜ Hintergrund mit Lücke: #captcha-verify-image",
                        "  ➜ Slider: .secsdk-captcha-drag-icon  (horizontal ziehen)",
                        "  ➜ Lösungsweg: Screenshot CAPTCHA-Element → NVIDIA NIM Vision",
                        "    schätzt Lückenposition → humanized_drag(knob → target_x).",
                    ].join("\n"),
                });
            }

            if (classSlide && hasSlider) {
                return this.result({
                    description: [
                        "Puzzle Slide CAPTCHA (V1 Klassen-Fallback).",
                        "  ➜ Container: div[class*='captcha_verify_slide']",
                        "  ➜ Slider: .secsdk-captcha-drag-icon  (horizontal ziehen)",
                    ].join("\n"),
                });
            }

            // ── V2: cap-absolute-Puzzleteil ──────────────────────────
            // In V2 liegt das Puzzleteil als img innerhalb eines
            // .cap-absolute-Containers über dem Hintergrundbild.
            // Abgrenzung zu Rotate-V2: img.cap-absolute direkt im
            // Tier-4-Container ist Rotate; hier ist es ein img INNERHALB
            // von .cap-absolute (ein Level tiefer).
            const puzzlePieceV2 = deepQueryVisible(doc,
                ".captcha-verify-container .cap-absolute img");
            const bgImageV2 = deepQueryVisible(doc, "#captcha-verify-image");

            // Sicherheitscheck: Rotate-V1/V2-Signale ausschließen
            const hasRotateSignal =
                deepQueryVisible(doc, "[data-testid='whirl-inner-img']") ||
                deepQueryVisible(doc, ".captcha-verify-container > div > div > div > img.cap-absolute");

            if (puzzlePieceV2 && bgImageV2 && !hasRotateSignal) {
                return this.result({
                    description: [
                        "Puzzle Slide CAPTCHA (V2) – Puzzleteil (.cap-absolute img) schieben.",
                        "  ➜ Hintergrund mit Lücke: #captcha-verify-image",
                        "  ➜ Slider: .captcha-verify-container div[draggable=true]",
                        "  ➜ Lösungsweg: Screenshot CAPTCHA-Element → NVIDIA NIM Vision →",
                        "    humanized_drag(knob → target_x).",
                    ].join("\n"),
                });
            }
        }
        return null;
    }
}


// ════════════════════════════════════════
//  PROVIDER: TikTok 3D Objects / Shapes CAPTCHA
//
//  Mechanismus:
//    Ein einzelnes Bild zeigt mehrere 3D-gerenderte Objekte
//    (Buchstaben, Zahlen, geometrische Formen) in einem Raum.
//    Eine Textanweisung gibt vor, welche Objekte in welcher
//    Reihenfolge angeklickt werden müssen. Nach allen Klicks
//    wird über einen Submit-Button abgesendet.
//    KEIN Slider, KEIN zweites Bild-Element.
//
//  Eindeutige DOM-Merkmale:
//    – Ein Hauptbild mit allen 3D-Objekten (#captcha-verify-image)
//    – Submit-Button (.verify-captcha-submit-button)
//    – Textanweisung (.captcha_verify_bar)
//    – V2: button.cap-w-full als Submit, span als Anweisung
//    – KEIN .secsdk-captcha-drag-icon (kein Slider!)
//    – KEIN img.captcha_verify_img_slide (kein Puzzleteil!)
//    – KEIN whirl-inner/outer-img (kein konzentrisches Bild!)
//
//  Abgrenzung:
//    Das Fehlen des Sliders ist das stärkste Abgrenzungsmerkmal
//    zu Rotate und Puzzle Slide. Zusätzlich ist der Submit-Button
//    exklusiv für diesen Typ.
//
//  Selektoren:
//    V1 Bild         : #captcha-verify-image
//    V1 Submit       : .verify-captcha-submit-button
//    V1 Anweisung    : .captcha_verify_bar
//    V2 Bild         : .captcha-verify-container div.cap-relative img
//    V2 Submit       : .captcha-verify-container .cap-relative button.cap-w-full
//    V2 Anweisung    : .captcha-verify-container > div > div > span
//    Negativfilter   : .secsdk-captcha-drag-icon (→ kein 3D Objects!)
// ════════════════════════════════════════

class TikTok3DObjectsProvider extends CaptchaProvider {
    constructor() { super("TikTok CAPTCHA (3D Objects)"); }

    detect() {
        if (!_tikTokContainerPresent()) return null;

        for (const doc of allDocs) {
            // ── Negativfilter: Slider vorhanden → nicht 3D Objects ───
            // Dieser Check muss als erstes laufen, da #captcha-verify-image
            // bei allen drei TikTok-Typen erscheint.
            const hasSlider =
                deepQueryVisible(doc, ".secsdk-captcha-drag-icon") ||
                deepQueryVisible(doc, ".captcha-verify-container div[draggable='true']");
            if (hasSlider) continue;  // Rotate oder Slide → überspringen

            // ── Negativfilter: Rotate-Bilder vorhanden → nicht 3D ────
            const hasRotateParts =
                deepQueryVisible(doc, "[data-testid='whirl-inner-img']") ||
                deepQueryVisible(doc, "[data-testid='whirl-outer-img']") ||
                deepQueryVisible(doc, ".captcha-verify-container > div > div > div > img.cap-absolute");
            if (hasRotateParts) continue;

            // ── V1: klassischer Submit-Button + Hauptbild ─────────────
            const submitV1 = deepQueryVisible(doc, ".verify-captcha-submit-button");
            const imageV1  = deepQueryVisible(doc, "#captcha-verify-image");
            const instrV1  = deepQueryVisible(doc, ".captcha_verify_bar");

            if (submitV1 && imageV1) {
                const hasInstruction = instrV1 ? "  ➜ Anweisung in: .captcha_verify_bar" : "";
                return this.result({
                    description: [
                        "3D Objects CAPTCHA (V1) – 3D-Objekte in Reihenfolge anklicken.",
                        "  ➜ Bild: #captcha-verify-image  (enthält alle Objekte)",
                        "  ➜ Submit: .verify-captcha-submit-button  (nach allen Klicks)",
                        hasInstruction,
                        "  ➜ Lösungsweg: Screenshot → NVIDIA NIM Vision liefert",
                        "    (x,y)-Koordinaten pro Objekt → humanized_click()",
                        "    mit Bezier-Trajektorie + Pause 500–1500 ms zwischen Klicks.",
                    ].filter(Boolean).join("\n"),
                });
            }

            // ── V2: button.cap-w-full + div.cap-relative img ──────────
            const submitV2 = deepQueryVisible(doc,
                ".captcha-verify-container .cap-relative button.cap-w-full");
            const imageV2  = deepQueryVisible(doc,
                ".captcha-verify-container div.cap-relative img");
            const instrV2  = deepQueryVisible(doc,
                ".captcha-verify-container > div > div > span");

            if (submitV2 && imageV2) {
                return this.result({
                    description: [
                        "3D Objects CAPTCHA (V2) – 3D-Objekte in Reihenfolge anklicken.",
                        "  ➜ Bild: .captcha-verify-container div.cap-relative img",
                        "  ➜ Submit: button.cap-w-full  (nach allen Klicks absenden)",
                        instrV2 ? "  ➜ Anweisung: .captcha-verify-container > div > div > span" : "",
                        "  ➜ Lösungsweg: Screenshot → NVIDIA NIM Vision liefert",
                        "    (x,y)-Koordinaten → humanized_click() mit",
                        "    Bezier-Trajektorie + menschlicher Pause zwischen Klicks.",
                    ].filter(Boolean).join("\n"),
                });
            }

            // ── Fallback: TUXCaptcha / Shapes-Klassenname ────────────
            const hasTUX =
                deepQueryVisible(doc, "div[class*='TUXCaptcha']") ||
                deepQueryVisible(doc, "div[class*='captcha_shapes']") ||
                deepQueryVisible(doc, "div[class*='captcha_verify_img_3d']") ||
                deepQueryVisible(doc, ".captcha_verify_img--wrapper");

            if (hasTUX) {
                return this.result({
                    description: [
                        "3D Objects CAPTCHA (TUX/Shapes-Fallback).",
                        "  ➜ Container: div[class*='TUXCaptcha'] oder captcha_shapes",
                        "  ➜ Kein Slider erkannt → Submit-Button-basierte Interaktion.",
                    ].join("\n"),
                });
            }
        }
        return null;
    }
}


// ════════════════════════════════════════
//  PROVIDER: GeeTest v3 / v4
// ════════════════════════════════════════

class GeeTestProvider extends CaptchaProvider {
    constructor() { super("GeeTest"); }

    detect() {
        let found = false;
        for (const doc of allDocs) {
            for (const sel of ["div.geetest_holder","div.geetest_wrap",".geetest_btn",
                               "div.geetest_box","div.geetest_oneclick_wrap"]) {
                if (deepQueryVisible(doc, sel)) { found = true; break; }
            }
            if (found) break;
        }
        const hasGTScript = scriptHas("static.geetest.com") || scriptHas("gcaptcha.geetest.com") ||
                            scriptHas("gcaptcha4.geetest.com");
        if (!found && !hasGTScript) return null;

        const isV4 = scriptHas("gcaptcha4.geetest.com") || scriptHas("static.geetest.com/v4");

        let solved = csi.geetest?.solved || false;
        if (!solved) {
            for (const doc of allDocs) {
                const c = deepQuery(doc, 'input[name="geetest_challenge"]');
                const v = deepQuery(doc, 'input[name="geetest_validate"]');
                const s = deepQuery(doc, 'input[name="geetest_seccode"]');
                if (c?.value && v?.value && s?.value) { solved = true; break; }
                if (deepQuery(doc, ".geetest_panel_success, .geetest_success_radar_tip")) { solved = true; break; }
            }
        }
        return this.result({
            name: isV4 ? "GeeTest v4" : "GeeTest v3",
            solved,
            description: isV4
                ? "GeeTest v4 – One-Click oder AI-Verification."
                : "GeeTest v3 – Slider-Puzzle.\n  ➜ Slider ziehen bis Puzzleteil in Lücke passt.",
        });
    }
}


// MTCaptchaProvider entfernt – nicht mehr unterstützt.


// ClickCaptchaProvider entfernt – nicht mehr unterstützt.


// ════════════════════════════════════════
//  PROVIDER: Meta Text-CAPTCHA
//  Instagram Checkpoint + Facebook Security Check
//
//  FALSE-POSITIVE-FIX (v6):
//  Ursache: Facebook-Registrierungsseite (facebook.com/r.php) wurde
//  erkannt weil onFbDomain allein als ausreichendes Signal galt.
//
//  Neue Logik – zwei Schutzebenen:
//
//  Ebene 1 – URL-Negativfilter:
//    Bekannte Non-CAPTCHA-Pfade (Registrierung, Login, Passwort-Reset)
//    werden ohne starkes Primärsignal grundsätzlich ausgeschlossen.
//    Starkes Primärsignal = captcha_response-Input im DOM.
//
//  Ebene 2 – Pflicht-Explizit-Signal:
//    Auf Meta-Domains (FB/IG) muss mindestens EINES der folgenden
//    expliziten CAPTCHA-Elemente vorhanden sein:
//      – hasCaptchaResponse: input[name=captcha_response/token/sid]
//      – hasFbSecurity: Security-Check-Container ODER CAPTCHA-Formular
//      – hasIgCheckpoint: iframe von instagram.com/checkpoint/
//      – hasIgSuspended: /accounts/suspended/ mit CAPTCHA-Bild
//      – hasMetaCaptchaImg: Bild mit CAPTCHA-typischer URL/Alt + CAPTCHA-Input
// ════════════════════════════════════════

class MetaTextCaptchaProvider extends CaptchaProvider {
    constructor() { super("Text-CAPTCHA (Meta)"); }

    detect() {
        const onFbDomain = /\.(facebook|fb)\.com$/.test(currentHostname);
        const onIgDomain = currentHostname.includes("instagram.com");

        if (!onFbDomain && !onIgDomain) return null;

        // ── Ebene 1: URL-Negativfilter ───────────────────────────────
        // Diese Pfade sind normale Account-Seiten ohne CAPTCHA-Formular.
        const NON_CAPTCHA_PATHS = [
            "/r.php", "/reg", "/signup", "/create",     // Registrierung
            "/login", "/accounts/login",                 // Login
            "/accounts/emailsignup",                     // IG Registrierung
            "/recover", "/forgot", "/password",          // Passwort-Reset
        ];
        const isNonCaptchaPage = NON_CAPTCHA_PATHS.some(p => currentPath.startsWith(p));

        // ── Explizite CAPTCHA-Signale ────────────────────────────────

        // Stärkstes Signal: Meta-typische Input-Namen im DOM
        let hasCaptchaResponse = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, "input[name='captcha_response'], input[name='captcha_token'], input[name='captcha_sid']")) {
                hasCaptchaResponse = true; break;
            }
        }

        // Instagram Checkpoint-Iframe
        const hasIgCheckpoint = iframeHas("instagram.com/checkpoint/");
        let hasIgFrame = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, "iframe[src*='instagram.com/checkpoint']")) { hasIgFrame = true; break; }
        }

        // Facebook Security Check – nur in dedizierten CAPTCHA-Containern suchen,
        // NICHT im gesamten Body-Text (würde bei /r.php fälschlich matchen)
        let hasFbSecurity = false;
        for (const doc of allDocs) {
            for (const sel of [".hidden_elem", "#captcha", "#captcha_response_wrapper"]) {
                const el = deepQuery(doc, sel);
                if (el?.textContent?.toLowerCase().includes("security check")) {
                    hasFbSecurity = true; break;
                }
            }
            if (hasFbSecurity) break;
            // Explizites CAPTCHA-Formular (eindeutigstes FB-Signal)
            if (deepQuery(doc, "form[action*='/captcha'], #captcha_response_wrapper")) {
                hasFbSecurity = true; break;
            }
        }

        // Instagram gesperrter Account mit Text-CAPTCHA
        // /accounts/suspended/ zeigt ein CAPTCHA-Bild + Eingabefeld
        const hasIgSuspended = onIgDomain && (
            currentPath.includes("/accounts/suspended") ||
            currentPath.includes("/challenge/")
        );

        // Allgemeines Meta-CAPTCHA-Bild + passender Input
        // (fängt neue Checkpoint-Varianten ab die keinen expliziten Namen haben)
        let hasMetaCaptchaImg = false;
        let hasMetaCaptchaInput = false;
        for (const doc of allDocs) {
            for (const sel of [
                "img[src*='captcha' i]","img[src*='challenge' i]",
                "img[alt*='captcha' i]","img[alt*='verification' i]",
                "img[class*='captcha' i]",
            ]) {
                if (deepQueryVisible(doc, sel)) { hasMetaCaptchaImg = true; break; }
            }
            for (const sel of [
                "input[placeholder*='abbildung' i]",
                "input[placeholder*='code' i][placeholder*='bild' i]",
                "input[aria-label*='captcha' i]",
                "input[name*='captcha' i]:not([type='hidden'])",
            ]) {
                if (deepQuery(doc, sel)) { hasMetaCaptchaInput = true; break; }
            }
        }
        // Text-Signale spezifisch für Meta-Plattformen
        const metaCaptchaTexts = [
            "bestätige, dass du kein roboter bist",
            "confirm you're not a robot",
            "hör dir diesen code an","fordere einen neuen code an",
            "gib den code auf der abbildung ein",
            "gib den text auf dem bild ein",
            "type the code shown above","enter the text you see",
        ];
        const hasMetaCaptchaText = metaCaptchaTexts.some(t => allText.includes(t));

        // ── Ebene 2: Pflicht-Explizit-Signal ────────────────────────
        const hasExplicitSignal =
            hasCaptchaResponse ||
            hasIgCheckpoint || hasIgFrame ||
            hasFbSecurity ||
            (hasIgSuspended && (hasMetaCaptchaImg || hasMetaCaptchaText || hasMetaCaptchaInput)) ||
            (hasMetaCaptchaImg && hasMetaCaptchaInput && hasMetaCaptchaText);

        if (!hasExplicitSignal) return null;

        // Auf bekannten Non-CAPTCHA-Pfaden: nur bei starkem Primärsignal melden
        if (isNonCaptchaPage && !hasCaptchaResponse) return null;

        const platform = onIgDomain ? "Instagram" : "Facebook";
        return this.result({
            description: `Text-CAPTCHA (${platform}) – Verzerrte Buchstaben/Zahlen.\n  ➜ Zeichen aus Bild abtippen; Audio-Alternative verfügbar.`,
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: Generisches Text-CAPTCHA
// ════════════════════════════════════════

class GenericTextCaptchaProvider extends CaptchaProvider {
    constructor() { super("Text-CAPTCHA"); }

    detect() {
        let hasCaptchaImg = false;
        for (const doc of allDocs) {
            for (const sel of ["img[src*='captcha' i]","img[alt*='captcha' i]",
                               "img[id*='captcha' i]","canvas[id*='captcha' i]",
                               "img[src*='challenge' i]","img[src*='verify' i]"]) {
                if (deepQueryVisible(doc, sel)) { hasCaptchaImg = true; break; }
            }
            if (hasCaptchaImg) break;
        }

        let hasCaptchaInput = false;
        for (const doc of allDocs) {
            for (const sel of [
                "input[name*='captcha' i]:not([type='hidden'])",
                "input[id*='captcha' i]:not([type='hidden'])",
                "input[placeholder*='abbildung' i]",
                "input[placeholder*='text from image' i]",
                "input[placeholder*='code' i][placeholder*='bild' i]",
                "input[aria-label*='captcha' i]",
                "#captcha",
            ]) {
                if (deepQuery(doc, sel)) { hasCaptchaInput = true; break; }
            }
            if (hasCaptchaInput) break;
        }

        const strongTextSignals = [
            // Deutsch
            "gib den code auf der abbildung ein",
            "gib den text auf dem bild ein",
            "du kannst den text nicht lesen",
            "bestätige, dass du kein roboter bist",
            "hör dir diesen code an",
            "fordere einen neuen code an",
            // Englisch
            "enter the code shown in the image",
            "type the characters you see",
            "type the text you hear or see",
            "enter text from image",
            "type the code from the image",
            "confirm you're not a robot",
            "enter the text you see",
        ];
        const hasStrongText = strongTextSignals.some(t => allText.includes(t));

        if (!(hasCaptchaImg && hasCaptchaInput) && !(hasStrongText && hasCaptchaInput)) return null;
        return this.result({
            description: "Text-CAPTCHA – Verzerrte Buchstaben/Zahlen im Bild.\n  ➜ Zeichen erkennen und ins Textfeld eintippen.",
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: Math-CAPTCHA
// ════════════════════════════════════════

class MathCaptchaProvider extends CaptchaProvider {
    constructor() { super("Math-CAPTCHA"); }

    detect() {
        let found = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, "input[id*='math' i], input[name*='math' i], .wpcf7-math-captcha")) {
                found = true; break;
            }
        }
        if (!found) return null;
        return this.result({
            description: "Mathe-CAPTCHA – Rechenaufgabe lösen und Ergebnis eingeben.",
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: DataDome
//  Sehr verbreitet bei E-Commerce / Booking-Sites.
//  Signale: iframe von geo.captcha-delivery.com,
//           Script von js.datadome.co, dd_cookie.
// ════════════════════════════════════════

class DataDomeProvider extends CaptchaProvider {
    constructor() { super("DataDome"); }

    detect() {
        const hasDDIframe = iframeHas("captcha-delivery.com") ||
                            iframeHas("datadome.co");
        const hasDDScript = scriptHas("datadome.co") ||
                            scriptHas("js.datado.me");
        let hasDDDom = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, "[id*='datadome' i], [class*='datadome' i], #dd_captcha")) {
                hasDDDom = true; break;
            }
        }
        if (!hasDDIframe && !hasDDScript && !hasDDDom) return null;
        return this.result({
            description: [
                "DataDome – Bot-Mitigation mit Slider- oder Press&Hold-Challenge.",
                "  ➜ Iframe: geo.captcha-delivery.com",
                "  ➜ Lösungsweg: Slider greifen (.slider, .geetest_btn-äquivalent),",
                "    horizontal ziehen — oder Press&Hold-Variante halten.",
            ].join("\n"),
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: AWS WAF CAPTCHA
//  Erkennt sowohl AWS WAF Captcha (visuell) als auch Token-Challenge.
//  Signale: iframe von /captcha/ auf awswaf.com, Token-Endpoints.
// ════════════════════════════════════════

class AwsWafCaptchaProvider extends CaptchaProvider {
    constructor() { super("AWS WAF CAPTCHA"); }

    detect() {
        const hasAwsIframe = iframeHas("awswaf.com") ||
                             iframeHas("token.awswaf.com") ||
                             iframeMatchRe(/awswaf\.com\/(captcha|token)/);
        const hasAwsScript = scriptHas("awswaf.com/awswaf");
        let hasAwsDom = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, "[class*='aws-waf-captcha' i], #captcha-container")) {
                // Heuristik: nur als AWS klassifizieren wenn auch Script/Iframe
                if (hasAwsIframe || hasAwsScript) {
                    hasAwsDom = true; break;
                }
            }
        }
        if (!hasAwsIframe && !hasAwsScript && !hasAwsDom) return null;
        return this.result({
            description: [
                "AWS WAF CAPTCHA – Puzzle- oder Bild-Klick-Challenge.",
                "  ➜ Iframe: awswaf.com/captcha/  |  Token-Endpoint: token.awswaf.com",
                "  ➜ Lösungsweg: variante-abhängig (puzzle slide oder image-click).",
            ].join("\n"),
        });
    }
}


// ════════════════════════════════════════
//  PROVIDER: Yandex SmartCaptcha
//  Yandex' eigene CAPTCHA — vor allem auf .ru-Sites + manchen EU-Cloud-Hosts.
// ════════════════════════════════════════

class YandexSmartCaptchaProvider extends CaptchaProvider {
    constructor() { super("Yandex SmartCaptcha"); }

    detect() {
        const hasYIframe = iframeHas("smartcaptcha.yandexcloud") ||
                           iframeHas("captcha-api.yandex");
        const hasYScript = scriptHas("smartcaptcha.yandexcloud") ||
                           scriptHas("captcha.yandex");
        let hasYDom = false;
        for (const doc of allDocs) {
            if (deepQuery(doc, ".smart-captcha, [data-sitekey][class*='smart' i]")) {
                hasYDom = true; break;
            }
        }
        if (!hasYIframe && !hasYScript && !hasYDom) return null;
        return this.result({
            description: [
                "Yandex SmartCaptcha – Checkbox + ggf. Bild-/Slider-Challenge.",
                "  ➜ Iframe: smartcaptcha.yandexcloud.net",
                "  ➜ Lösungsweg: Checkbox klicken; bei Eskalation → Slider/Bild.",
            ].join("\n"),
        });
    }
}


// ════════════════════════════════════════
//  ORCHESTRATOR
// ════════════════════════════════════════

class CaptchaScanner {
    constructor() {
        this.providers = [
            new MicrosoftHIPProvider(),        //  1: vor allen anderen!
            new ReCaptchaV3Provider(),         //  2a
            new ReCaptchaV2Provider(),         //  2b
            new HCaptchaProvider(),            //  3
            new TurnstileProvider(),           //  4a
            new CfChallengeProvider(),         //  4b
            // TikTok: drei separate Provider, Priorität Rotate > Slide > 3D Objects
            // Falls mehrere matchen (sollte nicht passieren), gewinnt der erste.
            new TikTokRotateProvider(),        //  5a: stärkste Signale zuerst
            new TikTokSlideProvider(),         //  5b: Slider + Puzzleteil
            new TikTok3DObjectsProvider(),     //  5c: Submit + kein Slider
            new GeeTestProvider(),             //  6
            new DataDomeProvider(),            //  7a: vor MetaText (DataDome hat eigene Iframe-URL)
            new AwsWafCaptchaProvider(),       //  7b
            new YandexSmartCaptchaProvider(),  //  7c
            new MetaTextCaptchaProvider(),     //  8
            new GenericTextCaptchaProvider(),  //  9: Fallback
            new MathCaptchaProvider(),         // 10: immer zusätzlich möglich
        ];
        this.specificTypes = new Set([
            "reCAPTCHA v2","reCAPTCHA v3 / Invisible","hCaptcha",
            "Cloudflare Turnstile","Cloudflare Challenge",
            "Text-CAPTCHA (Meta)",
            "DataDome","AWS WAF CAPTCHA","Yandex SmartCaptcha",
            // TikTok-spezifische Namen für GenericText-Ausschluss
            "TikTok CAPTCHA (Rotate)","TikTok CAPTCHA (Puzzle Slide)","TikTok CAPTCHA (3D Objects)",
        ]);
    }

    scan() {
        const results = [];
        let hasRcV3 = false;
        let hasTikTok = false;  // Nur ein TikTok-Typ pro Scan

        for (const provider of this.providers) {
            const name = provider.name;
            if (name === "reCAPTCHA v2" && hasRcV3) continue;
            if (name === "Text-CAPTCHA" && results.some(r => this.specificTypes.has(r.name))) continue;
            // Sobald ein TikTok-Typ gefunden wurde, restliche überspringen
            if (name.startsWith("TikTok CAPTCHA") && hasTikTok) continue;

            const result = provider.detect();
            if (result) {
                results.push(result);
                if (name === "reCAPTCHA v3 / Invisible") hasRcV3  = true;
                if (name.startsWith("TikTok CAPTCHA"))   hasTikTok = true;
            }
        }
        return results;
    }
}

updateGlobals();
const scanner = new CaptchaScanner();
const initialResults = scanner.scan();

if (window.__INJECTED_KEY__) return initialResults;
window.__INJECTED_KEY__ = true;

const reported = new Set(initialResults.map(r => r.name + (r.solved ? "_solved" : "")));
let debounceTimer = null;

const TARGET_SELECTORS = [
    "iframe", "script", "div[class*='captcha']", "#recaptcha-anchor", 
    ".g-recaptcha", ".h-captcha", ".cf-turnstile", "#challenge-form",
    ".secsdk-captcha-drag-icon", "img", ".captcha-verify-container"
];

function runScanEvent() {
    updateGlobals();
    const results = scanner.scan();
    for (const res of results) {
        const key = res.name + (res.solved ? "_solved" : "");
        if (!reported.has(key)) {
            reported.add(key);
            // Report channel (R1): emit on console instead of calling a
            // Playwright expose_binding() function on window. A bound
            // window function is a one-line automation tell; a prefixed
            // console.debug message adds nothing to the window object and
            // is indistinguishable from ordinary page logging. The Python
            // side filters page.on("console") on "__REPORT_PREFIX__".
            try {
                console.debug("__REPORT_PREFIX__" + JSON.stringify(res));
            } catch (e) {}
        }
    }
}

const obsEvent = new MutationObserver((mutations) => {
    let shouldScan = false;
    for (const m of mutations) {
        for (const node of m.addedNodes) {
            if (node.nodeType === 1) {
                if (TARGET_SELECTORS.some(sel => {
                    try { return node.matches(sel) || node.querySelector(sel); } 
                    catch(e) { return false; }
                })) {
                    shouldScan = true;
                    break;
                }
            }
        }
        if (shouldScan) break;
    }
    if (shouldScan) {
        if (debounceTimer) clearTimeout(debounceTimer);
        debounceTimer = setTimeout(runScanEvent, __SCAN_DEBOUNCE_MS__);
    }
});

const startObserving = () => {
    obsEvent.observe(document.documentElement, { childList: true, subtree: true });
};

if (document.body) startObserving();
else document.addEventListener("DOMContentLoaded", startObserving);

return initialResults;
})();
"""


# ══════════════════════════════════════════════════════════════════
#  Terminal helpers
# ══════════════════════════════════════════════════════════════════

def _clear_line():
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()

def _ts() -> str:
    return datetime.now().strftime("%H:%M:%S")

def _sep(ch: str = "─", n: int = 70) -> None:
    print(ch * n)

def _print_report(captchas: list, url: str, title: str, idx: int, total: int) -> None:
    print()
    _sep("═")
    print(f"  🚨  CAPTCHA ERKANNT  –  {_ts()}")
    print(f"  🗂   Page {idx}/{total}:  {(title or '(kein Titel)')[:52]}")
    print(f"  🌐  {url[:72]}{'...' if len(url) > 72 else ''}")
    _sep("═")
    for i, cap in enumerate(captchas, 1):
        print(f"\n  [{i}]  🤖  {cap['name']}")
        _sep()
        print(f"  📋  {cap['description']}\n")
        if cap.get("solved"):
            print("  ✅  Status: GELÖST")
        elif cap.get("expired"):
            print("  ⏰  Status: TOKEN ABGELAUFEN – bitte neu lösen")
    _sep("═")
    print()


# ══════════════════════════════════════════════════════════════════
#  PLAYWRIGHT-ADAPTER  (primäre Nutzungsform)
# ══════════════════════════════════════════════════════════════════

async def _inject_observer(page) -> None:
    """Injiziert den MutationObserver in Main-Frame + alle Sub-Frames.

    Wird einmalig pro (Page, URL) ausgeführt. Im Idealfall hat der
    Caller bereits `context.add_init_script(JS_INJECT_OBSERVERS)`
    aufgerufen — dann läuft der Observer vor allen Page-Scripts und
    fängt auch Captchas auf dem ersten Frame-Paint. Diese Funktion
    bleibt als Fallback und für Frames, die bei `add_init_script`
    noch nicht existierten.
    """
    url = page.url
    if _observer_injected.get(page) == url:
        return
    markers = _markers_for_page(page)
    injected_any = False
    for frame in list(page.frames):
        try:
            if hasattr(frame, "is_detached") and frame.is_detached():
                continue
        except Exception:
            continue
        try:
            await frame.evaluate(_render(JS_INJECT_OBSERVERS, markers))
            injected_any = True
        except Exception:
            # Cross-origin / CSP / navigation race — Observer für
            # diesen Frame nicht installierbar; Detection bleibt
            # trotzdem möglich via direktem deep-scan.
            continue
    if injected_any:
        _observer_injected[page] = url


async def scan_page(page) -> list[dict]:
    """
    Scannt eine Playwright-Page auf CAPTCHAs — Main-Frame UND alle
    Sub-Frames (inkl. cross-origin).

    Chrome's Site Isolation rendert cross-origin iframes in separaten
    Prozessen; `page.evaluate` ist auf den Main-Frame beschränkt. Über
    `page.frames` greift Playwright via CDP auf jeden Frame einzeln zu,
    was die Erkennung von reCAPTCHA / hCaptcha / Turnstile in deren
    eigenen iframes ermöglicht.

    Per-Frame-Ergebnisse werden über (name, solved) dedupliziert.
    Cross-origin oder detached Frames werden silent geskippt — das ist
    bei normalem Page-Lifecycle erwartet.

    Gibt zurück:
        [{"name": str, "solved": bool, "description": str,
          "_frame_url": str}, ...]
    """
    await _inject_observer(page)
    markers = _markers_for_page(page)
    all_results: list[dict] = []
    seen_keys: set[str] = set()

    frames = list(page.frames)  # main_frame ist Index 0
    for frame in frames:
        # Detached frames werfen on evaluate. is_detached() ist die
        # Playwright-API für sync check; bei dynamisch entfernten frames
        # zwischen list() und evaluate() fängt der try/except den Rest.
        try:
            if hasattr(frame, "is_detached") and frame.is_detached():
                continue
        except Exception:
            continue
        try:
            result = await frame.evaluate(_render(JS_DEEP_SCAN, markers))
        except Exception:
            # Cross-origin restrictions, navigation in flight, oder
            # CSP blockiert eval — alle erwartet, kein Loud-Print.
            continue
        if not isinstance(result, list):
            continue
        for cap in result:
            if not isinstance(cap, dict):
                continue
            key = f"{cap.get('name', '')}|{'1' if cap.get('solved') else '0'}"
            if not key.strip("|") or key in seen_keys:
                continue
            seen_keys.add(key)
            try:
                cap["_frame_url"] = frame.url
            except Exception:
                cap["_frame_url"] = ""
            all_results.append(cap)
    return all_results


MAX_SOLVER_RETRIES = 3

# Solver-Registry: erste matchende Regel gewinnt. Predicates bekommen
# (name_lower, desc_lower) und liefern bool. Neue Solver werden einfach
# durch Hinzufügen eines Tupels registriert — kein if/elif-Branching.
_SOLVER_ROUTES: list[tuple] = [
    # (predicate(name_lower, desc_lower), solver_module_name, human_label)
    (lambda n, d: "3d objects" in n or "identische objekte" in d,                "object_3d",    "TikTok 3D Objects"),
    (lambda n, d: "rotate" in n,                                                  "rotate",       "TikTok Rotate"),
    (lambda n, d: "puzzle slide" in n or "slide" in n or "geetest" in n,          "slide",        "Slide-basierte CAPTCHAs"),
    (lambda n, d: "recaptcha v2" in n,                                            "recapctha_v2", "reCAPTCHA v2"),
    (lambda n, d: ("text-captcha" in n) and any(p in n for p in ("meta", "instagram", "facebook")),
                                                                                   "meta_text",    "Meta Text-CAPTCHA"),
]


def _resolve_solver(name: str, desc: str) -> Optional[tuple[str, str]]:
    """Findet den passenden Solver für (name, description).

    Returns: (module_name, label) wenn match, sonst None.
    """
    n = (name or "").lower()
    d = (desc or "").lower()
    for predicate, module_name, label in _SOLVER_ROUTES:
        try:
            if predicate(n, d):
                return module_name, label
        except Exception:
            continue
    return None


async def auto_solve_captcha(cap: dict, page) -> bool:
    """
    Routet das Cap-Dict an den entsprechenden automatischen Solver via
    _SOLVER_ROUTES. Import läuft package-relativ (mit __package__) oder
    absolut als Fallback.
    """
    import importlib
    import asyncio

    name = cap.get("name", "")
    desc = cap.get("description", "")

    print(f"\n  🚀  [AutoSolver] Starte automatischen Lösungs-Prozess für: {name}")

    route = _resolve_solver(name, desc)
    if not route:
        print(f"  ⏭️  [AutoSolver] Kein passender Auto-Solver für '{name}' gefunden.")
        return False
    module_name, label = route

    def _import_solver(module: str):
        if __package__:
            return importlib.import_module(f"{__package__}.captchas_solver.{module}")
        return importlib.import_module(f"captchas_solver.{module}")

    for _attempt in range(MAX_SOLVER_RETRIES):
        try:
            solver_mod = _import_solver(module_name)
            solved = await solver_mod.solve(page)
            if solved:
                return True
            print(f"  ❌  [AutoSolver] {label} meldete ungelöst (Versuch {_attempt+1}/{MAX_SOLVER_RETRIES}).")
        except Exception as e:
            print(f"  ❌  [AutoSolver] {label} fehlgeschlagen (Versuch {_attempt+1}/{MAX_SOLVER_RETRIES}): {e}")
        if _attempt < MAX_SOLVER_RETRIES - 1:
            print(f"  ⏳  [AutoSolver] Warte 2s vor nächstem Versuch...")
            await asyncio.sleep(2)
    return False


# Network-Hint-Pattern: wenn eine Response auf diesen Strings matcht,
# wird ein verzögerter Re-Scan getriggert. Fängt Captchas ab, die nach
# DOMContentLoaded async via XHR/Fetch nachgeladen werden (typisch bei
# Cloudflare-Challenge-Pages, DataDome, hCaptcha-Lazy-Mount).
CAPTCHA_URL_HINTS: tuple[str, ...] = (
    "recaptcha", "hcaptcha", "/turnstile", "challenges.cloudflare.com",
    "geetest.com", "/captcha", "/__cf_chl",
    "datadome.co", "captcha-delivery.com",
    "perimeterx", "px-cdn", "px-cloud",
    "akamai/sensor", "akamai/akam",
    "smartcaptcha.yandexcloud", "yastatic.net/s3/passport",
    "awswaf.com", "token.awswaf.com",
    "verify.bytedance.com", "verification.bytedance.com",
)


async def live_scan(
    context,
    interval: float = SCAN_INTERVAL, # Veraltet, nur für Abwärtskompatibilität
    callback: Optional[Callable] = None,
    auto_solve: bool = True,
) -> None:
    """
    Dauerhafter Event-Driven Scan aller Pages in einem Playwright-BrowserContext.

    v9-Härtung (Chrome-Reliability):
      * `add_init_script` injiziert den Observer VOR allen Page-Scripts
        statt erst nach Navigation. Fängt damit Captchas ab, die im
        ersten Paint da sind.
      * Per-Frame Setup: alle Sub-Frames (cross-origin inklusive) werden
        durchgereicht statt nur Main-Frame.
      * Network-Hint-Listener: Response auf bekannte Captcha-URLs
        triggert verzögerten Re-Scan, damit XHR-spät-eingebundene
        Captchas nicht durchrutschen.

    Parameter:
        context   – playwright BrowserContext
        interval  – (deprecated, ignoriert)
        callback  – optionale async-Funktion:  async def cb(cap: dict, page) → None
        auto_solve - automatische Lösung
    """
    print(f"\n  🔄  Playwright Event-Driven Scanner v9")
    print("  Alle Pages im Context werden überwacht  –  Strg+C zum Beenden.\n")

    # Tracks (page_id, captcha_name+solved) gegen Re-Scan-Doppelmeldungen
    _handled_in_session: dict = {}

    async def handle_captcha(captcha_data: dict, page) -> None:
        name = captcha_data.get("name", "Unknown")
        page_id = id(page)
        dedup_key = f"{name}|{'1' if captcha_data.get('solved') else '0'}"
        seen = _handled_in_session.setdefault(page_id, set())
        if dedup_key in seen:
            return
        seen.add(dedup_key)

        title = ""
        try:
            title = await page.title()
        except Exception:
            pass

        _print_report([captcha_data], page.url, title, 1, len(context.pages))

        if auto_solve and not captcha_data.get("solved"):
            solved = await auto_solve_captcha(captcha_data, page)
            captcha_data["solved"] = solved
            if not solved:
                print(f"\n  ⚠️   [LiveScan] Solver für {name} fehlgeschlagen.")
            else:
                _clear_line()
                print(f"  ✅  [{_ts()}]  Gelöst: {name}")

        if callback:
            try:
                await callback(captcha_data, page)
            except Exception:
                pass

    # R1: no context.expose_binding() here. A bound window function is a
    # Playwright automation tell. The in-page observer now reports new
    # captchas via console.debug(prefix + json); each page's _on_console
    # listener (see setup_page) parses them. R3: the early-inject script
    # is registered per page (page.add_init_script with per-page markers)
    # instead of once on the context, so no marker is shared across pages.

    async def _delayed_rescan(page, delay_ms: int = 400) -> None:
        """Verzögerter Multi-Frame-Scan — wird von Network-Hints + Frame-Navs getriggert."""
        try:
            await asyncio.sleep(delay_ms / 1000)
            results = await scan_page(page)
            for cap in results:
                if isinstance(cap, dict):
                    await handle_captcha(cap, page)
        except Exception:
            pass

    async def setup_page(page):
        try:
            markers = _markers_for_page(page)
            prefix = markers["report"]

            def _on_console(msg):
                """R1 report channel: the in-page observer pushes newly
                found captchas via console.debug(prefix + json) instead
                of a Playwright expose_binding() (which would install a
                detectable window function). Parse those messages here
                and dispatch them like any other detection."""
                try:
                    text = msg.text
                except Exception:
                    return
                if not text or not text.startswith(prefix):
                    return
                try:
                    cap = json.loads(text[len(prefix):])
                except Exception:
                    return
                if not isinstance(cap, dict):
                    return
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    return
                try:
                    loop.create_task(handle_captcha(cap, page))
                except RuntimeError:
                    return

            # Attach the report listener before any scan so observer-driven
            # console reports are never missed.
            page.on("console", _on_console)

            # R3: per-page early-inject at document_start with this page's
            # own markers. Replaces the old context-level add_init_script
            # (which forced one shared marker across every page). Only
            # affects future navigations; _inject_observer below is the
            # fallback for frames that already loaded.
            try:
                await page.add_init_script(_render(JS_INJECT_OBSERVERS, markers))
            except Exception as e:
                print(f"  ⚠️   [Scanner] add_init_script (page) fehlgeschlagen: {e}")

            await _inject_observer(page)
            # Multi-Frame Initial-Scan (scan_page handelt Cross-Origin)
            initial_results = await scan_page(page)
            for cap in initial_results:
                if isinstance(cap, dict):
                    await handle_captcha(cap, page)

            # Per-page cooldowns: prevent task-flood under bursty events.
            # Minimum interval between rescans triggered by the same source.
            _last_response_rescan: list[float] = [0.0]
            _last_framenav_rescan: list[float] = [0.0]
            _last_load_rescan: list[float] = [0.0]
            _RESPONSE_COOLDOWN = 1.0
            _FRAMENAV_COOLDOWN = 0.5
            _LOAD_COOLDOWN = 0.5

            def _spawn_rescan(delay_ms: int) -> None:
                """Schedule _delayed_rescan defensively.

                Playwright sometimes fires events from threads/contexts where
                no asyncio loop is active. asyncio.create_task() would crash
                with RuntimeError; asyncio.get_event_loop() is deprecated in
                3.10+. Use get_running_loop() with a guarded fallback so the
                callback NEVER raises into Playwright's dispatcher (which
                would tear down the page).
                """
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    # No running loop on this thread — drop the rescan
                    # silently. The next observer-triggered scan will pick
                    # up the captcha eventually.
                    return
                try:
                    loop.create_task(_delayed_rescan(page, delay_ms=delay_ms))
                except RuntimeError:
                    # Loop closed mid-shutdown. Same fallback as above.
                    return

            def _on_response(response):
                try:
                    url = (response.url or "").lower()
                except Exception:
                    return
                if not any(h in url for h in CAPTCHA_URL_HINTS):
                    return
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    return
                now = loop.time()
                if now - _last_response_rescan[0] < _RESPONSE_COOLDOWN:
                    return
                _last_response_rescan[0] = now
                _spawn_rescan(500)

            def _on_framenavigated(frame):
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    return
                now = loop.time()
                if now - _last_framenav_rescan[0] < _FRAMENAV_COOLDOWN:
                    return
                _last_framenav_rescan[0] = now
                _spawn_rescan(300)

            def _on_load(_p=None):
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    return
                now = loop.time()
                if now - _last_load_rescan[0] < _LOAD_COOLDOWN:
                    return
                _last_load_rescan[0] = now
                _spawn_rescan(600)

            def _on_close(_p=None):
                # Alle Listener bereinigen, damit kein Leak entsteht wenn die Page
                # geschlossen wird. Danach Dedup-State für diese Page entfernen.
                for event, handler in (
                    ("response", _on_response),
                    ("framenavigated", _on_framenavigated),
                    ("load", _on_load),
                    ("console", _on_console),
                ):
                    try:
                        page.remove_listener(event, handler)
                    except Exception:
                        pass
                _handled_in_session.pop(id(page), None)

            # Network-Listener für Captcha-URLs (XHR-spät-Mounts abfangen)
            page.on("response", _on_response)
            # Frame-Navigation -> Observer in neue Frames injizieren
            page.on("framenavigated", _on_framenavigated)
            # Page-Load -> Re-scan (manche Sites mounten captcha bei load)
            page.on("load", _on_load)
            # Cleanup beim Schließen der Page
            page.once("close", _on_close)
        except Exception as e:
            print(f"  ⚠️   [Scanner] Setup-Fehler für Page {getattr(page, 'url', 'unknown')}: {e}")

    context.on("page", lambda page: asyncio.create_task(setup_page(page)))
    for page in context.pages:
        asyncio.create_task(setup_page(page))

    # Keep alive
    while True:
        await asyncio.sleep(3600)


# ══════════════════════════════════════════════════════════════════
#  CAMOUFOX-ADAPTER  (async + sync convenience wrappers)
# ══════════════════════════════════════════════════════════════════
#
# AsyncCamoufox / Camoufox return either a Browser (default) or a
# BrowserContext (when persistent_context=True). live_scan() needs a
# BrowserContext, so we normalize. Helpers honor every Camoufox launch
# kwarg via **camoufox_kwargs (proxy, locale, geolocation, os, …).

def _as_context(browser_or_context):
    """Normalize SYNC Camoufox return to a BrowserContext.

    Detection rule:
      - Browser has `.new_context()` and `.contexts`
      - BrowserContext does not have `.new_context`

    This helper is for sync Playwright/Camoufox launches only. Passing
    an AsyncBrowser here would silently return a coroutine and break
    the downstream `.new_page()` call — detect and refuse explicitly so
    the failure mode is obvious instead of `AttributeError: 'coroutine'
    object has no attribute 'new_page'`.
    """
    if hasattr(browser_or_context, "new_context"):
        if asyncio.iscoroutinefunction(browser_or_context.new_context):
            raise RuntimeError(
                "_as_context() received an AsyncBrowser; use "
                "_async_as_context() instead. The async/sync Camoufox "
                "APIs are not interchangeable."
            )
        # Browser: prefer existing context if Camoufox already created
        # one (some launch options do this), else create a fresh one.
        contexts = getattr(browser_or_context, "contexts", None) or []
        if contexts:
            return contexts[0]
        return browser_or_context.new_context()
    # BrowserContext: return as-is
    return browser_or_context


async def _async_as_context(browser_or_context):
    """Async variant — awaits new_context() if it's a Browser."""
    if hasattr(browser_or_context, "new_context"):
        contexts = getattr(browser_or_context, "contexts", None) or []
        if contexts:
            return contexts[0]
        return await browser_or_context.new_context()
    return browser_or_context


async def run_with_camoufox(
    url: str,
    *,
    headless=False,
    auto_solve: bool = True,
    callback: Optional[Callable] = None,
    **camoufox_kwargs,
) -> None:
    """Launch Camoufox, navigate, and run live_scan — async one-shot driver.

    Blocks until the scanner is interrupted (Ctrl-C / cancellation). All
    extra kwargs are forwarded to AsyncCamoufox (proxy, locale, os,
    geolocation, …).

    Example:
        import asyncio
        from scripts_macros.captcha import scanner
        asyncio.run(scanner.run_with_camoufox(
            "https://accounts.google.com/signin",
            headless=False,
            proxy={"server": "http://127.0.0.1:8888"},
            locale="de-DE",
        ))
    """
    try:
        from camoufox.async_api import AsyncCamoufox
    except ImportError as exc:
        raise RuntimeError(
            "camoufox.async_api is not importable. Install camoufox "
            "(`pip install camoufox`) or use the manual flow with raw "
            "Playwright Firefox."
        ) from exc

    async with AsyncCamoufox(headless=headless, **camoufox_kwargs) as launched:
        context = await _async_as_context(launched)
        page = await context.new_page()
        try:
            await page.goto(url)
        except Exception as exc:
            print(f"  ⚠️   [run_with_camoufox] goto({url!r}) failed: {exc}")
        await live_scan(context, auto_solve=auto_solve, callback=callback)


def scan_with_camoufox_sync(
    url: str,
    *,
    headless=False,
    wait_after_load_ms: int = 800,
    on_captcha: Optional[Callable] = None,
    **camoufox_kwargs,
) -> list[dict]:
    """Sync one-shot: launch Camoufox, navigate, scan, return results.

    For simple scripts that just want "does this page have a captcha?".
    Does NOT run live_scan (no continuous monitoring) and does NOT call
    the async auto-solvers. Use run_with_camoufox() for those.

    Args:
        url: page to navigate to
        headless: Camoufox headless flag (False / True / 'virtual')
        wait_after_load_ms: pause after page load before scanning, lets
            late-mounting captchas finish DOM-insertion
        on_captcha: optional callable(cap_dict, page) for each detected
        **camoufox_kwargs: forwarded to Camoufox(...)

    Returns: list of detected captcha dicts (with `_frame_url` per entry).
    """
    try:
        from camoufox.sync_api import Camoufox
    except ImportError as exc:
        raise RuntimeError(
            "camoufox.sync_api is not importable. Install camoufox "
            "(`pip install camoufox`) or use the async flow."
        ) from exc

    results: list[dict] = []
    seen: set[str] = set()

    with Camoufox(headless=headless, **camoufox_kwargs) as launched:
        context = _as_context(launched)
        page = context.new_page()
        try:
            page.goto(url)
        except Exception as exc:
            print(f"  ⚠️   [scan_with_camoufox_sync] goto({url!r}) failed: {exc}")
            return results

        if wait_after_load_ms > 0:
            try:
                page.wait_for_timeout(wait_after_load_ms)
            except Exception:
                pass

        # Inject observer in every frame, then evaluate JS_DEEP_SCAN in
        # every frame (mirrors async scan_page logic exactly).
        markers = _markers_for_page(page)
        for frame in list(page.frames):
            try:
                if hasattr(frame, "is_detached") and frame.is_detached():
                    continue
            except Exception:
                continue
            try:
                frame.evaluate(_render(JS_INJECT_OBSERVERS, markers))
            except Exception:
                pass
            try:
                frame_results = frame.evaluate(_render(JS_DEEP_SCAN, markers))
            except Exception:
                continue
            if not isinstance(frame_results, list):
                continue
            for cap in frame_results:
                if not isinstance(cap, dict):
                    continue
                key = f"{cap.get('name', '')}|{'1' if cap.get('solved') else '0'}"
                if not key.strip("|") or key in seen:
                    continue
                seen.add(key)
                try:
                    cap["_frame_url"] = frame.url
                except Exception:
                    cap["_frame_url"] = ""
                results.append(cap)
                if on_captcha:
                    try:
                        on_captcha(cap, page)
                    except Exception as exc:
                        print(f"  ⚠️   [on_captcha] callback raised: {exc}")
    return results


# ══════════════════════════════════════════════════════════════════
#  LEGACY CDP PATH  (Chrome-only, deprecated)
# ══════════════════════════════════════════════════════════════════

def _fetch_cdp_targets(host: str, port: int) -> list[dict]:
    """Liest die offenen CDP-Targets über das JSON-Endpoint aus."""
    endpoint = f"http://{host}:{port}/json/list"
    with urllib.request.urlopen(endpoint, timeout=CDP_RECV_TIMEOUT) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [target for target in payload if isinstance(target, dict)]


def live_scan_cdp(
    host: str = CDP_HOST,
    port: int = CDP_PORT,
    interval: float = SCAN_INTERVAL,
    callback: Optional[Callable] = None,
) -> None:
    """
    Legacy-Kompatibilitätsmodus für frühere CDP-basierte Aufrufer.

    Hinweis:
        Der eigentliche Deep-Scan benötigt heute Playwright-Page-Objekte und ist
        über `live_scan(context)` event-driven implementiert. Diese Funktion
        verhindert Alt-Aufrufer-Fehler und meldet den Zustand des CDP-Endpunkts.
    """
    print("\n  🔌  Legacy CDP-Scanner aktiviert")
    print("  Für den vollständigen Deep-Scan bitte `live_scan(context)` verwenden.\n")

    last_snapshot: tuple[str, ...] = ()

    while True:
        try:
            targets = _fetch_cdp_targets(host, port)
            page_targets = [
                target for target in targets
                if target.get("type") == "page"
            ]
            snapshot = tuple(
                sorted(
                    str(target.get("url", ""))
                    for target in page_targets
                    if target.get("url")
                )
            )

            if snapshot != last_snapshot:
                _clear_line()
                print(
                    f"  [{_ts()}]  CDP verbunden: {len(page_targets)} Page-Target(s) auf {host}:{port}"
                )
                for idx, url in enumerate(snapshot, 1):
                    print(f"    [{idx}] {url}")
                last_snapshot = snapshot

            if callback:
                try:
                    callback(
                        {
                            "host": host,
                            "port": port,
                            "targets": page_targets,
                            "timestamp": _ts(),
                        }
                    )
                except Exception:
                    pass

        except Exception as exc:
            _clear_line()
            print(f"  [{_ts()}]  CDP-Verbindung fehlgeschlagen ({host}:{port}): {exc}")

        time.sleep(max(interval, 1.0))

