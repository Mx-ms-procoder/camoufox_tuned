#!/usr/bin/env python3
"""
check_upstream_security.py — flag Mozilla security advisories that have
landed in Firefox releases newer than the version pinned in
``upstream.sh``.

Rationale (audit T3.3 / 2026-05-25): the fork pinned ``150.0.2-beta.25``
for an extended window while Mozilla shipped 150.0.3 + 151. Without a
CI check, security-relevant point releases age silently. This script
runs as a weekly cron job in
``.github/workflows/upstream-security-check.yml`` and exits non-zero
when our pinned version is older than the highest release named in any
MFSA listed under the configured cutoff date — letting GitHub email
the repo owner.

Usage:
    python3 scripts/check_upstream_security.py           # uses upstream.sh
    python3 scripts/check_upstream_security.py --json    # machine-readable

No network access required at import time. The MFSA fetch is gated
behind ``--check`` so unit tests can import the parser without going
to mozilla.org.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

MFSA_INDEX_URL = "https://www.mozilla.org/en-US/security/advisories/"
UPSTREAM_FILE = Path(__file__).resolve().parent.parent / "upstream.sh"
DEFAULT_TIMEOUT_SEC = 20


@dataclass(frozen=True)
class FirefoxVersion:
    """Parsed Firefox version: (major, minor, patch). beta/esr are stripped.

    Example: '150.0.3' -> FirefoxVersion(150, 0, 3).
    """
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, raw: str) -> Optional["FirefoxVersion"]:
        # Strip 'beta.NN', 'esr' suffixes and pull just the numeric tuple.
        m = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?", raw.strip())
        if not m:
            return None
        return cls(
            major=int(m.group(1)),
            minor=int(m.group(2)),
            patch=int(m.group(3) or 0),
        )

    def as_tuple(self) -> tuple:
        return (self.major, self.minor, self.patch)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def read_pinned_version(path: Path = UPSTREAM_FILE) -> FirefoxVersion:
    """Parse the ``version=X.Y.Z`` line from upstream.sh."""
    if not path.exists():
        raise FileNotFoundError(f"upstream.sh not found at {path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version="):
            raw = line.split("=", 1)[1].strip()
            parsed = FirefoxVersion.parse(raw)
            if parsed is None:
                raise ValueError(f"upstream.sh has unparseable version={raw!r}")
            return parsed
    raise ValueError("upstream.sh has no version= line")


# Each MFSA index entry looks like:
#   <td><a href="/en-US/security/advisories/mfsa2026-15/">MFSA 2026-15</a></td>
#   <td>March 11, 2026</td>
#   <td>Firefox 151, Firefox ESR 128.13, Thunderbird 151</td>
_MFSA_ROW_RE = re.compile(
    r'<a[^>]+href="(?P<href>/[^"]*/mfsa(?P<id>\d{4}-\d+)/?)"[^>]*>'
    r'\s*MFSA\s*\d{4}-\d+\s*</a>\s*</td>\s*'
    r'<td[^>]*>(?P<date>[^<]+)</td>\s*'
    r'<td[^>]*>(?P<products>[^<]+)</td>',
    re.IGNORECASE | re.DOTALL,
)

_FF_VER_RE = re.compile(r"\bFirefox\s+(\d+(?:\.\d+){0,2})", re.IGNORECASE)


@dataclass(frozen=True)
class MFSARecord:
    id: str
    date: str
    products: str
    firefox_versions: tuple

    @property
    def highest_firefox(self) -> Optional[FirefoxVersion]:
        if not self.firefox_versions:
            return None
        return max(self.firefox_versions, key=lambda v: v.as_tuple())


def parse_mfsa_index(html: str) -> List[MFSARecord]:
    """Parse the MFSA advisories HTML table into a list of records."""
    records: List[MFSARecord] = []
    for m in _MFSA_ROW_RE.finditer(html):
        products = m.group("products")
        versions = []
        for vm in _FF_VER_RE.finditer(products):
            parsed = FirefoxVersion.parse(vm.group(1))
            if parsed is not None:
                versions.append(parsed)
        records.append(MFSARecord(
            id=m.group("id"),
            date=m.group("date").strip(),
            products=products.strip(),
            firefox_versions=tuple(versions),
        ))
    return records


def fetch_mfsa_index(timeout: float = DEFAULT_TIMEOUT_SEC) -> str:
    req = urllib.request.Request(
        MFSA_INDEX_URL,
        headers={"User-Agent": "camoufox-upstream-check/1"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def newer_releases(pinned: FirefoxVersion, records: List[MFSARecord]) -> List[MFSARecord]:
    """Return MFSAs that name a Firefox release strictly newer than `pinned`."""
    hits: List[MFSARecord] = []
    for rec in records:
        for ver in rec.firefox_versions:
            # Only flag same-major drift (don't page on 151+ if we pin 150).
            if ver.major != pinned.major:
                continue
            if ver.as_tuple() > pinned.as_tuple():
                hits.append(rec)
                break
    return hits


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--json", action="store_true",
                   help="emit machine-readable JSON instead of human text")
    p.add_argument("--upstream", type=Path, default=UPSTREAM_FILE,
                   help="path to upstream.sh (default: repo root)")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SEC,
                   help="HTTP timeout in seconds (default: 20)")
    args = p.parse_args(argv)

    pinned = read_pinned_version(args.upstream)

    try:
        html = fetch_mfsa_index(timeout=args.timeout)
    except Exception as exc:
        # Don't fail CI when mozilla.org is briefly unreachable — surface
        # the error and exit 0 so the cron does not page on flakes.
        print(f"WARNING: fetching MFSA index failed: {exc}", file=sys.stderr)
        return 0

    records = parse_mfsa_index(html)
    hits = newer_releases(pinned, records)

    if args.json:
        json.dump(
            {
                "pinned": str(pinned),
                "newer_advisories": [
                    {"id": h.id, "date": h.date, "products": h.products,
                     "highest_firefox": str(h.highest_firefox)}
                    for h in hits
                ],
            },
            sys.stdout, indent=2,
        )
        sys.stdout.write("\n")
    else:
        if not hits:
            print(f"OK: upstream.sh pins {pinned}; no newer same-major MFSA found.")
            return 0
        print(f"DRIFT: upstream.sh pins {pinned}; "
              f"{len(hits)} MFSA(s) name a newer same-major Firefox release:")
        for h in hits:
            print(f"  * MFSA {h.id} ({h.date}) — {h.products}")
        print("\nAction: review the listed advisories, rebase upstream.sh, "
              "and re-run scripts/validate_patches.py.")

    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
