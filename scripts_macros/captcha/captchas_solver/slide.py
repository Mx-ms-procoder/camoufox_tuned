"""
captchas_solver/slide.py
════════════════════════════════════════════════════════════════════
Solver für Puzzle-Slide-CAPTCHAs (TikTok V1/V2, GeeTest, Alibaba …).

Verbesserungen ggü. v1:
  * Multi-Frame-Selektor-Suche — Captchas in cross-origin iframes
    (Standardfall) werden jetzt überhaupt gefunden.
  * Humanized Drag via human_mouse.py (Bezier + Distortion +
    easeOutQuad-Easing — separat vom Browser).
  * Robusterer Success-Check (mehrere Indikatoren statt "knob noch da?").
  * Sub-Region-Screenshot wenn möglich (effizienter Vision-Call).
"""

from __future__ import annotations
import asyncio
import os
import random
from typing import Optional

from playwright.async_api import Page

# Relative imports with fallback for direct execution
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

SLIDE_KNOB_SELECTORS = [
    ".secsdk-captcha-drag-icon",                              # TikTok V1
    ".captcha-verify-container div[draggable='true']",        # TikTok V2
    ".geetest_slider_button",                                 # GeeTest
    ".nc_iconfont.btn_slide",                                 # Alibaba
    ".slide-to-unlock-handle",                                # Generic
    "[class*='slider-handle' i]",
    "[class*='captcha-drag' i]",
]

SLIDE_TRACK_SELECTORS = [
    ".captcha_verify_slide--wrapper",                         # TikTok V1
    ".captcha-verify-container > div",                        # TikTok V2 (drag-bar parent)
    ".geetest_slider",                                        # GeeTest
    ".nc-lang-cnt",                                           # Alibaba
    ".slide-to-unlock-bg",                                    # Generic
    "[class*='slider-track' i]",
    "[class*='captcha-track' i]",
]

# Success-Indikatoren (positive Signale, nicht nur "knob weg")
SUCCESS_INDICATORS = [
    ".geetest_panel_success",
    ".geetest_success_radar_tip",
    ".secsdk-captcha-success",
    "[class*='captcha-success' i]",
    ".verify-success",
]

# Äußerster CAPTCHA-Container: enthält sowohl das Puzzle-Bild als auch den
# Slider-Track. Dieses Element wird für den Screenshot verwendet, damit das
# Vision-Modell Bild UND Slider gleichzeitig sieht.
SLIDE_CONTAINER_SELECTORS = [
    "#captcha_container",                              # TikTok V1 outer
    ".captcha_verify_container",                       # TikTok V1 inner
    ".captcha-verify-container",                       # TikTok V2
    ".geetest_panel_box",                              # GeeTest
    ".geetest_panel",                                  # GeeTest alt
    "[class*='captcha-container' i]",
    "[class*='captcha-wrap' i]",
    "[class*='captcha-box' i]",
]


class SlideSolver(AsyncCaptchaSolver):
    """Solver für Puzzle-Slide-CAPTCHAs."""

    def __init__(self, page: Page):
        super().__init__(page)

    async def solve(self) -> bool:
        print("\n  🧩  [SlideSolver] Starte Slide-CAPTCHA Solver…")

        # ── 1. Knob + Track in irgendeinem Frame finden ─────────────
        knob_hit = await self.find_selector_in_frames(SLIDE_KNOB_SELECTORS)
        track_hit = await self.find_selector_in_frames(SLIDE_TRACK_SELECTORS)

        if not knob_hit or not track_hit:
            print("  ❌  [SlideSolver] Slider-Elemente in keinem Frame gefunden.")
            return False

        knob_frame, knob_sel = knob_hit
        track_frame, track_sel = track_hit

        knob = knob_frame.locator(knob_sel).first
        track = track_frame.locator(track_sel).first

        k_bbox = await knob.bounding_box()
        t_bbox = await track.bounding_box()

        if not k_bbox or not t_bbox:
            print("  ❌  [SlideSolver] BoundingBox konnte nicht ermittelt werden.")
            return False

        # Cross-frame: bounding_box gibt Koordinaten relativ zum Viewport
        # zurück. Frames in iframes liefern bereits absolute Werte
        # (Playwright handelt das). Also einfach direkt nutzen.
        track_x_start = int(t_bbox["x"])
        track_width = int(t_bbox["width"])
        track_x_end = track_x_start + track_width

        print(f"  📍  [SlideSolver] Track: X={track_x_start}…{track_x_end} px (Breite {track_width})")

        # ── 2. Screenshot des gesamten CAPTCHA-Containers (Bild + Slider).
        #       screenshot_locator(track) würde nur den Slider-Balken zeigen —
        #       das Modell sähe kein Puzzle und könnte nichts bestimmen.
        #       Container-BoundingBox wird für die Koordinaten-Formel im Prompt
        #       benötigt (image_width ≠ track_width wenn der Container Padding hat).
        container_hit = await self.find_selector_in_frames(SLIDE_CONTAINER_SELECTORS)
        container_el = container_hit[0].locator(container_hit[1]).first if container_hit else None
        container_bbox = await container_el.bounding_box() if container_el else None
        if container_bbox:
            c_x = int(container_bbox["x"])
            c_x_end = c_x + int(container_bbox["width"])
        else:
            # Fallback: Container-Koords = Track-Koords (gleiche Breite angenommen)
            c_x = track_x_start
            c_x_end = track_x_end
        image_bytes = (
            (await self.screenshot_locator(container_el) if container_el else None)
            or await self.screenshot_fullpage()
        )
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompt_slide.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
        except Exception as e:
            print(f"  ❌  [SlideSolver] Konnte prompt_slide.txt nicht lesen: {e}")
            return False

        prompt = prompt.replace("[CONTAINER_X_START]", str(c_x))
        prompt = prompt.replace("[CONTAINER_X_END]", str(c_x_end))
        prompt = prompt.replace("[TRACK_X_START]", str(track_x_start))
        prompt = prompt.replace("[TRACK_X_END]", str(track_x_end))

        try:
            raw_response = await self.get_vision_response(image_bytes, prompt)
            print(f"  🤖  [SlideSolver] Vision-Antwort: {raw_response[:200]!r}")
            target_x = self.extract_target_x(raw_response)
        except Exception as e:
            print(f"  ❌  [SlideSolver] Vision-API-Fehler: {e}")
            return False

        if target_x is None:
            print("  ⚠️   [SlideSolver] Kein Target_X aus Antwort extrahierbar.")
            return False

        if not (track_x_start <= target_x <= track_x_end):
            print(f"  ⚠️   [SlideSolver] Target_X ({target_x}) außerhalb [{track_x_start},{track_x_end}].")
            # Clamp statt abort
            target_x = max(track_x_start, min(target_x, track_x_end))
            print(f"  ↪️   [SlideSolver] auf {target_x} gec­lampt.")

        print(f"  🎯  [SlideSolver] Ziel-X: {target_x}")

        # ── 3. Humanized Drag ───────────────────────────────────────
        start_x = k_bbox["x"] + k_bbox["width"] / 2
        start_y = k_bbox["y"] + k_bbox["height"] / 2
        # Y mit minimalem Jitter — echte Slider-Bewegung ist nie 100 %
        # horizontal (Hand-Mikrotremor).
        end_y = start_y + random.uniform(-2.0, 2.0)

        print(f"  🖱️   [SlideSolver] Drag von ({start_x:.0f},{start_y:.0f}) nach ({target_x},{end_y:.0f})…")
        await self.humanized_drag((start_x, start_y), (float(target_x), end_y))

        # Validierung dauert oft 1-3 Sekunden
        await asyncio.sleep(random.uniform(1.5, 2.5))

        # ── 4. Success-Check (mehrstufig) ───────────────────────────
        # Positive Indikatoren zuerst (zuverlässiger als "knob weg")
        success_hit = await self.find_selector_in_frames(SUCCESS_INDICATORS)
        if success_hit:
            print(f"  🎉  [SlideSolver] CAPTCHA gelöst (Success-Indikator: {success_hit[1]}).")
            return True

        # Fallback: ist der Knob noch sichtbar?
        knob_still = await self.find_selector_in_frames(SLIDE_KNOB_SELECTORS)
        if not knob_still:
            print("  🎉  [SlideSolver] CAPTCHA vermutlich gelöst (Knob nicht mehr sichtbar).")
            return True

        print("  ❌  [SlideSolver] Versuch fehlgeschlagen.")
        return False


async def solve(page: Page) -> bool:
    solver = SlideSolver(page)
    return await solver.solve()
