"""Timezone-injection helper for the Playwright launch path.

The C++ MaskConfig timezone override is applied per-realm and — through the
juggler window-creation path — can intermittently lose the race and leak the
host timezone (real machine tz) while every other spoof holds. Passing the
spoofed timezone to the Playwright *context* (`timezone_id`) uses the juggler's
own context-timezone override, which applies reliably. This helper reads the
`timezone` value out of the already-generated launch options so sync_api /
async_api can forward it as `timezone_id`.

(The engine-side root cause is fixed by timezone-spoofing.patch's #657 cache
seeding; this is the belt to that suspenders and works without a rebuild.)
"""

import json
from typing import Any, Dict, Optional


def config_timezone(from_options: Optional[Dict[str, Any]]) -> Optional[str]:
    """Return the spoofed timezone from launch options, or None.

    Only the file-based config path (CAMOU_CONFIG_FILE) carries the parsed
    timezone; the legacy chunked-env path is not read here (timezone_id is a
    best-effort convenience, and a missing value simply falls back to the
    MaskConfig override).
    """
    if not from_options:
        return None
    env = from_options.get("env") or {}
    path = env.get("CAMOU_CONFIG_FILE")
    if not path:
        return None
    try:
        with open(path, encoding="utf-8") as f:
            tz = json.load(f).get("timezone")
        return tz or None
    except Exception:
        return None
