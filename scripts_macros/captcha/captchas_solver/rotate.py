"""
captchas_solver/rotate.py
════════════════════════════════════════════════════════════════════
Solver für TikTok Rotate-CAPTCHAs (V1 + V2).

Mechanismus:
    Zwei konzentrische, kreisförmige Bilder. Das innere ist rotiert,
    der Nutzer muss es per Slider zurückdrehen. Das Vision-Modell
    schätzt den nötigen Pixel-Offset (auf der Slider-Track-Skala)
    und der Slider wird per humanized drag dorthin gezogen.

Verbesserungen ggü. v1:
  * Multi-Frame-Selektor-Suche.
  * V2-Selektoren ergänzt (draggable-div in .captcha-verify-container).
  * Humanized Drag via human_mouse.py (separat vom Browser).
  * Mehrere Success-Indikatoren statt naivem "knob noch da?".
"""

from __future__ import annotations
import asyncio
import os
import random
from typing import Optional

from playwright.async_api import Page

try:
    from .base_solver import AsyncCaptchaSolver
except (ImportError, ValueError):
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from base_solver import AsyncCaptchaSolver  # type: ignore

# ══════════════════════════════════════════════════════════════════
#  KONFIGURATION
# ══════════════════════════════════════════════════════════════════

ROTATE_KNOB_SELECTORS = [
    ".secsdk-captcha-drag-icon",                            # TikTok V1 (gleicher Slider wie Slide)
    ".captcha-verify-container div[draggable='true']",      # TikTok V2
    ".geetest_slider_button",                               # GeeTest Slider-Rotate
    "[class*='slider-handle' i]",
    "[class*='captcha-drag' i]",
]

ROTATE_TRACK_SELECTORS = [
    ".captcha_verify_slide--wrapper",                       # TikTok V1
    ".captcha-verify-container > div",                      # TikTok V2 (drag-bar parent)
    ".geetest_slider",
    "[class*='slider-track' i]",
    "[class*='captcha-track' i]",
]

# Spezifisch für Rotate: zwei Bilder müssen sichtbar sein.
ROTATE_IMAGE_SIGNALS = [
    "[data-testid='whirl-inner-img']",                      # TikTok V1
    "[data-testid='whirl-outer-img']",                      # TikTok V1
    ".captcha-verify-container > div > div > div > img.cap-absolute",  # V2 inner
]

SUCCESS_INDICATORS = [
    ".geetest_panel_success",
    ".secsdk-captcha-success",
    "[class*='captcha-success' i]",
    ".verify-success",
]

# Äußerster CAPTCHA-Container: enthält sowohl die konzentrischen Kreise als
# auch den Slider-Track. Dieser wird für den Screenshot verwendet.
ROTATE_CONTAINER_SELECTORS = [
    "#captcha_container",                              # TikTok V1 outer
    ".captcha_verify_container",                       # TikTok V1 inner
    ".captcha-verify-container",                       # TikTok V2
    ".geetest_panel_box",                              # GeeTest
    "[class*='captcha-container' i]",
    "[class*='captcha-wrap' i]",
    "[class*='captcha-box' i]",
]


class RotateSolver(AsyncCaptchaSolver):
    """Solver für Rotations-CAPTCHAs."""

    def __init__(self, page: Page):
        super().__init__(page)

    async def solve(self) -> bool:
        print("\n  🧩  [RotateSolver] Starte Rotate-CAPTCHA Solver…")

        # ── 1. Rotate-Indikator vorhanden? (sonst Slide oder anderer Typ) ──
        rotate_indicator = await self.find_selector_in_frames(ROTATE_IMAGE_SIGNALS)
        if not rotate_indicator:
            print("  ⚠️   [RotateSolver] Kein Rotate-Bild-Indikator (whirl-img/cap-absolute) gefunden — vermutlich ist das doch ein Slide- oder 3D-Captcha.")
            # Wir gehen trotzdem weiter, falls die Site Custom-Selektoren nutzt.

        # ── 2. Knob + Track finden ──────────────────────────────────
        knob_hit = await self.find_selector_in_frames(ROTATE_KNOB_SELECTORS)
        track_hit = await self.find_selector_in_frames(ROTATE_TRACK_SELECTORS)

        if not knob_hit or not track_hit:
            print("  ❌  [RotateSolver] Slider-Elemente nicht gefunden.")
            return False

        knob_frame, knob_sel = knob_hit
        track_frame, track_sel = track_hit

        knob = knob_frame.locator(knob_sel).first
        track = track_frame.locator(track_sel).first

        k_bbox = await knob.bounding_box()
        t_bbox = await track.bounding_box()

        if not k_bbox or not t_bbox:
            print("  ❌  [RotateSolver] BoundingBox konnte nicht ermittelt werden.")
            return False

        track_x_start = int(t_bbox["x"])
        track_width = int(t_bbox["width"])
        track_x_end = track_x_start + track_width

        print(f"  📌  [RotateSolver] Track: X={track_x_start}…{track_x_end} px")

        # ── 3. Screenshot des gesamten CAPTCHA-Containers (Kreise + Slider).
        #       screenshot_locator(track) würde nur den Slider-Balken zeigen —
        #       ohne die konzentrischen Kreise kann das Modell den Winkel nicht bestimmen.
        container_hit = await self.find_selector_in_frames(ROTATE_CONTAINER_SELECTORS)
        container_el = container_hit[0].locator(container_hit[1]).first if container_hit else None
        image_bytes = (
            (await self.screenshot_locator(container_el) if container_el else None)
            or await self.screenshot_fullpage()
        )
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompt_rotate.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
        except Exception as e:
            print(f"  ❌  [RotateSolver] Konnte prompt_rotate.txt nicht lesen: {e}")
            return False

        prompt = prompt.replace("[FÜGE HIER track_x_start EIN]", str(track_x_start))
        prompt = prompt.replace("[FÜGE HIER track_x_start + track_width EIN]", str(track_x_end))

        try:
            raw_response = await self.get_vision_response(image_bytes, prompt)
            print(f"  🤖  [RotateSolver] Vision-Antwort: {raw_response[:200]!r}")
            target_x = self.extract_target_x(raw_response)
        except Exception as e:
            print(f"  ❌  [RotateSolver] Vision-API-Fehler: {e}")
            return False

        if target_x is None:
            print("  ⚠️   [RotateSolver] Kein Target_X aus Antwort extrahierbar.")
            return False

        if not (track_x_start <= target_x <= track_x_end):
            print(f"  ⚠️   [RotateSolver] Target_X ({target_x}) außerhalb [{track_x_start},{track_x_end}], clampe.")
            target_x = max(track_x_start, min(target_x, track_x_end))

        print(f"  🎯  [RotateSolver] Ziel-X: {target_x}")

        # ── 4. Humanized Drag ───────────────────────────────────────
        start_x = k_bbox["x"] + k_bbox["width"] / 2
        start_y = k_bbox["y"] + k_bbox["height"] / 2
        end_y = start_y + random.uniform(-2.0, 2.0)

        print(f"  🖱️   [RotateSolver] Drag von ({start_x:.0f},{start_y:.0f}) nach ({target_x},{end_y:.0f})…")
        await self.humanized_drag((start_x, start_y), (float(target_x), end_y))

        await asyncio.sleep(random.uniform(1.8, 2.8))

        # ── 5. Success-Check ────────────────────────────────────────
        success_hit = await self.find_selector_in_frames(SUCCESS_INDICATORS)
        if success_hit:
            print(f"  🎉  [RotateSolver] CAPTCHA gelöst (Indikator: {success_hit[1]}).")
            return True

        knob_still = await self.find_selector_in_frames(ROTATE_KNOB_SELECTORS)
        if not knob_still:
            print("  🎉  [RotateSolver] CAPTCHA vermutlich gelöst (Knob nicht mehr sichtbar).")
            return True

        print("  ❌  [RotateSolver] Versuch fehlgeschlagen.")
        return False


async def solve(page: Page) -> bool:
    solver = RotateSolver(page)
    return await solver.solve()
