import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import orjson

from camoufox.pkgman import OS_ARCH_MATRIX

# Get database path relative to this file
DB_PATH = Path(__file__).parent / 'webgl_data.db'

# Renderers that mean "no GPU": software rasterisers and the Windows
# no-driver fallback. They occur in the wild — inside VMs, over RDP and in
# containers — which is exactly why the telemetry-derived table carries them,
# and exactly why they must not be handed to a random identity: reporting one
# tells a platform that this session is a virtual machine or a headless
# container, the population anti-bot systems score as high risk. An
# explicitly requested vendor/renderer pair is still honoured.
_SOFTWARE_RENDERER_MARKERS = (
    'swiftshader',
    'llvmpipe',
    'softpipe',
    'microsoft basic render',
    'mesa offscreen',
    'software rasterizer',
)


def _is_software_renderer(renderer: str) -> bool:
    lowered = (renderer or '').lower()
    return any(marker in lowered for marker in _SOFTWARE_RENDERER_MARKERS)


# Renderer substrings that only ever occur on one platform. ANGLE is Chrome's
# GL-over-Direct3D translator and Direct3D is a Windows API, so either token
# under a macOS or Linux user agent is a contradiction a page can check in one
# line -- and the data set does contain such rows: of six macOS entries, two
# are `ANGLE (NVIDIA, ... Direct3D11 ...)` carrying a mac weight of 0.004
# against a win weight of 0.22, i.e. almost certainly a misparsed user agent
# upstream. That was enough to give roughly one in fifteen macOS identities a
# Windows GPU string.
_WINDOWS_ONLY_RENDERER_MARKERS = ('angle (', 'direct3d', 'd3d11')


def _is_os_foreign_renderer(os: str, renderer: str) -> bool:
    """True if this renderer cannot occur on the given OS."""
    if os == 'win':
        return False
    lowered = (renderer or '').lower()
    return any(marker in lowered for marker in _WINDOWS_ONLY_RENDERER_MARKERS)


def sample_webgl(
    os: str,
    vendor: Optional[str] = None,
    renderer: Optional[str] = None,
    seed: Optional[int] = None,
) -> Dict[str, str]:
    """
    Sample a random WebGL vendor/renderer combination and its data based on OS probabilities.
    Optionally use a specific vendor/renderer pair.

    Args:
        os: Operating system ('win', 'mac', or 'lin')
        vendor: Optional specific vendor to use
        renderer: Optional specific renderer to use (requires vendor to be set)
        seed: Optional integer seed for deterministic sampling. When set, the
            same seed always picks the same vendor/renderer pair so that
            identity-stable fingerprints stay reproducible across runs.

    Returns:
        Dict containing WebGL data including vendor, renderer and additional parameters

    Raises:
        ValueError: If invalid OS provided or no data found for OS/vendor/renderer
    """
    # Check that the OS is valid (avoid SQL injection)
    if os not in OS_ARCH_MATRIX:
        raise ValueError(f'Invalid OS: {os}. Must be one of: win, mac, lin')

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if vendor and renderer:
        # Get specific vendor/renderer pair and verify it exists for this OS
        cursor.execute(
            f'SELECT vendor, renderer, data, {os} FROM webgl_fingerprints '  # nosec
            'WHERE vendor = ? AND renderer = ?',
            (vendor, renderer),
        )
        result = cursor.fetchone()

        if not result:
            raise ValueError(f'No WebGL data found for vendor "{vendor}" and renderer "{renderer}"')

        if result[3] <= 0:  # Check OS-specific probability
            # Get a list of possible (vendor, renderer) pairs for this OS
            cursor.execute(
                f'SELECT DISTINCT vendor, renderer FROM webgl_fingerprints WHERE {os} > 0'  # nosec
            )
            possible_pairs = cursor.fetchall()
            raise ValueError(
                f'Vendor "{vendor}" and renderer "{renderer}" combination not valid for {os.title()}.\n'
                f'Possible pairs: {", ".join(str(pair) for pair in possible_pairs)}'
            )

        conn.close()
        return orjson.loads(result[2])

    # Get all vendor/renderer pairs and their probabilities for this OS
    cursor.execute(
        f'SELECT vendor, renderer, data, {os} FROM webgl_fingerprints WHERE {os} > 0'  # nosec
    )
    results = cursor.fetchall()
    conn.close()

    if not results:
        raise ValueError(f'No WebGL data found for OS: {os}')

    # Drop no-GPU renderers from the random pool (see
    # _SOFTWARE_RENDERER_MARKERS). Keep the unfiltered pool if that would
    # leave nothing to sample, so a future data set can never make this raise.
    hardware = [row for row in results if not _is_software_renderer(row[1])]
    if hardware:
        results = hardware

    # Drop renderers that cannot exist on this OS (see
    # _is_os_foreign_renderer). Same guard: never filter the pool to empty.
    native = [row for row in results if not _is_os_foreign_renderer(os, row[1])]
    if native:
        results = native

    # Split into separate arrays
    _, _, data_strs, probs = map(list, zip(*results))

    # Convert probabilities to numpy array and normalize
    probs_array = np.array(probs, dtype=np.float64)
    probs_array = probs_array / probs_array.sum()

    # Sample based on probabilities. A dedicated Generator with a caller-
    # provided seed keeps the choice deterministic for a given identity
    # without leaking through the global numpy RNG state.
    rng = np.random.default_rng(seed) if seed is not None else np.random.default_rng()
    idx = rng.choice(len(probs_array), p=probs_array)

    # Parse the JSON data string
    return orjson.loads(data_strs[idx])


def get_possible_pairs() -> Dict[str, List[Tuple[str, str]]]:
    """
    Get all possible (vendor, renderer) pairs for all OS, where the probability is greater than 0.
    """
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all vendor/renderer pairs for each OS where probability > 0
    result: Dict[str, List[Tuple[str, str]]] = {}
    for os_type in OS_ARCH_MATRIX:
        cursor.execute(
            'SELECT DISTINCT vendor, renderer FROM webgl_fingerprints '
            f'WHERE {os_type} > 0 ORDER BY {os_type} DESC',  # nosec
        )
        result[os_type] = cursor.fetchall()

    conn.close()
    return result
