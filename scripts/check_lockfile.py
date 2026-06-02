#!/usr/bin/env python3
"""Fail fast when requirements.lock has drifted from requirements.txt.

The CI installs with ``pip install --require-hashes -r requirements.lock``.
If someone edits ``requirements.txt`` (adds/removes/bumps a pin) but forgets
to regenerate the lock, that surfaces only as a cryptic ``HashMismatch`` or a
silently outdated dependency much later. This check turns it into an early,
actionable failure: for every top-level requirement it verifies the lock
pins a concrete version that satisfies the requirement's specifier.

It is intentionally lightweight (no ``pip-compile`` invocation, so no
cross-version formatting false positives): it only validates the *direct*
requirements against the locked versions. The hash-pinned install still
guarantees the full transitive closure is intact.

Exit code 0 = in sync, 1 = drift detected (with a report), 2 = usage error.
"""

import os
import re
import sys

from packaging.requirements import InvalidRequirement, Requirement
from packaging.utils import canonicalize_name

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ_TXT = os.path.join(REPO_ROOT, "requirements.txt")
REQ_LOCK = os.path.join(REPO_ROOT, "requirements.lock")

# A locked pin line looks like:  ``click==8.1.8 \``  (hashes follow on
# indented ``--hash=`` continuation lines, which we ignore). Extras may be
# preserved by pip-compile, e.g. ``httpx[http2]==0.27.2 \``, so an optional
# ``[...]`` group is allowed between the name and ``==``.
LOCK_PIN_RE = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]*\])?==(?P<ver>[0-9][^\s\\;]*)"
)


def parse_lock(path):
    """Return {canonical_name: version} for every top-level pin in the lock."""
    pins = {}
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("--"):
                continue
            m = LOCK_PIN_RE.match(line)
            if m:
                pins[canonicalize_name(m.group("name"))] = m.group("ver")
    return pins


def parse_requirements(path):
    """Yield Requirement objects for each direct requirement line."""
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            try:
                yield Requirement(line)
            except InvalidRequirement as exc:
                print(f"  [skip] unparseable requirement {line!r}: {exc}")


def main():
    for path in (REQ_TXT, REQ_LOCK):
        if not os.path.isfile(path):
            print(f"error: {path} not found", file=sys.stderr)
            return 2

    pins = parse_lock(REQ_LOCK)
    problems = []
    checked = 0

    for req in parse_requirements(REQ_TXT):
        # Skip requirements whose environment marker is false for the current
        # interpreter; the lock legitimately need not pin them here.
        if req.marker is not None and not req.marker.evaluate():
            continue
        name = canonicalize_name(req.name)
        checked += 1
        locked = pins.get(name)
        if locked is None:
            problems.append(
                f"{req.name}: present in requirements.txt but NOT pinned in requirements.lock"
            )
            continue
        if req.specifier and not req.specifier.contains(locked, prereleases=True):
            problems.append(
                f"{req.name}: lock pins {locked}, which does NOT satisfy "
                f"requirements.txt spec '{req.specifier}'"
            )

    if problems:
        print("requirements.lock is OUT OF SYNC with requirements.txt:\n")
        for p in problems:
            print(f"  - {p}")
        print(
            "\nRegenerate the lockfile and commit both files together:\n"
            "  python -m pip install pip-tools\n"
            "  pip-compile --allow-unsafe --generate-hashes "
            "--output-file=requirements.lock requirements.txt"
        )
        return 1

    print(f"requirements.lock is in sync with requirements.txt ({checked} direct deps checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
