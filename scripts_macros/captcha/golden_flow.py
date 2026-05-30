"""
golden_flow.py  –  Anti-Bot Stealth für Playwright  (Performance-Edition)
══════════════════════════════════════════════════════════════════════════
Identische Stealth-Layer wie die vorherige Version, aber ohne die
massiven Performance-Probleme durch Proxy-Wrapping.

Warum die alte Version laggte (und was geändert wurde):
  ❌ VORHER: Function.prototype.toString = new Proxy(nativeToString, {...})
     → Jeder JS-Funktionsaufruf im Browser lief durch einen Proxy-Trap.
     → V8 kann Proxy-Objekte nicht JIT-optimieren → dramatischer FPS-Einbruch.

  ❌ VORHER: cloak(fn) → Proxy für JEDE ersetzte Funktion
     → WebGLRenderingContext.prototype.getParameter wird bei jedem Frame
       hunderte Male aufgerufen. Als Proxy: kein JIT, 10-100x langsamer.

  ❌ VORHER: 2 separate CDPSessions pro Page (Network + WebRTC)
     → Doppelter CDP-Handshake-Overhead bei jedem neuen Tab.

  ✅ JETZT: Direkte Prototyp-Ersetzung via gespeichertem Original-Ref
     → Normales JS, voll JIT-optimierbar, kein Proxy-Overhead.

  ✅ JETZT: toString-Schutz nur für die wenigen ersetzten Fns, nicht global
     → Object.defineProperty statt Proxy.

  ✅ JETZT: Eine kombinierte CDPSession pro Page.

  ✅ JETZT: Chrome-Args bereinigt (keine Args die GPU/Rendering blockieren).

Stealth-Layer:
  Layer 1 – Camoufox Native Fingerprinting (Ersetzt alte CDP-Hacks)
  Layer 2 – BehavioralHelper     (Maus, Scroll, Typing)

Nutzung:
        flow = GoldenFlow()
        browser, context = await flow.create_browser(pw)
        page   = await flow.new_page(context)
        await page.mouse.move(100, 100, steps=20)

Benötigt:
    pip install playwright numpy
    playwright install chromium
"""

from __future__ import annotations

import asyncio
import math
import random
import re
from typing import Literal, Optional

try:
    from playwright.async_api import (
        async_playwright,
        Browser,
        BrowserContext,
        Page,
    )
except ImportError:
    raise SystemExit(
        "❌  Playwright fehlt:  pip install playwright"
    )


# ══════════════════════════════════════════════════════════════════
#  KONFIGURATION
# ══════════════════════════════════════════════════════════════════

WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 900

# ══════════════════════════════════════════════════════════════════
#  GOLDEN FLOW  –  Haupt-Klasse
# ══════════════════════════════════════════════════════════════════

class GoldenFlow:
    """
    Orchestriert alle Stealth-Layer für einen Playwright-Browser.

    Empfohlene Nutzung (Context-Manager, kein Browser-Leak bei Fehlern):
        async with GoldenFlow(headless=False).launch(pw) as (browser, context):
            page = await context.new_page()
            ...
        # Browser & Context werden hier automatisch geschlossen.

    Legacy-Nutzung (manuelle Cleanup-Verantwortung):
        flow = GoldenFlow()
        browser, context = await flow.create_browser(pw)
        try:
            page = await flow.new_page(context)
        finally:
            await browser.close()
    """

    def __init__(
        self,
        headless:   bool = False,
    ) -> None:
        self.headless   = headless
        self._browser:  Optional[Browser]        = None
        self._context:  Optional[BrowserContext] = None

    async def create_browser(self, pw) -> tuple[Browser, BrowserContext]:
        """
        Startet Camoufox. Gibt (Browser, BrowserContext) zurück.
        """
        print(f"\n  🚀  [GoldenFlow] Starte Camoufox Stealth-Browser…")

        try:
            from camoufox.async_api import AsyncNewBrowser  # type: ignore
        except ImportError:
            raise SystemExit("❌  Camoufox fehlt: pip install camoufox")

        browser = await AsyncNewBrowser(pw, headless=self.headless)
        try:
            context = await browser.new_context(
                no_viewport=True,
                java_script_enabled=True,
            )
        except Exception:
            # If context creation fails after the browser process is up,
            # the browser would leak. Close it explicitly before
            # propagating the exception.
            try:
                await browser.close()
            except Exception:
                pass
            raise

        # Rotate per-session JS markers so every new context gets unique
        # window property names — prevents cross-session fingerprinting.
        try:
            from scripts_macros.captcha.scanner import _regenerate_session_markers
            _regenerate_session_markers()
        except ImportError:
            pass

        self._browser = browser
        self._context = context
        print("  ✅  [GoldenFlow] Camoufox erstellt (Natives Stealthing).")
        return browser, context

    def launch(self, pw) -> "_GoldenFlowSession":
        """Returns an async context manager that owns the launched browser.

        Use this instead of create_browser() when you want guaranteed
        cleanup on exception — the previous bare create_browser() leaked
        a Firefox process whenever the caller forgot to wrap the result
        in try/finally.
        """
        return _GoldenFlowSession(self, pw)

    async def aclose(self) -> None:
        """Close the browser+context owned by this GoldenFlow (idempotent)."""
        if self._context is not None:
            try:
                await self._context.close()
            except Exception:
                pass
            self._context = None
        if self._browser is not None:
            try:
                await self._browser.close()
            except Exception:
                pass
            self._browser = None


class _GoldenFlowSession:
    """Async context manager for GoldenFlow.launch()."""

    def __init__(self, flow: "GoldenFlow", pw) -> None:
        self._flow = flow
        self._pw = pw

    async def __aenter__(self) -> tuple[Browser, BrowserContext]:
        return await self._flow.create_browser(self._pw)

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._flow.aclose()

    async def new_page(self, context: BrowserContext) -> Page:
        page = await context.new_page()
        await self.maximize_window(page)
        return page

    async def maximize_window(self, page: Page) -> None:
        """Maximizes the window via JS (Juggler/Firefox-compatible)."""
        try:
            await page.evaluate(
                "() => { window.moveTo(0, 0); "
                "window.resizeTo(screen.availWidth, screen.availHeight); }"
            )
        except Exception as e:
            print(f"  ⚠️   [GoldenFlow] Konnte Fenster nicht maximieren: {e}")

async def _run_test() -> None:
    test_url = "https://bot.sannysoft.com/"

    print("\n" + "═" * 60)
    print("  🔍  GoldenFlow Stealth-Test (Performance-Edition)")
    print("═" * 60)

    async with async_playwright() as pw:
        flow             = GoldenFlow(headless=False)
        browser, context = await flow.create_browser(pw)
        page             = await flow.new_page(context)
        await page.goto(test_url, wait_until="domcontentloaded")
        await page.mouse.wheel(0, 800)

        print("\n  ✅  Ergebnisse sichtbar.")
        print("     Grün = gut  |  Rot = Bot-Signal erkannt\n")
        input("  ⏎  Enter zum Beenden …")

        await browser.close()


def main() -> None:
    print("🚀  [GoldenFlow] Starte Stealth-Test…")
    try:
        asyncio.run(_run_test())
    except KeyboardInterrupt:
        print("\n  👋  Abgebrochen.")


if __name__ == "__main__":
    main()
