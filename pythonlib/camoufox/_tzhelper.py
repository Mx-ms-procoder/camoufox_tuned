"""Context-option helpers for the Playwright launch path.

Some identity values only take effect if they are forwarded as Playwright
*context* options rather than left to the C++ MaskConfig layer:

- timezone: the MaskConfig override is applied per-realm and — through the
  juggler window-creation path — can intermittently lose the race and leak the
  host timezone while every other spoof holds. `timezone_id` uses the juggler's
  own context-timezone override, which applies reliably. (The engine-side root
  cause is fixed by timezone-spoofing.patch's #657 cache seeding; this is the
  belt to that suspenders and works without a rebuild.)
- prefers-color-scheme: nothing else moves it at all, see config_color_scheme.

Both are read out of the already-generated launch options so sync_api /
async_api can pass them straight through.
"""

import json
from typing import Any, Dict, Optional

# Share of identities reporting prefers-color-scheme: dark, as a 0-255 cutoff
# on one byte: 90 ~= 35%. Field estimates for dark-mode adoption vary widely
# (~30-50% depending on platform and survey), so this is a calibration knob,
# not a measurement -- move it if better numbers turn up for the population
# being blended into.
_DARK_SCHEME_CUTOFF = 90


def _config_value(from_options: Optional[Dict[str, Any]], key: str) -> Any:
    """Read one key out of the generated launch config, or None.

    Only the file-based config path (CAMOU_CONFIG_FILE) carries the parsed
    values; the legacy chunked-env path is not read here (these forwards are
    best-effort conveniences, and a missing value simply falls back to
    whatever the browser would do on its own).
    """
    if not from_options:
        return None
    env = from_options.get("env") or {}
    path = env.get("CAMOU_CONFIG_FILE")
    if not path:
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f).get(key)
    except Exception:
        return None


def config_timezone(from_options: Optional[Dict[str, Any]]) -> Optional[str]:
    """Return the spoofed timezone from launch options, or None."""
    tz = _config_value(from_options, "timezone")
    return tz if isinstance(tz, str) and tz else None


def config_color_scheme(from_options: Optional[Dict[str, Any]]) -> Optional[str]:
    """Return the identity's prefers-color-scheme ('dark'/'light'), or None.

    The juggler override used to force 'dark' on every profile; aligning it
    to upstream's `colorScheme || browserContext.colorScheme || 'none'`
    removed that tell but replaced it with its mirror image, because 'none'
    follows a default that never varies. Measured 17/17 light across headless
    and headful launches, and ui.systemUsesDarkTheme (set to 1 in
    camoufox.cfg) turned out to move content not at all, so nothing else was
    varying it either. A population where every member reports the same
    scheme is a marker whichever value it is.

    Derived from canvas:noiseSeed rather than a key of its own: every config
    key is validated against the properties.json shipped inside the browser
    package, so a new one would raise UnknownProperty on every launch until
    the next rebuild. canvas:noiseSeed comes from the same identity digest,
    so it is exactly as stable per seed and just as independent.
    """
    seed = _config_value(from_options, "canvas:noiseSeed")
    if not isinstance(seed, int):
        return None
    return "dark" if (seed & 0xFF) < _DARK_SCHEME_CUTOFF else "light"
