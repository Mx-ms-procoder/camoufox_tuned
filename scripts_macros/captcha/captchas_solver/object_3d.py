"""
captchas_solver/object_3d.py
════════════════════════════════════════════════════════════════════
Solver für 3D-Bilder/Icon-CAPTCHAs ("Identische Objekte finden").
Nutzt Gemma-4-31b-it zur Koordinatenschätzung.
"""

from __future__ import annotations
import asyncio
import os
import random
import re
from typing import Optional

from playwright.async_api import Page

# Relative imports with fallback for direct execution
try:
    from .base_solver import AsyncCaptchaSolver, get_nvidia_vision_response
except (ImportError, ValueError):
    import sys
    # Add current directory to path to support direct execution
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from base_solver import AsyncCaptchaSolver, get_nvidia_vision_response  # type: ignore

# ══════════════════════════════════════════════════════════════════
#  KONFIGURATION
# ══════════════════════════════════════════════════════════════════

OBJECT_3D_SELECTORS = [
    ".captcha_verify_img--wrapper",  # TikTok 3D
    ".geetest_table_box",            # GeeTest Icons
    ".captcha-box",                  # Generisch
    "[id*='captcha-box' i]",
    "img[src*='captcha']",
]

class Object3DSolver(AsyncCaptchaSolver):
    """
    Solver für "Finde identische Objekte" CAPTCHAs.
    Wendet Geometric-Anchoring mit Gemma 4 an.
    """
    def __init__(self, page: Page):
        super().__init__(page, model="google/gemma-4-31b-it")

    async def solve(self) -> bool:
        print("\n  🧩  [Object3DSolver] Starte 3D-Objekt Solver (Gemma-4-31b-it)…")

        # ── Schritt 1: Captcha-Canvas/Box finden ────────────────────────────
        box_sel = await self.find_selector(OBJECT_3D_SELECTORS)

        if not box_sel:
            print("  ❌  [Object3DSolver] Captcha-Box nicht gefunden.")
            return False

        box = self.page.locator(box_sel).first
        bbox = await box.bounding_box()

        if not bbox:
            print("  ❌  [Object3DSolver] BoundingBox konnte nicht ermittelt werden.")
            return False

        box_x = int(bbox["x"])
        box_y = int(bbox["y"])
        box_width = int(bbox["width"])
        box_height = int(bbox["height"])
        
        box_x_end = box_x + box_width
        box_y_end = box_y + box_height

        print(f"  📌  [Object3DSolver] Captcha Box: X:{box_x} Y:{box_y} bis X:{box_x_end} Y:{box_y_end}")

        # ── Schritt 2: Full-Page Screenshot & Prompt-Injection ──────────
        image_bytes = await self.screenshot_fullpage()
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompt_3d.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
        except Exception as e:
            print(f"  ❌  [Object3DSolver] Konnte prompt_3d.txt nicht lesen: {e}")
            return False

        # Dynamisches "Geometric Anchoring" injizieren
        prompt = prompt.replace("{box_x}", str(box_x))
        prompt = prompt.replace("{box_y}", str(box_y))
        prompt = prompt.replace("{box_x_end}", str(box_x_end))
        prompt = prompt.replace("{box_y_end}", str(box_y_end))

        try:
            # API-Call mit dem spezifischen Gemma-Modell, temp=0/top_p=1
            raw_response = await get_nvidia_vision_response(
                image_bytes=image_bytes,
                prompt=prompt,
                api_key=self.api_key,
                model="google/gemma-4-31b-it",
                temperature=0.0,
                top_p=1.0
            )
            print(f"  🤖  [Object3DSolver] Gemma-Antwort: '{raw_response}'")
            
            coords = self._extract_coordinates(raw_response)
        except Exception as e:
            print(f"  ❌  [Object3DSolver] KI-Fehler: {e}")
            return False

        if not coords:
            print("  ⚠️   [Object3DSolver] Konnte keine gültigen x,y Koordinaten extrahieren.")
            return False

        # Boundary Safety Check
        valid_coords = []
        for x, y in coords:
            if box_x <= x <= box_x_end and box_y <= y <= box_y_end:
                valid_coords.append((x, y))
            else:
                print(f"  ⚠️   [Object3DSolver] Koordinate ({x},{y}) außerhalb der Box! Wird ignoriert.")
        
        if not valid_coords:
            print("  ⚠️   [Object3DSolver] Keine validen Koordinaten innerhalb der Box gefunden.")
            return False

        print(f"  🎯  [Object3DSolver] Ziele validiert: {valid_coords}")

        # ── Schritt 3/4: Ausführen der Klicks mit BehavioralHelper ────────────
        print(f"  🖱️   [Object3DSolver] Führe Klicks aus…")
        
        for i, (tx, ty) in enumerate(valid_coords):
            await self._humanized_move_and_click(tx, ty)
            if i < len(valid_coords) - 1:
                await asyncio.sleep(random.uniform(0.4, 0.9)) # Kurze Menschliche Pause zw. Klicks
        
        await asyncio.sleep(1.0)
        
        # Submit Button (falls nötig, ansonsten geht es automatisch)
        submit_btn = self.page.locator(".geetest_commit, .captcha_submit_btn").first
        if await submit_btn.is_visible():
            await submit_btn.click()
            
        await asyncio.sleep(2)
        
        # ── Schritt 5: Erfolgskontrolle ───────────────────────────
        box_still_visible = await self.find_selector(OBJECT_3D_SELECTORS)
        if not box_still_visible:
            print("  🎉  [Object3DSolver] CAPTCHA offenbar gelöst!")
            return True
        else:
            print(f"  ❌  [Object3DSolver] Versuch fehlgeschlagen. Übergebe an Agenten...")
            return False

    def _extract_coordinates(self, text: str) -> list[tuple[int, int]]:
        """Extrahiert alle gefundenen x,y Paare aus dem Output Format."""
        # Sucht flexibel nach allen x,y Paaren
        matches = re.findall(r'x\d*:\s*(\d+),\s*y\d*:\s*(\d+)', text, re.IGNORECASE)
        coords = []
        for match in matches:
            coords.append((int(match[0]), int(match[1])))
        return coords

    async def _humanized_move_and_click(self, target_x: int, target_y: int):
        """Maus-Flow zu einem Punkt via Playwright (Camoufox injected)."""
        await self.page.mouse.move(
            target_x + random.uniform(-1, 1), 
            target_y + random.uniform(-1, 1),
            steps=random.randint(15, 30)
        )
        await asyncio.sleep(random.uniform(0.1, 0.2))
        await self.page.mouse.down()
        await asyncio.sleep(random.uniform(0.08, 0.2))
        await self.page.mouse.up()


async def solve(page: Page) -> bool:
    solver = Object3DSolver(page)
    return await solver.solve()
