"""
api_config — external-service credentials and the opt-in gate.

The CAPTCHA solvers in this package transmit screenshots to the NVIDIA NIM
Vision API. This is a data-egress surface, so the gate is closed by default.
Operators who intend to use external solvers must explicitly set
``CAMOU_CAPTCHA_ALLOW_EXTERNAL`` to a truthy value.

T2.2 (audit): gate fails fast at solver construction rather than silently
no-op'ing or hitting auth errors halfway through the solve loop.
"""

import os
from typing import Optional


# ── External service gate ────────────────────────────────────────────

_EXTERNAL_GATE_ENV = "CAMOU_CAPTCHA_ALLOW_EXTERNAL"
_TRUTHY = {"1", "true", "yes", "on"}


class ExternalServiceDisabledError(RuntimeError):
    """Raised when a CAPTCHA solver would transmit data to an external
    service but the operator has not opted in via
    CAMOU_CAPTCHA_ALLOW_EXTERNAL."""


def is_external_captcha_allowed() -> bool:
    return os.environ.get(_EXTERNAL_GATE_ENV, "").strip().lower() in _TRUTHY


def require_external_captcha_allowed(service_name: str) -> None:
    """Raise if external CAPTCHA services are not explicitly enabled."""
    if not is_external_captcha_allowed():
        raise ExternalServiceDisabledError(
            f"External CAPTCHA service {service_name!r} requires "
            f"{_EXTERNAL_GATE_ENV}=1. This solver would transmit page "
            f"screenshots outside the local process."
        )


# ── Credential lookup ────────────────────────────────────────────────

def _env_or_none(*names: str) -> Optional[str]:
    for n in names:
        val = os.environ.get(n)
        if val:
            return val
    return None


# NVIDIA NIM API keys. NVIDIA_API_KEY is the catch-all fallback for
# both model families if a model-specific key is not set.
NVIDIA_API_KEY_Qwen: Optional[str] = _env_or_none(
    "NVIDIA_API_KEY_Qwen", "NVIDIA_API_KEY"
)
NVIDIA_API_KEY_Gemma: Optional[str] = _env_or_none(
    "NVIDIA_API_KEY_Gemma", "NVIDIA_API_KEY"
)
