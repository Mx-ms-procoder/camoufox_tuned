"""
captchas_solver/base_solver.py
════════════════════════════════════════════════════════════════════
Basis-Klasse für alle CAPTCHA-Solver.

  * Zentralisiert NVIDIA-NIM-Vision-API-Aufrufe (real existierende
    Modell-IDs — KEINE hallucinierten Namen mehr).
  * Bietet Multi-Frame-Selektor-Suche (find_selector_in_frames),
    damit Captchas in cross-origin iframes (reCAPTCHA, hCaptcha,
    Turnstile, TikTok) für die Solver erreichbar sind.
  * Bietet humanized_drag / humanized_click via human_mouse.py
    (separat vom Browser — funktioniert auch ohne das Camoufox-
    Patchset, z.B. unter vanilla Playwright-Firefox/Chromium).
"""

from __future__ import annotations
import asyncio
import base64
import json
import os
import random
import re
from typing import Optional, List, Tuple, Any

import httpx
from playwright.async_api import Page, Frame, Locator

# Relative imports with fallback for direct execution
try:
    from .human_mouse import humanized_drag, humanized_click, humanized_move
except (ImportError, ValueError):  # pragma: no cover
    import sys as _sys
    _sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from human_mouse import humanized_drag, humanized_click, humanized_move  # type: ignore

# ══════════════════════════════════════════════════════════════════
#  KONFIGURATION
# ══════════════════════════════════════════════════════════════════

try:
    from .api_config import NVIDIA_API_KEY_Qwen, NVIDIA_API_KEY_Gemma
except ImportError:  # pragma: no cover
    NVIDIA_API_KEY_Qwen = NVIDIA_API_KEY_Gemma = ""

if not NVIDIA_API_KEY_Qwen or "DEIN_" in NVIDIA_API_KEY_Qwen:
    NVIDIA_API_KEY_Qwen = os.environ.get(
        "NVIDIA_API_KEY_Qwen", os.environ.get("NVIDIA_API_KEY", "")
    )
if not NVIDIA_API_KEY_Gemma or "DEIN_" in NVIDIA_API_KEY_Gemma:
    NVIDIA_API_KEY_Gemma = os.environ.get(
        "NVIDIA_API_KEY_Gemma", os.environ.get("NVIDIA_API_KEY", "")
    )

NVIDIA_INVOKE_URL: str = "https://integrate.api.nvidia.com/v1/chat/completions"

# R2 — Screenshot egress guard.
# Every solved CAPTCHA ships a screenshot to the third-party NVIDIA NIM
# vision API. A *full-page* screenshot of a logged-in page leaks far more
# than the captcha (emails, account data, anything below the fold). To
# bound the privacy blast-radius and bandwidth we (1) default screenshots
# to the viewport instead of the full document, (2) prefer tight
# element/region crops, and (3) hard-cap the bytes that may leave on a
# single call. Override the cap via CAPTCHA_MAX_IMAGE_BYTES (bytes);
# set 0 to disable. Default 8 MiB — comfortably above a viewport PNG,
# below a long full-page capture.
def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)))
    except (TypeError, ValueError):
        return default

CAPTCHA_MAX_IMAGE_BYTES: int = _env_int("CAPTCHA_MAX_IMAGE_BYTES", 8 * 1024 * 1024)

# Real existing NVIDIA NIM model identifiers (verified against
# build.nvidia.com catalog). The previous defaults
# "qwen/qwen3.5-122b-a10b" and "google/gemma-4-31b-it" do NOT exist
# and caused every Vision-API call to return HTTP 404 / model_not_found.
QWEN_VISION_MODEL_DEFAULT: str = "qwen/qwen2.5-vl-72b-instruct"
GEMMA_VISION_MODEL_DEFAULT: str = "google/gemma-3-27b-it"
NVIDIA_MODEL: str = QWEN_VISION_MODEL_DEFAULT  # alias for backwards compat

# Allow override via env so operators can switch models without code edits.
# Validate shape early so a typo in the env var is surfaced at import time
# rather than as a confusing HTTP 404 on the first vision call. NIM model
# IDs always look like "<publisher>/<model-name>"; reject anything else
# with a warning and fall back to the verified default.
_ENV_MODEL_OVERRIDE = os.environ.get("NVIDIA_CAPTCHA_MODEL")
if _ENV_MODEL_OVERRIDE:
    if "/" in _ENV_MODEL_OVERRIDE and len(_ENV_MODEL_OVERRIDE) > 3:
        NVIDIA_MODEL = _ENV_MODEL_OVERRIDE
    else:
        print(
            f"  ⚠️   [BaseSolver] NVIDIA_CAPTCHA_MODEL={_ENV_MODEL_OVERRIDE!r} "
            f"does not match the expected NIM '<publisher>/<model>' shape. "
            f"Falling back to default {NVIDIA_MODEL!r}."
        )


class AsyncCaptchaSolver:
    """
    Abstrakte Basisklasse für CAPTCHA-Solver.

    Konkrete Subklassen müssen `solve(self) -> bool` implementieren.
    """

    def __init__(self, page: Page, model: Optional[str] = None):
        self.page = page
        self.model = model or NVIDIA_MODEL
        # Default: Qwen-Key, es sei denn das Modell ist eine Gemma-Variante
        if "gemma" in self.model.lower():
            self.api_key = NVIDIA_API_KEY_Gemma
        else:
            self.api_key = NVIDIA_API_KEY_Qwen

        if not self.api_key:
            print(
                f"  ⚠️   [BaseSolver] Warnung: API_KEY für Modell '{self.model}' "
                f"nicht gesetzt (env NVIDIA_API_KEY / NVIDIA_API_KEY_Qwen / "
                f"NVIDIA_API_KEY_Gemma)."
            )

    async def solve(self) -> bool:
        raise NotImplementedError("Subclasses must implement solve()")

    # ── Vision-API ──────────────────────────────────────────────────

    async def get_vision_response(
        self,
        image_bytes: bytes,
        prompt: str,
        temperature: float = 0.0,
        top_p: float = 1.0,
    ) -> str:
        """Sendet Bild + Prompt an NVIDIA NIM. Returnt Modell-Antwort."""
        return await get_nvidia_vision_response(
            image_bytes=image_bytes,
            prompt=prompt,
            api_key=self.api_key,
            model=self.model,
            temperature=temperature,
            top_p=top_p,
        )

    # ── Multi-Frame-Selektor-Suche ─────────────────────────────────
    #
    # Captchas leben sehr oft in cross-origin iframes. Der vorherige
    # `find_selector` suchte nur im Main-Frame und scheiterte regelmäßig
    # an reCAPTCHA / hCaptcha / Turnstile / TikTok-Iframes.

    async def find_selector_in_frames(
        self, selectors: List[str]
    ) -> Optional[Tuple[Frame, str]]:
        """Findet den ersten sichtbaren Selektor in irgendeinem Frame.

        Returns: (frame, selector) oder None.
        Cross-origin iframes werden über Playwright's `page.frames`
        API erreicht — funktioniert in Chrome via CDP und in Firefox/
        Camoufox via Juggler.
        """
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

    async def find_selector(self, selectors: List[str]) -> Optional[str]:
        """Backwards-compat: returnt nur den Selektor-String, Main-Frame.

        Neue Solver sollten `find_selector_in_frames` benutzen.
        """
        for sel in selectors:
            try:
                elem = self.page.locator(sel).first
                if await elem.is_visible(timeout=1500):
                    return sel
            except Exception:
                continue
        return None

    async def first_visible_locator(
        self, selectors: List[str]
    ) -> Optional[Locator]:
        """Multi-Frame-Lookup, returnt direkt den Locator des ersten Treffers."""
        hit = await self.find_selector_in_frames(selectors)
        if hit is None:
            return None
        frame, sel = hit
        return frame.locator(sel).first

    # ── Screenshot ──────────────────────────────────────────────────

    async def screenshot_fullpage(self, full_page: bool = False) -> bytes:
        """Viewport screenshot by default (R2: egress reduction).

        This previously captured the ENTIRE scrollable document
        (full_page=True) and shipped it to the third-party vision API —
        leaking everything below the fold on a logged-in page. The captcha
        being solved is always within the viewport, so default to
        viewport-only and require an explicit full_page=True opt-in for the
        rare case a solver genuinely needs the whole document.
        """
        return await self.page.screenshot(type="png", full_page=full_page)

    async def screenshot_locator(self, loc: Locator) -> Optional[bytes]:
        """Screenshot eines spezifischen Elements — der bevorzugte,
        egress-minimale Pfad. Sendet nur die Captcha-Box an das Vision-
        Modell statt des ganzen Viewports/der ganzen Seite."""
        try:
            return await loc.screenshot(type="png")
        except Exception:
            return None

    async def screenshot_region(self, loc: Locator, pad: int = 24) -> Optional[bytes]:
        """Screenshot of a captcha element plus a small padding margin.

        Some captchas need a little surrounding context (e.g. the prompt
        text above a tile grid) that a tight element screenshot crops out.
        This clips to the element bounding box + `pad` px — clamped to the
        viewport — instead of falling back to a full viewport/page capture,
        keeping egress to the vision API minimal (R2).
        """
        try:
            box = await loc.bounding_box()
        except Exception:
            box = None
        if not box:
            return None
        try:
            vp = self.page.viewport_size or {}
        except Exception:
            vp = {}
        x = max(0.0, box["x"] - pad)
        y = max(0.0, box["y"] - pad)
        w = box["width"] + 2 * pad
        h = box["height"] + 2 * pad
        if vp:
            w = min(w, max(1.0, vp.get("width", x + w) - x))
            h = min(h, max(1.0, vp.get("height", y + h) - y))
        try:
            return await self.page.screenshot(
                type="png",
                clip={"x": x, "y": y, "width": w, "height": h},
            )
        except Exception:
            return None

    # ── Antwort-Parsing ─────────────────────────────────────────────

    def extract_percentage(self, text: str) -> Optional[float]:
        match = re.search(r"(\d+(?:\.\d+)?)\s*%", text)
        if match:
            val = float(match.group(1))
            return max(0.0, min(100.0, val))
        match = re.search(r"(\d+(?:\.\d+)?)", text)
        if match:
            val = float(match.group(1))
            if 0 <= val <= 100:
                return val
        return None

    def extract_target_x(self, text: str) -> Optional[int]:
        """Extrahiert Target_X aus 'Target_X: 123'-Format. Fallback: letzte Zahl."""
        match = re.search(r"Target_X:\s*(\d+)", text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        matches = re.findall(r"\b\d+\b", text)
        if matches:
            return int(matches[-1])
        return None

    # ── Humanized Mouse (separat vom Browser) ───────────────────────
    #
    # Delegiert an human_mouse.py — ein pure-Python-Port des Camoufox
    # C++ `HumanizeMouseTrajectory`-Algorithmus (Bezier + Distortion +
    # easeOutQuad). Funktioniert auf jedem Playwright-Browser, ohne dass
    # das Camoufox-Patchset im Browser aktiv sein muss.

    async def humanized_drag(self, from_xy: Tuple[float, float],
                             to_xy: Tuple[float, float]) -> None:
        await humanized_drag(self.page, from_xy, to_xy)

    async def humanized_click(self, x: float, y: float,
                              from_xy: Optional[Tuple[float, float]] = None) -> None:
        await humanized_click(self.page, x, y, from_xy=from_xy)

    async def humanized_move(self, from_xy: Tuple[float, float],
                             to_xy: Tuple[float, float]) -> None:
        await humanized_move(self.page, from_xy, to_xy)


# ══════════════════════════════════════════════════════════════════
#  NVIDIA NIM Vision API
# ══════════════════════════════════════════════════════════════════

async def get_nvidia_vision_response(
    image_bytes: bytes,
    prompt: str,
    api_key: str,
    model: str = NVIDIA_MODEL,
    temperature: float = 0.0,
    top_p: float = 1.0,
) -> str:
    """Standalone Helper für NVIDIA-NIM-Vision-Anfragen (echtes async via httpx).

    Streamt via SSE und filtert `reasoning_content` raus (sonst würde
    der "Denk"-Anteil des Modells in die Koordinaten-Extraktion lecken).

    Warum httpx statt requests+run_in_executor:
      - Echter asyncio-kompatibel (kein Thread-Pool-Blocking)
      - Kein Thread-Pool-Erschöpfen bei vielen gleichzeitigen Solves
      - Bessere Timeout-Kontrolle (connect + read separat)
      - HTTP/2-fähig
    """
    from .api_config import require_external_captcha_allowed
    require_external_captcha_allowed("NVIDIA NIM Vision")

    if not api_key:
        raise EnvironmentError(
            "NVIDIA_API_KEY fehlt — setze NVIDIA_API_KEY, NVIDIA_API_KEY_Qwen "
            "oder NVIDIA_API_KEY_Gemma in der Umgebung."
        )

    # R2 egress guard: bound how much screenshot data leaves the machine on
    # a single call. An oversized payload almost always means a full-page
    # capture slipped through; the caller should send a locator/region crop.
    img_len = len(image_bytes)
    if CAPTCHA_MAX_IMAGE_BYTES and img_len > CAPTCHA_MAX_IMAGE_BYTES:
        raise ValueError(
            f"Refusing to send a {img_len} byte screenshot to {model}: exceeds "
            f"CAPTCHA_MAX_IMAGE_BYTES={CAPTCHA_MAX_IMAGE_BYTES}. Capture a "
            f"locator/region screenshot (screenshot_locator/screenshot_region) "
            f"instead of a full-page image, or raise the cap explicitly."
        )

    b64 = base64.b64encode(image_bytes).decode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "max_tokens": 16384,
        "temperature": temperature,
        "top_p": top_p,
        "stream": True,
        "chat_template_kwargs": {"enable_thinking": True},
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64}"},
                    },
                ],
            }
        ],
    }

    full_text = ""
    timeout = httpx.Timeout(connect=10.0, read=60.0, write=30.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout, http2=True) as client:
        async with client.stream("POST", NVIDIA_INVOKE_URL, headers=headers, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line:
                    continue
                data = line
                if data.startswith("data:"):
                    data = data[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    # IMPORTANT: only consume delta.content. Some NIM
                    # reasoning models emit a separate delta.reasoning_content
                    # field with chain-of-thought text. Concatenating that
                    # into full_text would let the model's reasoning leak
                    # into the downstream regex parsers (extract_target_x,
                    # extract_percentage) which would then mis-parse a
                    # random number from the reasoning as the CAPTCHA
                    # coordinate. Explicitly ignore reasoning_content here.
                    content = delta.get("content", "")
                    if content:
                        full_text += content
                except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                    continue

    # Strip any <think>...</think> blocks the model may still inline in
    # content (some models do this even when reasoning_content is also
    # available). DOTALL so multi-line reasoning blocks are caught.
    full_text = re.sub(r"<think>.*?</think>", "", full_text, flags=re.DOTALL)
    # Also strip any unclosed <think>… tail in case the stream cut off
    # mid-reasoning before the closing tag arrived.
    full_text = re.sub(r"<think>.*\Z", "", full_text, flags=re.DOTALL)
    return full_text.strip()
