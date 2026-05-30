"""reCAPTCHA v2 solver for Playwright (audio-challenge path)."""

import os
import shutil

from ..errors import RecaptchaSolveError
from ..api_config import require_external_captcha_allowed, ExternalServiceDisabledError

_async_import_error = None
_sync_import_error = None

try:
    from .async_solver import AsyncSolver
except Exception as e:
    AsyncSolver = None
    _async_import_error = e

try:
    from .sync_solver import SyncSolver
except Exception as e:
    SyncSolver = None
    _sync_import_error = e

__all__ = ["AsyncSolver", "SyncSolver", "solve"]


def _ffmpeg_available() -> bool:
    """pydub braucht ffmpeg auf System-Ebene (nicht in pip-Deps).

    Wir suchen entweder im PATH oder via FFMPEG_BINARY-Env.
    """
    if os.environ.get("FFMPEG_BINARY"):
        return os.path.isfile(os.environ["FFMPEG_BINARY"])
    return shutil.which("ffmpeg") is not None or shutil.which("ffmpeg.exe") is not None


async def solve(page) -> bool:
    """Top-Level Solver-Entry, vom scanner.py via _SOLVER_ROUTES aufgerufen.

    Diagnose-flow:
      1. Python-Dependencies vorhanden? (pydub, speech_recognition, tenacity)
      2. ffmpeg auf System-Ebene vorhanden? (pydub-Voraussetzung)
      3. Echter Solve via AsyncSolver.solve_recaptcha(attempts=3)
    """
    print("\n  [ReCaptchaV2] Starte reCAPTCHA v2 Audio-Solver...")

    if AsyncSolver is None:
        detail = _async_import_error or _sync_import_error
        print(
            f"  [ReCaptchaV2] Solver nicht verfuegbar — Python-Dependency fehlt: {detail}"
        )
        print(
            "  [ReCaptchaV2] Erforderliche pip-Pakete: pydub, SpeechRecognition, tenacity"
        )
        return False

    if not _ffmpeg_available():
        print(
            "  [ReCaptchaV2] ffmpeg auf System-Ebene nicht gefunden — pydub kann "
            "die MP3-Audio-Challenge nicht in WAV konvertieren. Installiere ffmpeg "
            "(Windows: winget install ffmpeg; Linux: apt install ffmpeg; "
            "macOS: brew install ffmpeg) oder setze FFMPEG_BINARY auf den ffmpeg-Pfad."
        )
        return False

    try:
        require_external_captcha_allowed("Google Web Speech API (reCAPTCHA audio)")
    except ExternalServiceDisabledError as e:
        print(f"  [ReCaptchaV2] Externer Aufruf blockiert: {e}")
        return False

    try:
        # `async with` guarantees solver.close() runs, which removes the
        # page.on("response", …) listener registered in BaseSolver.__init__.
        # Without it every solve attempt (and every retry) leaked a response
        # listener onto the page — they accumulated across a live_scan
        # session and each fired a coroutine on every subsequent HTTP
        # response.
        async with AsyncSolver(page) as solver:
            token = await solver.solve_recaptcha(attempts=3)
        if token:
            print("  [ReCaptchaV2] reCAPTCHA geloest.")
            return True
        print("  [ReCaptchaV2] Konnte kein Token generieren.")
        return False
    except RecaptchaSolveError as e:
        if "image challenge" in str(e).lower():
            print(
                f"  [ReCaptchaV2] Bild-Challenge wurde angeboten — Audio-Solver "
                f"kann das nicht lösen. IP/Proxy wechseln und erneut versuchen."
            )
        else:
            print(f"  [ReCaptchaV2] Konnte reCAPTCHA nicht lösen: {e}")
        return False
    except Exception as e:
        print(f"  [ReCaptchaV2] Fehler beim Loesen: {e}")
        return False
