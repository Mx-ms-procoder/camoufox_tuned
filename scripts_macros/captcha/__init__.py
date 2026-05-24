"""CAPTCHA Solver module for autonomous CAPTCHA resolution.

K-19 (AUDIT_2026-05-18.md): this module is **experimental** and is not
loaded by the default Camoufox launcher. It is shipped here for
operators who want to wire it into their own pipelines, but the audit
flagged it as a half-functional subsystem:

  * `scanner.py` carries a mix of German and English doc comments and
    has not been exercised against the current upstream selector set.
  * `captchas_solver/recapctha_v2/` is vendored third-party code (see
    its NOTICE.md) and was never integrated with the Juggler bridge.
  * The provider providers in `scanner.py` rely on selectors that
    target sites change frequently and that this fork does not own.

To use the captcha subsystem you must opt-in explicitly by setting
``CAMOUFOX_ENABLE_CAPTCHA=1`` in your environment before importing any
submodule. Importing without the opt-in raises an ImportError so that
no downstream code accidentally depends on the experimental surface.
"""

import os as _os

if _os.environ.get("CAMOUFOX_ENABLE_CAPTCHA") != "1":
    raise ImportError(
        "scripts_macros.captcha is experimental and disabled by default. "
        "Set CAMOUFOX_ENABLE_CAPTCHA=1 in the environment to opt in. "
        "See K-19 in AUDIT_2026-05-18.md for the current status."
    )
