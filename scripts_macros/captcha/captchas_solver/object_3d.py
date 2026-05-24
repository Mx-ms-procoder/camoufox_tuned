"""
captchas_solver/object_3d.py
════════════════════════════════════════════════════════════════════
Solver für "Identische 3D-Objekte"-Captchas (TikTok V1/V2, GeeTest-Icons).

Verbesserungen ggü. v1:
  * Reales NVIDIA-NIM-Modell `google/gemma-3-27b-it` (statt der
    nicht-existenten ID "google/gemma-4-31b-it" — JEDER Vision-Call
    bekam vorher 404).
  * Liest die Anweisungstext-DOM-Box (.captcha_verify_bar / V2-Span)
    und übergibt sie ans Modell, damit die Klick-Reihenfolge stimmt.
  * Multi-Frame-Selektor-Suche.
  * Humanized Clicks via human_mouse.py (Bezier-Trajektorie, Jitter,
    Hold-Dauer).
  * V1- und V2-Submit-Buttons erkannt (.verify-captcha-submit-button,
    button.cap-w-full).
"""

from __future__ import annotations
import asyncio
import os
import random
import re
from typing import List, Optional, Tuple

from playwright.async_api import Page

try:
    from .base_solver import (
        AsyncCaptchaSolver,
        get_nvidia_vision_response,
        GEMMA_VISION_MODEL_DEFAULT,
    )
except (ImportError, ValueError):
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from base_solver import (  # type: ignore
        AsyncCaptchaSolver,
        get_nvidia_vision_response,
        GEMMA_VISION_MODEL_DEFAULT,
    )

# ══════════════════════════════════════════════════════════════════
#  KONFIGURATION
# ══════════════════════════════════════════════════════════════════

OBJECT_3D_SELECTORS = [
    ".captcha_verify_img--wrapper",                          # TikTok V1
    ".captcha-verify-container div.cap-relative",            # TikTok V2 image wrapper
    ".geetest_table_box",                                    # GeeTest Icons
    ".captcha-box",                                          # Generic
    "[id*='captcha-box' i]",
]

INSTRUCTION_SELECTORS = [
    ".captcha_verify_bar",                                   # TikTok V1
    ".captcha-verify-container > div > div > span",          # TikTok V2
    ".captcha_verify_message",
    "[class*='instruction' i]",
]

SUBMIT_SELECTORS = [
    ".verify-captcha-submit-button",                         # TikTok V1
    ".captcha-verify-container .cap-relative button.cap-w-full",  # TikTok V2
    ".geetest_commit",                                       # GeeTest
    ".captcha_submit_btn",                                   # Generic
    "button[class*='submit' i][class*='captcha' i]",
]

SUCCESS_INDICATORS = [
    ".geetest_panel_success",
    ".secsdk-captcha-success",
    "[class*='captcha-success' i]",
    ".verify-success",
]


class Object3DSolver(AsyncCaptchaSolver):
    """Solver für "Finde identische Objekte"-CAPTCHAs.

    Nutzt Gemma-3-Vision (auf NVIDIA NIM) für die Koordinaten-Schätzung
    UND die Reihenfolge-Bestimmung. Klicks erfolgen über humanized_click
    (Bezier-Trajektorie, Mikro-Jitter, Hold-Dauer).
    """

    def __init__(self, page: Page, model: Optional[str] = None):
        # Default: real existing NVIDIA-NIM Gemma-3 Vision model. Operator
        # kann via env override (NVIDIA_CAPTCHA_GEMMA_MODEL) auf eine
        # andere Variante schwenken.
        model_id = model or os.environ.get(
            "NVIDIA_CAPTCHA_GEMMA_MODEL", GEMMA_VISION_MODEL_DEFAULT
        )
        super().__init__(page, model=model_id)

    async def _read_instruction(self) -> Optional[str]:
        """Liest die Aufgaben-Anweisung aus dem DOM (Reihenfolge der Klicks).

        Wenn die Site sagt "Klicke auf das A, dann das B", muss das Modell
        diese Reihenfolge kennen — sonst klickt es zwar passende Objekte,
        aber falsch geordnet.
        """
        hit = await self.find_selector_in_frames(INSTRUCTION_SELECTORS)
        if not hit:
            return None
        frame, sel = hit
        try:
            text = await frame.locator(sel).first.inner_text(timeout=2000)
            return text.strip()
        except Exception:
            return None

    async def solve(self) -> bool:
        print(f"\n  🧩  [Object3DSolver] Starte 3D-Objects-Solver (Modell: {self.model})…")

        # ── 1. Captcha-Box finden ───────────────────────────────────
        box_hit = await self.find_selector_in_frames(OBJECT_3D_SELECTORS)
        if not box_hit:
            print("  ❌  [Object3DSolver] Captcha-Box in keinem Frame gefunden.")
            return False

        box_frame, box_sel = box_hit
        box = box_frame.locator(box_sel).first
        bbox = await box.bounding_box()
        if not bbox:
            print("  ❌  [Object3DSolver] BoundingBox nicht ermittelbar.")
            return False

        box_x = int(bbox["x"])
        box_y = int(bbox["y"])
        box_x_end = box_x + int(bbox["width"])
        box_y_end = box_y + int(bbox["height"])
        print(f"  📌  [Object3DSolver] Box: ({box_x},{box_y}) → ({box_x_end},{box_y_end})")

        # ── 2. Anweisungstext lesen ─────────────────────────────────
        instruction = await self._read_instruction()
        if instruction:
            print(f"  📝  [Object3DSolver] Anweisung: {instruction!r}")
        else:
            print("  ⚠️   [Object3DSolver] Keine DOM-Anweisung gefunden — Modell muss aus Bild raten.")

        # ── 3. Vision-Call ──────────────────────────────────────────
        image_bytes = await self.screenshot_fullpage()
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompt_3d.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
        except Exception as e:
            print(f"  ❌  [Object3DSolver] Konnte prompt_3d.txt nicht lesen: {e}")
            return False

        prompt = prompt.replace("{box_x}", str(box_x))
        prompt = prompt.replace("{box_y}", str(box_y))
        prompt = prompt.replace("{box_x_end}", str(box_x_end))
        prompt = prompt.replace("{box_y_end}", str(box_y_end))

        # Die DOM-gelesene Anweisung an den Prompt kleben — Modell weiss
        # jetzt explizit, welche Objekte/Reihenfolge gefragt sind.
        if instruction:
            prompt = (
                f"### Page Instruction (extracted from DOM, in original language)\n"
                f"{instruction}\n\n"
                f"### IMPORTANT\n"
                f"Output coordinates in the EXACT order the instruction asks. "
                f"If the instruction names objects sequentially, the coordinate "
                f"order MUST match.\n\n"
                + prompt
            )

        try:
            raw_response = await get_nvidia_vision_response(
                image_bytes=image_bytes,
                prompt=prompt,
                api_key=self.api_key,
                model=self.model,
                temperature=0.0,
                top_p=1.0,
            )
            print(f"  🤖  [Object3DSolver] Vision-Antwort: {raw_response[:300]!r}")
            coords = self._extract_coordinates(raw_response)
        except Exception as e:
            print(f"  ❌  [Object3DSolver] Vision-API-Fehler: {e}")
            return False

        if not coords:
            print("  ⚠️   [Object3DSolver] Keine (x,y)-Paare aus Antwort extrahierbar.")
            return False

        # ── 4. Boundary-Check ──────────────────────────────────────
        valid_coords: List[Tuple[int, int]] = []
        for x, y in coords:
            if box_x <= x <= box_x_end and box_y <= y <= box_y_end:
                valid_coords.append((x, y))
            else:
                print(f"  ⚠️   [Object3DSolver] ({x},{y}) außerhalb Box, ignoriert.")
        if not valid_coords:
            print("  ⚠️   [Object3DSolver] Keine validen Koords nach Boundary-Check.")
            return False
        print(f"  🎯  [Object3DSolver] {len(valid_coords)} Ziel(e): {valid_coords}")

        # ── 5. Humanized Clicks (Reihenfolge wie vom Modell ausgegeben) ──
        last_pos: Optional[Tuple[float, float]] = None
        for i, (tx, ty) in enumerate(valid_coords):
            await self.humanized_click(float(tx), float(ty), from_xy=last_pos)
            last_pos = (float(tx), float(ty))
            if i < len(valid_coords) - 1:
                # Menschliche Pause zwischen Klicks (lesen + zielen)
                await asyncio.sleep(random.uniform(0.5, 1.2))

        # ── 6. Submit-Button ───────────────────────────────────────
        submit_hit = await self.find_selector_in_frames(SUBMIT_SELECTORS)
        if submit_hit:
            sub_frame, sub_sel = submit_hit
            sub_loc = sub_frame.locator(sub_sel).first
            try:
                sub_box = await sub_loc.bounding_box()
                if sub_box:
                    sx = sub_box["x"] + sub_box["width"] / 2
                    sy = sub_box["y"] + sub_box["height"] / 2
                    print(f"  ✉️   [Object3DSolver] Submit via humanized click → ({sx:.0f},{sy:.0f})")
                    await self.humanized_click(sx, sy, from_xy=last_pos)
                else:
                    await sub_loc.click()
            except Exception as e:
                print(f"  ⚠️   [Object3DSolver] Submit-Click fehlgeschlagen: {e}")

        await asyncio.sleep(random.uniform(1.8, 2.8))

        # ── 7. Success-Check ───────────────────────────────────────
        success_hit = await self.find_selector_in_frames(SUCCESS_INDICATORS)
        if success_hit:
            print(f"  🎉  [Object3DSolver] CAPTCHA gelöst (Indikator: {success_hit[1]}).")
            return True

        box_still = await self.find_selector_in_frames(OBJECT_3D_SELECTORS)
        if not box_still:
            print("  🎉  [Object3DSolver] CAPTCHA vermutlich gelöst (Box weg).")
            return True

        print("  ❌  [Object3DSolver] Versuch fehlgeschlagen.")
        return False

    def _extract_coordinates(self, text: str) -> List[Tuple[int, int]]:
        """Extrahiert (x,y)-Paare aus dem Modell-Output.

        Robust gegen Variationen:
          x1: 100, y1: 200   →  (100, 200)
          x: 100, y: 200     →  (100, 200)
          (100, 200)         →  (100, 200)  ← Fallback
        """
        coords: List[Tuple[int, int]] = []
        # Primär: x\d*: NUM, y\d*: NUM
        for m in re.finditer(
            r"x\d*\s*[:=]\s*(\d+)\s*[,;]?\s*y\d*\s*[:=]\s*(\d+)", text, re.IGNORECASE
        ):
            coords.append((int(m.group(1)), int(m.group(2))))
        if coords:
            return coords
        # Fallback: (NUM, NUM)
        for m in re.finditer(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)", text):
            coords.append((int(m.group(1)), int(m.group(2))))
        return coords


async def solve(page: Page) -> bool:
    solver = Object3DSolver(page)
    return await solver.solve()
