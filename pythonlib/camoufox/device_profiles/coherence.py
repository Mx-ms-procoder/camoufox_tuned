"""
Cross-validation rules for DeviceProfile coherence.

These rules catch implausible fingerprint combinations that would
be flagged by advanced anti-bot systems doing cross-reference checks
(e.g., Apple GPU on Windows, HiDPI on a low-end GPU, etc.).
"""

import logging
from typing import Any, Callable, List, Tuple

# TYPE_CHECKING import to avoid circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import DeviceProfile

logger = logging.getLogger("camoufox.coherence")


def validate_coherence(profile: 'DeviceProfile') -> List[str]:
    """
    Run all coherence rules against a DeviceProfile.

    Returns:
        List of human-readable issue descriptions.
        Empty list means the profile is fully coherent.
    """
    issues = []
    for name, rule_fn in COHERENCE_RULES:
        try:
            if not rule_fn(profile):
                issues.append(name)
        except (AttributeError, TypeError, ValueError, ZeroDivisionError) as exc:
            # A broken rule should be visible (logged + reported) instead of
            # silently masking inconsistencies. We still keep going so one
            # bad rule does not abort the whole check.
            logger.warning(
                "Coherence rule %r raised %s: %s — treating profile as failing this rule",
                name,
                type(exc).__name__,
                exc,
            )
            issues.append(f"{name} [rule errored: {type(exc).__name__}]")
    return issues


# ── GPU ↔ OS coherence ────────────────────────────────────────────────

def _gpu_os_apple(p: 'DeviceProfile') -> bool:
    """Apple GPUs (M1/M2/M3, Apple GPU) should only appear on macOS."""
    vendor = (p.gpu_vendor + " " + p.gpu_renderer).lower()
    if "apple" in vendor and p.os_family != "mac":
        return False
    return True


def _gpu_os_directx(p: 'DeviceProfile') -> bool:
    """Direct3D / ANGLE (D3D11) references should only appear on Windows."""
    renderer = p.gpu_renderer.lower()
    if "d3d11" in renderer and p.os_family != "win":
        return False
    return True


def _gpu_os_mesa(p: 'DeviceProfile') -> bool:
    """Mesa drivers (llvmpipe, radeonsi, iris) are Linux-only."""
    renderer = p.gpu_renderer.lower()
    mesa_markers = ("mesa", "llvmpipe", "radeonsi", "iris", "gallium")
    if any(m in renderer for m in mesa_markers) and p.os_family != "lin":
        return False
    return True


# ── Screen ↔ OS coherence ────────────────────────────────────────────

def _dpr_os(p: 'DeviceProfile') -> bool:
    """Plausibility bounds on device pixel ratio per OS.

    R7 calibration: the previous rule rejected DPR < 1.5 on macOS, but a
    Mac mini / Mac Pro — or any MacBook driving a standard 1080p/1440p
    external display — legitimately reports DPR 1.0. That is a common real
    configuration, not a tell, yet it tripped IdentityCoherenceError and
    blocked the launch. It also capped Linux at 2.0, rejecting genuine 4K
    Linux laptops. Keep only the genuinely implausible extremes.
    """
    if p.device_pixel_ratio <= 0 or p.device_pixel_ratio > 4.0:
        return False  # No real display reports DPR <= 0 or > 4.
    if p.os_family == "lin" and p.device_pixel_ratio > 3.0:
        return False  # Linux HiDPI exists, but > 3.0 is unheard of.
    return True


def _color_depth_os(p: 'DeviceProfile') -> bool:
    """macOS uses 30-bit color (10bpc). Windows/Linux typically use 24-bit."""
    if p.os_family == "mac" and p.color_depth not in (24, 30):
        return False
    if p.os_family != "mac" and p.color_depth not in (24, 32):
        return False
    return True


def _screen_resolution_plausible(p: 'DeviceProfile') -> bool:
    """Screen dimensions must be reasonable (no 0x0 or 50000x50000)."""
    if p.screen_width < 320 or p.screen_width > 7680:
        return False
    if p.screen_height < 240 or p.screen_height > 4320:
        return False
    return True


def _screen_aspect_ratio(p: 'DeviceProfile') -> bool:
    """Aspect ratio plausibility.

    R7 calibration: the old [1.0, 3.6] band rejected portrait-oriented
    monitors (rotated displays, e.g. 1080x1920 → 0.5625) which are a real,
    common setup for developers and finance desks. Accept portrait down to
    9:16 while still rejecting degenerate ratios; keep the ultrawide
    ceiling just past 32:9 (3.55).
    """
    ratio = p.screen_width / max(p.screen_height, 1)
    if ratio < 0.5 or ratio > 3.7:
        return False
    return True


# ── Hardware ↔ plausibility ──────────────────────────────────────────

def _hardware_concurrency_valid(p: 'DeviceProfile') -> bool:
    """Core count must be realistic.

    R7 calibration: the old fixed whitelist {1,2,4,...,64} rejected real
    high-core CPUs (36/40/44/56/72/96/128 — Threadripper / Xeon / EPYC)
    and odd VM core counts (3/5). Accept any value in a plausible range —
    small counts as-is, larger counts must be even (no real CPU exposes an
    odd hardwareConcurrency above 8).
    """
    n = p.hardware_concurrency
    if not isinstance(n, int) or n < 1 or n > 256:
        return False
    if n <= 8:
        return True
    return n % 2 == 0


def _hardware_concurrency_os(p: 'DeviceProfile') -> bool:
    """macOS minimum is typically 4 cores (no single-core Macs exist)."""
    if p.os_family == "mac" and p.hardware_concurrency < 4:
        return False
    return True


# ── Audio ↔ OS coherence ─────────────────────────────────────────────

# R7: standard PCM sample rates. The old list (8000/16000/22050/44100/
# 48000/96000) rejected legitimate hardware — 32000 (broadcast), 88200
# (mastering), 176400/192000 (hi-res DACs), 11025 (legacy) — and tripped
# IdentityCoherenceError on real devices. Calibrated to the full set of
# rates Firefox/AudioContext can plausibly report. Mirrored in
# identity.validate_identity_blob.
STANDARD_AUDIO_SAMPLE_RATES = (
    8000, 11025, 16000, 22050, 32000, 44100, 48000,
    88200, 96000, 176400, 192000,
)


def _audio_sample_rate_valid(p: 'DeviceProfile') -> bool:
    """Sample rate must be a standard PCM value (R7-calibrated set)."""
    return p.audio_sample_rate in STANDARD_AUDIO_SAMPLE_RATES


def _audio_latency_os(p: 'DeviceProfile') -> bool:
    """Output latency plausibility per OS audio subsystem.

    R7 calibration: the old 0.05 s ceiling on Windows/macOS flagged
    legitimate setups — Bluetooth output, USB DACs and loaded systems
    routinely report 0.1–0.2 s on WASAPI/CoreAudio. Raise the ceiling to a
    value that still rejects the absurd without false-positiving on
    wireless audio.
    """
    if p.audio_output_latency < 0:
        return False
    if p.os_family in ("win", "mac") and p.audio_output_latency > 0.20:
        return False
    if p.audio_output_latency > 0.5:
        return False  # implausible on any OS
    return True


# ── Font ↔ OS coherence ──────────────────────────────────────────────

def _fonts_os_windows_markers(p: 'DeviceProfile') -> bool:
    """Windows-only fonts (Segoe UI, Calibri) must not appear on Mac/Linux."""
    win_only = {"Segoe UI", "Calibri", "Consolas", "Corbel"}
    if p.os_family != "win" and any(f in p.fonts for f in win_only):
        return False
    return True


def _fonts_os_mac_markers(p: 'DeviceProfile') -> bool:
    """macOS-only fonts must not appear on Windows/Linux."""
    mac_only = {"Helvetica Neue", "Lucida Grande", "Menlo", "Geneva", "Monaco"}
    if p.os_family != "mac" and any(f in p.fonts for f in mac_only):
        return False
    return True


def _fonts_os_linux_markers(p: 'DeviceProfile') -> bool:
    """Linux TOR fonts must not appear on Windows/macOS."""
    lin_only = {"Arimo", "Cousine", "Tinos"}
    if p.os_family != "lin" and any(f in p.fonts for f in lin_only):
        return False
    return True


def _fonts_not_empty(p: 'DeviceProfile') -> bool:
    """A profile must have at least some fonts."""
    return len(p.fonts) >= 5


# ── Platform string ↔ OS coherence ───────────────────────────────────

def _platform_os_match(p: 'DeviceProfile') -> bool:
    """navigator.platform must match the OS family."""
    expected = {
        "win": "Win32",
        "mac": "MacIntel",
        "lin": "Linux x86_64",
    }
    if p.platform and p.platform != expected.get(p.os_family, ""):
        return False
    return True


def _oscpu_os_match(p: 'DeviceProfile') -> bool:
    """navigator.oscpu must reference the correct OS."""
    if not p.oscpu:
        return True
    if p.os_family == "win" and "Windows" not in p.oscpu:
        return False
    if p.os_family == "mac" and "Mac" not in p.oscpu:
        return False
    if p.os_family == "lin" and "Linux" not in p.oscpu:
        return False
    return True


# ── Screen ↔ GPU coherence ───────────────────────────────────────────

def _4k_needs_decent_gpu(p: 'DeviceProfile') -> bool:
    """4K+ resolution is implausible with integrated/software GPUs."""
    if p.screen_width >= 3840:
        renderer_lower = p.gpu_renderer.lower()
        software_markers = ("llvmpipe", "swiftshader", "software", "swrast")
        if any(m in renderer_lower for m in software_markers):
            return False
    return True


# ── Comprehensive rule registry ──────────────────────────────────────

COHERENCE_RULES: List[Tuple[str, Callable[['DeviceProfile'], bool]]] = [
    # GPU ↔ OS
    ("Apple GPU on non-macOS", _gpu_os_apple),
    ("D3D11 renderer on non-Windows", _gpu_os_directx),
    ("Mesa driver on non-Linux", _gpu_os_mesa),

    # Screen ↔ OS
    ("Non-Retina DPR on macOS", _dpr_os),
    ("Invalid color depth for OS", _color_depth_os),
    ("Screen resolution out of range", _screen_resolution_plausible),
    ("Implausible aspect ratio", _screen_aspect_ratio),

    # Hardware
    ("Invalid hardware concurrency value", _hardware_concurrency_valid),
    ("Too few cores for macOS", _hardware_concurrency_os),

    # Audio ↔ OS
    ("Invalid audio sample rate", _audio_sample_rate_valid),
    ("Implausible audio latency for OS", _audio_latency_os),

    # Fonts ↔ OS
    ("Windows-only fonts on non-Windows", _fonts_os_windows_markers),
    ("macOS-only fonts on non-macOS", _fonts_os_mac_markers),
    ("Linux-only fonts on non-Linux", _fonts_os_linux_markers),
    ("Too few fonts in profile", _fonts_not_empty),

    # Platform strings ↔ OS
    ("Platform string does not match OS", _platform_os_match),
    ("oscpu does not match OS", _oscpu_os_match),

    # Screen ↔ GPU
    ("4K resolution with software GPU", _4k_needs_decent_gpu),
]
