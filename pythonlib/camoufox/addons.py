import hashlib
import logging
import os
import shutil
from dataclasses import dataclass
from enum import Enum
from threading import Lock
from typing import List, Optional

import requests

from .exceptions import InvalidAddonPath
from .pkgman import get_path, unzip, webdl

logger = logging.getLogger("camoufox.addons")


@dataclass(frozen=True)
class AddonSource:
    """A pinned download source for a bundled add-on.

    ``sha256`` is optional only because uBO's "latest" rolling URL has no
    stable hash; when set, the downloaded bytes are verified before
    extraction and a mismatch aborts the install.
    """

    url: str
    sha256: Optional[str] = None


# uBlock Origin source.
#
# By default we fall back to the AMO "latest" endpoint to keep parity with
# upstream Camoufox, but the audit (S-003) flagged that this is unpinned
# and reproducibility-unsafe. Operators are expected to pin via env vars:
#   CAMOUFOX_UBO_URL    — direct AMO file URL for a specific version
#   CAMOUFOX_UBO_SHA256 — hex sha256 of the XPI bytes
_DEFAULT_UBO_URL = "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"

_ADDON_SOURCES = {
    "UBO": AddonSource(
        url=os.environ.get("CAMOUFOX_UBO_URL", _DEFAULT_UBO_URL),
        sha256=os.environ.get("CAMOUFOX_UBO_SHA256") or None,
    ),
}


class DefaultAddons(Enum):
    """
    Default addons to be downloaded
    """

    UBO = "UBO"

    @property
    def source(self) -> AddonSource:
        return _ADDON_SOURCES[self.value]


ADDON_LOCK = Lock()


def _is_extracted_addon(path: str) -> bool:
    return os.path.isdir(path) and os.path.exists(os.path.join(path, 'manifest.json'))


def confirm_paths(paths: List[str]) -> None:
    """
    Confirms that the addon paths are valid
    """
    for path in paths:
        if not os.path.isdir(path):
            raise InvalidAddonPath(path)
        if not os.path.exists(os.path.join(path, 'manifest.json')):
            raise InvalidAddonPath(
                'manifest.json is missing. Addon path must be a path to an extracted addon.'
            )


def add_default_addons(
    addons_list: List[str], exclude_list: Optional[List[DefaultAddons]] = None
) -> None:
    """
    Adds default addons, minus any specified in exclude_list, to addons_list
    """
    # Build a dictionary from DefaultAddons, excluding keys found in exclude_list
    if exclude_list is None:
        exclude_list = []

    addons = [addon for addon in DefaultAddons if addon not in exclude_list]

    with ADDON_LOCK:
        maybe_download_addons(addons, addons_list)


def download_and_extract(source: "AddonSource", extract_path: str, name: str) -> None:
    """
    Downloads and extracts an addon from a pinned source to a specified path.

    When ``source.sha256`` is set, the downloaded XPI is hashed and compared
    before extraction; a mismatch raises ``InvalidAddonPath``. When unset
    (e.g. the AMO "latest" fallback URL) a warning is logged so unpinned
    installs remain visible in CI/build logs.
    """
    buffer = webdl(source.url, desc=f"Downloading addon ({name})", bar=False)

    if source.sha256:
        buffer.seek(0)
        digest = hashlib.sha256(buffer.read()).hexdigest()
        if digest.lower() != source.sha256.lower():
            raise InvalidAddonPath(
                f"Addon {name} hash mismatch: expected {source.sha256}, got {digest}"
            )
        buffer.seek(0)
    else:
        logger.warning(
            "Addon %s downloaded without a sha256 pin (url=%s). "
            "Set CAMOUFOX_%s_URL and CAMOUFOX_%s_SHA256 for reproducible builds.",
            name,
            source.url,
            name,
            name,
        )

    unzip(buffer, extract_path, f"Extracting addon ({name})", bar=False)


def get_addon_path(addon_name: str) -> str:
    """
    Returns a path to the addon
    """
    return get_path(os.path.join("addons", addon_name))


def maybe_download_addons(
    addons: List[DefaultAddons], addons_list: Optional[List[str]] = None
) -> None:
    """
    Downloads and extracts addons from a given dictionary to a specified list
    Skips downloading if the addon is already downloaded
    """
    for addon in addons:
        # Get the addon path
        addon_path = get_addon_path(addon.name)

        # Check if the addon is already extracted
        if _is_extracted_addon(addon_path):
            # Add the existing addon path to addons_list
            if addons_list is not None:
                addons_list.append(addon_path)
            continue

        # Addon doesn't exist, create directory and download
        try:
            os.makedirs(addon_path, exist_ok=True)
            download_and_extract(addon.source, addon_path, addon.name)
            if not _is_extracted_addon(addon_path):
                raise InvalidAddonPath(
                    'manifest.json is missing. Addon path must be a path to an extracted addon.'
                )
            # Add the new addon directory path to addons_list
            if addons_list is not None:
                addons_list.append(addon_path)
        except (OSError, InvalidAddonPath, requests.RequestException) as e:
            if os.path.isdir(addon_path) and not _is_extracted_addon(addon_path):
                shutil.rmtree(addon_path, ignore_errors=True)
            logger.error("Failed to download and extract %s: %s", addon.name, e)
