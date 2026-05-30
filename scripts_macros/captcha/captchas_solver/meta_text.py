"""
captchas_solver/meta_text.py
════════════════════════════════════════════════════════════════════
Text-CAPTCHA-Solver für Meta-Plattformen (Instagram + Facebook).

Verbesserungen ggü. v1:
  * Reales NVIDIA-NIM-Modell (`qwen/qwen2.5-vl-72b-instruct` per Default,
    via env NVIDIA_CAPTCHA_MODEL überschreibbar).
  * Multi-Frame-Lookup für Input + Submit (manche Checkpoint-Pages
    bauen das Formular in ein Sub-Frame).
  * Wartet auf network-idle nach Submit statt blindem sleep(3).
  * Erweiterte Erfolg-/Fehlermeldung-Erkennung.
  * Humanized Typing-Pausen (war schon vorhanden, beibehalten).
"""

from __future__ import annotations
import asyncio
import os
import random
import re
from typing import List, Optional, Tuple

from playwright.async_api import Page, Frame

try:
    from .base_solver import (
        get_nvidia_vision_response,
        NVIDIA_API_KEY_Qwen,
        NVIDIA_MODEL,
        require_external_captcha_allowed,
    )
except (ImportError, ValueError):
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from base_solver import (  # type: ignore
        get_nvidia_vision_response,
        NVIDIA_API_KEY_Qwen,
        NVIDIA_MODEL,
        require_external_captcha_allowed,
    )

# ══════════════════════════════════════════════════════════════════
#  KONFIGURATION
# ══════════════════════════════════════════════════════════════════

CAPTCHA_IMAGE_SELECTORS: list[str] = [
    "img#captcha_image", "img[src*='captcha']", "#captcha img",
    "form[action*='captcha'] img", "#captcha_response_wrapper img",
    "img[src*='checkpoint']", "form[action*='checkpoint'] img",
    "img[alt*='captcha' i]", "img[id*='captcha' i]",
    "img[class*='captcha' i]", "canvas[id*='captcha' i]",
]

CAPTCHA_INPUT_SELECTORS: list[str] = [
    "input[name='captcha_response']", "input[name='captcha_token']",
    "input[name='captcha_sid']",
    "input[id*='captcha' i]:not([type='hidden'])",
    "input[name*='captcha' i]:not([type='hidden'])",
    "#captcha_input",
    "input[placeholder*='code' i]",
    "input[placeholder*='text' i]",
    "input[aria-label*='captcha' i]",
]

SUBMIT_SELECTORS: list[str] = [
    "button[type='submit']",
    "input[type='submit']",
    "button:has-text('Weiter')",
    "button:has-text('Continue')",
    "button:has-text('Bestätigen')",
    "button:has-text('Confirm')",
    "button:has-text('Absenden')",
    "button:has-text('Submit')",
    "button:has-text('OK')",
    "[data-testid='submit-button']",
]

SUCCESS_SIGNALS = ["/home", "/feed", "?next=", "accounts/onetap"]
ERROR_SIGNALS = [
    "incorrect", "wrong", "ungültig", "falsch",
    "try again", "erneut versuchen", "doesn't match", "stimmt nicht überein",
]


class MetaTextSolver:
    """Spezialisierter Solver für Meta Text-CAPTCHAs.

    Eigenständig (nicht von AsyncCaptchaSolver erbend), aber nutzt
    dieselben NVIDIA-NIM-Defaults und Multi-Frame-Logik.
    """

    def __init__(self, page: Page, model: Optional[str] = None):
        require_external_captcha_allowed("NVIDIA NIM Vision")
        self.page = page
        self.api_key = NVIDIA_API_KEY_Qwen
        self.model = model or os.environ.get("NVIDIA_CAPTCHA_MODEL", NVIDIA_MODEL)

    async def solve(self) -> bool:
        print("\n  🧩  [MetaSolver] Starte Text-CAPTCHA Solver (Meta)…")

        url = self.page.url
        platform = "Instagram" if "instagram" in url else "Facebook"

        # ── 1. Screenshot — bevorzuge CAPTCHA-Bild-Element (kein PII) ──
        image_bytes = None
        captcha_img_hit = await self._find_in_frames(CAPTCHA_IMAGE_SELECTORS)
        if captcha_img_hit:
            img_frame, img_sel = captcha_img_hit
            img_loc = img_frame.locator(img_sel).first
            try:
                image_bytes = await img_loc.screenshot(type="png")
            except Exception:
                image_bytes = None
        if not image_bytes:
            # R2: viewport-only fallback (not full_page) — the captcha is
            # on screen and a full-page capture would egress unrelated PII
            # below the fold to the third-party vision API.
            image_bytes = await self.page.screenshot(type="png", full_page=False)
        if not image_bytes:
            print("  ❌  [MetaSolver] Screenshot fehlgeschlagen.")
            return False

        # ── 2. Vision-Call ─────────────────────────────────────────
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompt_meta.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
        except Exception as e:
            print(f"  ❌  [MetaSolver] Konnte prompt_meta.txt nicht lesen: {e}")
            return False

        prompt = f"Platform: {platform}. " + prompt

        try:
            raw_response = await get_nvidia_vision_response(
                image_bytes=image_bytes,
                prompt=prompt,
                api_key=self.api_key,
                model=self.model,
                temperature=0.0,
                top_p=1.0,
            )
            print(f"  🤖  [MetaSolver] Vision-Antwort: {raw_response[:200]!r}")
        except Exception as e:
            print(f"  ❌  [MetaSolver] Vision-API-Fehler: {e}")
            return False

        captcha_code = self._extract_code(raw_response)
        if not captcha_code:
            print("  ⚠️   [MetaSolver] Kein Code aus Antwort extrahierbar.")
            return False
        print(f"  ✅  [MetaSolver] Extrahierter Code: {captcha_code!r}")

        # ── 3. Input-Feld finden (multi-frame) + tippen ─────────────
        input_hit = await self._find_in_frames(CAPTCHA_INPUT_SELECTORS)
        if not input_hit:
            print("  ❌  [MetaSolver] Kein Eingabefeld in irgendeinem Frame gefunden.")
            return False
        in_frame, in_sel = input_hit

        before_url = self.page.url
        await self._human_type_in_frame(in_frame, in_sel, captcha_code)
        await asyncio.sleep(random.uniform(0.4, 0.9))

        # ── 4. Senden + auf Navigation/Network-idle warten ─────────
        await self._submit_form(in_frame)

        # Beste Heuristik: warten bis network idle ODER 6s timeout.
        try:
            await self.page.wait_for_load_state("networkidle", timeout=6000)
        except Exception:
            # Manche Single-Page-Apps werden nicht idle; einfach kurz warten
            await asyncio.sleep(2.0)

        # ── 5. Erfolg prüfen ────────────────────────────────────────
        success = await self._check_success(before_url)
        if success:
            print(f"  🎉  [MetaSolver] CAPTCHA ({platform}) gelöst.")
        else:
            print(f"  ❌  [MetaSolver] CAPTCHA-Versuch fehlgeschlagen.")
        return success

    # ── Helpers ────────────────────────────────────────────────────

    async def _find_in_frames(
        self, selectors: List[str]
    ) -> Optional[Tuple[Frame, str]]:
        """Sucht den ersten sichtbaren Selektor in irgendeinem Frame."""
        for frame in list(self.page.frames):
            try:
                if hasattr(frame, "is_detached") and frame.is_detached():
                    continue
            except Exception:
                continue
            for sel in selectors:
                try:
                    elem = frame.locator(sel).first
                    if await elem.is_visible(timeout=1500):
                        return (frame, sel)
                except Exception:
                    continue
        return None

    def _extract_code(self, raw_response: str) -> str:
        """Mehrstufige Code-Extraktion.

        1. Primary: 'Line: XXXXXX' (vom Prompt gefordert)
        2. Sechs-stellige Ziffernfolge (Standard-Meta-Format)
        3. 4-10 stellige Ziffernfolge
        4. Alpha-numeric Fallback
        """
        m = re.search(r"Line:\s*([A-Za-z0-9]{4,10})", raw_response, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        m = re.search(r"\b(\d{6})\b", raw_response)
        if m:
            return m.group(1)
        m = re.search(r"\b(\d{4,10})\b", raw_response)
        if m:
            return m.group(1)
        cleaned = re.sub(r"[^A-Za-z0-9]", "", raw_response)
        return cleaned[:10] if cleaned else ""

    async def _human_type_in_frame(
        self, frame: Frame, selector: str, text: str
    ) -> None:
        """Tippt mit menschlichen Pausen ins gefundene Input-Feld."""
        # Erst leeren, dann Char für Char tippen
        try:
            await frame.locator(selector).first.fill("")
        except Exception:
            pass
        try:
            await frame.locator(selector).first.click()
        except Exception:
            pass
        for ch in text:
            try:
                await self.page.keyboard.type(ch)
            except Exception:
                # Fallback: direkt ins Element
                try:
                    await frame.locator(selector).first.press(ch)
                except Exception:
                    pass
            await asyncio.sleep(random.uniform(0.07, 0.22))

    async def _submit_form(self, in_frame: Frame) -> None:
        """Click Submit oder press Enter im Input-Feld."""
        # 1. Versuche Submit-Button im gleichen Frame wie das Input
        for sel in SUBMIT_SELECTORS:
            try:
                btn = in_frame.locator(sel).first
                if await btn.is_visible(timeout=800):
                    await btn.click()
                    return
            except Exception:
                continue
        # 2. Fallback: in anderen Frames
        hit = await self._find_in_frames(SUBMIT_SELECTORS)
        if hit:
            frame, sel = hit
            try:
                await frame.locator(sel).first.click()
                return
            except Exception:
                pass
        # 3. Letzter Versuch: Enter im Input
        try:
            await self.page.keyboard.press("Enter")
        except Exception:
            pass

    async def _check_success(self, before_url: str) -> bool:
        """Mehrstufige Success-Detection."""
        current_url = self.page.url
        if current_url != before_url:
            # URL-Wechsel → vermutlich weitergekommen
            if any(sig in current_url for sig in SUCCESS_SIGNALS):
                return True
            if (
                "captcha" not in current_url.lower()
                and "checkpoint" not in current_url.lower()
            ):
                return True

        # Fehlermeldungen im Body?
        try:
            body_text = (await self.page.inner_text("body", timeout=2000)).lower()
            if any(sig in body_text for sig in ERROR_SIGNALS):
                return False
        except Exception:
            pass

        # Input-Feld noch da? → Captcha noch aktiv → vermutlich fail
        input_hit = await self._find_in_frames(CAPTCHA_INPUT_SELECTORS)
        return input_hit is None


async def solve(page: Page) -> bool:
    solver = MetaTextSolver(page)
    return await solver.solve()
