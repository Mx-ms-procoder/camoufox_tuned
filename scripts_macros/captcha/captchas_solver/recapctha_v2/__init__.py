"""reCAPTCHA v2 solver for Playwright (audio-challenge path)."""

import os
import shutil

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
        solver = AsyncSolver(page)
        token = await solver.solve_recaptcha(attempts=3)
        if token:
            print("  [ReCaptchaV2] reCAPTCHA geloest.")
            return True
        print("  [ReCaptchaV2] Konnte kein Token generieren.")
        return False
    except NotImplementedError as e:
        # Image-Challenge: bewusst nicht supported, klare Meldung
        print(
            f"  [ReCaptchaV2] Bild-Challenge wurde angeboten — Audio-Solver kann "
            f"das nicht lösen ({e}). Versuche einen anderen User-Agent / IP oder "
            f"einen externen Solver-Service (z.B. CapSolver)."
        )
        return False
    except Exception as e:
        print(f"  [ReCaptchaV2] Fehler beim Loesen: {e}")
        return False
