#!/usr/bin/env python3

"""
Common functions used across the Camoufox build system.
Not meant to be called directly.
"""

import contextlib
import fnmatch
import optparse
import os
import re
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass

start_time = time.time()


@contextlib.contextmanager
def temp_cd(path):
    """Temporarily change to a different working directory"""
    _old_cwd = os.getcwd()
    abs_path = os.path.abspath(path)
    assert os.path.exists(abs_path), f'{abs_path} does not exist.'
    os.chdir(abs_path)

    try:
        yield
    finally:
        os.chdir(_old_cwd)


def get_options():
    """Get options"""
    parser = optparse.OptionParser()
    parser.add_option('--mozconfig-only', dest='mozconfig_only', default=False, action="store_true")
    parser.add_option('--validate-only', dest='validate_only', default=False, action="store_true")
    parser.add_option(
        '--feature',
        dest='features',
        action='append',
        default=[],
        help='Only include patches claimed by the named manifest feature',
    )
    parser.add_option(
        '-P', '--no-settings-pane', dest='settings_pane', default=True, action="store_false"
    )
    parser.add_option(
        '--bundle',
        dest='bundle',
        default=None,
        help='Apply only a single patch bundle (e.g. --bundle identity)',
    )
    parser.add_option(
        '--check-conflicts',
        dest='check_conflicts',
        default=False,
        action='store_true',
        help='Run conflict detection without applying patches',
    )
    parser.add_option(
        '--strict',
        dest='strict',
        default=False,
        action='store_true',
        help=(
            'With --check-conflicts: exit non-zero if any hard conflict is '
            'not in patches/manifests/expected_overlaps.yaml.'
        ),
    )
    return parser.parse_args()


def find_src_dir(root_dir='.', version=None, release=None):
    """Get the source directory"""
    if version and release:
        name = os.path.join(root_dir, f'camoufox-{version}-{release}')
        assert os.path.exists(name), f'{name} does not exist.'
        return name
    folders = os.listdir(root_dir)
    for folder in folders:
        if os.path.isdir(folder) and folder.startswith('camoufox-'):
            return os.path.join(root_dir, folder)
    raise FileNotFoundError('No camoufox-* folder found')


def get_moz_target(target, arch):
    """Get moz_target from target and arch.

    Returns the Mozilla configure triple (consumed by ``--target=`` in the
    generated mozconfig). This is intentionally *not* the same as the Rust
    target triple installed via ``rustup target add`` in CI:

        Mozilla configure       Rust target (rustup)
        --------------------    ----------------------
        i686-pc-linux-gnu       i686-unknown-linux-gnu
        x86_64-pc-mingw32       x86_64-pc-windows-gnu
        i686-pc-mingw32         i686-pc-windows-gnu
        *-apple-darwin          *-apple-darwin           (identical)

    Mach maps Mozilla->Rust internally; do NOT "align" these by switching
    the windows branch to ``-pc-windows-gnu``, because mozconfig parsing
    keys off the ``mingw32`` substring to apply MinGW-specific build logic.
    """
    if target == "linux":
        return "aarch64-unknown-linux-gnu" if arch == "arm64" else f"{arch}-pc-linux-gnu"
    if target == "windows":
        return f"{arch}-pc-mingw32"
    if target == "macos":
        return "aarch64-apple-darwin" if arch == "arm64" else f"{arch}-apple-darwin"
    raise ValueError(f"Unsupported target: {target}")


def list_files(root_dir, suffix):
    """List files in a directory"""
    for root, _, files in os.walk(root_dir):
        for file in fnmatch.filter(files, suffix):
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, root_dir)
            yield os.path.join(root_dir, relative_path).replace('\\', '/')


class PatchManifestError(ValueError):
    """Raised when the patch manifest graph is inconsistent or unsafe."""


HUNK_HEADER_RE = re.compile(r'^@@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? @@')
HUNK_HEADER_FULL_RE = re.compile(
    r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@'
)
ZERO_OLD_INDEX_RE = re.compile(r'^index 0+\.\.[0-9a-fA-F]+')


def _expected_hunk_count(value):
    return int(value) if value is not None else 1


def _validate_unified_diff_hunks(patch_path, contents):
    """Check that unified diff hunk headers match the lines in each hunk."""
    lines = contents.splitlines()
    index = 0
    while index < len(lines):
        header = HUNK_HEADER_RE.match(lines[index])
        if not header:
            index += 1
            continue

        hunk_line = index + 1
        old_expected = _expected_hunk_count(header.group(1))
        new_expected = _expected_hunk_count(header.group(2))
        old_count = 0
        new_count = 0
        index += 1

        while index < len(lines):
            line = lines[index]
            if old_count == old_expected and new_count == new_expected:
                if line.startswith('\\'):
                    index += 1
                    continue
                break
            if line.startswith('@@ ') or line.startswith('diff --git '):
                break
            if line.startswith('\\'):
                index += 1
                continue
            if not line:
                old_count += 1
                new_count += 1
            elif line[0] == ' ':
                old_count += 1
                new_count += 1
            elif line[0] == '-':
                old_count += 1
            elif line[0] == '+':
                new_count += 1
            elif old_count == old_expected and new_count == new_expected:
                break
            else:
                raise PatchManifestError(
                    f'Malformed patch hunk in {patch_path}:{hunk_line}; '
                    f'unexpected line at {index + 1}: {line}'
                )

            if old_count > old_expected or new_count > new_expected:
                raise PatchManifestError(
                    f'Malformed patch hunk in {patch_path}:{hunk_line}; '
                    f'header expects -{old_expected} +{new_expected} lines, '
                    f'but hunk exceeds that at line {index + 1}'
                )
            index += 1

        if old_count != old_expected or new_count != new_expected:
            raise PatchManifestError(
                f'Malformed patch hunk in {patch_path}:{hunk_line}; '
                f'header expects -{old_expected} +{new_expected} lines, '
                f'but hunk has -{old_count} +{new_count}'
            )


def _validate_git_diff_headers(patch_path, contents):
    """Reject git diff metadata that makes GNU patch treat edits as file creation."""
    lines = contents.splitlines()
    for index, line in enumerate(lines):
        if not ZERO_OLD_INDEX_RE.match(line):
            continue
        old_header = next(
            (candidate for candidate in lines[index + 1:] if candidate.startswith('--- ')),
            '',
        )
        if old_header and old_header != '--- /dev/null':
            raise PatchManifestError(
                f'Patch uses an all-zero old git index for an existing file: '
                f'{patch_path}:{index + 1}'
            )


def _strip_wrapping_quotes(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_manifest(manifest_path):
    manifest = {"name": None, "description": "", "patches": []}
    current_key = None
    with open(manifest_path, 'r', encoding='utf-8') as handle:
        for line_number, raw_line in enumerate(handle, 1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if stripped.startswith('name:'):
                manifest["name"] = stripped.split(':', 1)[1].strip()
                current_key = None
                continue
            if stripped.startswith('description:'):
                manifest["description"] = _strip_wrapping_quotes(
                    stripped.split(':', 1)[1].strip()
                )
                current_key = None
                continue
            if stripped == 'patches:':
                current_key = 'patches'
                continue
            if current_key == 'patches' and stripped.startswith('- '):
                manifest["patches"].append(stripped[2:].strip())
                continue
            raise PatchManifestError(
                f'Unsupported manifest syntax in {manifest_path}:{line_number}: {stripped}'
            )
    if not manifest["name"]:
        raise PatchManifestError(f'Manifest {manifest_path} does not define a name')
    return manifest


def load_patch_manifests(root_dir='../patches', manifests_dir=None):
    """Load all patch manifests and validate that every claimed patch exists."""
    manifests_root = manifests_dir or os.path.join(root_dir, 'manifests')
    if not os.path.isdir(manifests_root):
        raise PatchManifestError(f'Manifest directory not found: {manifests_root}')

    # expected_overlaps.yaml is an allowlist consumed by detect_conflicts,
    # not a patch manifest, and uses a different YAML schema.
    manifest_paths = sorted(
        (
            os.path.join(manifests_root, name).replace('\\', '/')
            for name in os.listdir(manifests_root)
            if name.endswith('.yaml') and name != 'expected_overlaps.yaml'
        ),
        key=os.path.basename,
    )
    if not manifest_paths:
        raise PatchManifestError(f'No patch manifests found in {manifests_root}')

    manifests = []
    seen_names = set()
    for manifest_path in manifest_paths:
        manifest = _parse_manifest(manifest_path)
        if manifest["name"] in seen_names:
            raise PatchManifestError(f'Duplicate manifest name: {manifest["name"]}')
        seen_names.add(manifest["name"])
        for patch_name in manifest["patches"]:
            patch_path = os.path.join(root_dir, patch_name).replace('\\', '/')
            if not os.path.exists(patch_path):
                raise PatchManifestError(
                    f'Manifest {manifest["name"]} references missing patch {patch_name}'
                )
        manifests.append(manifest)
    return manifests


def validate_patch_file(patch_path):
    """Reject placeholder or non-portable patch stubs before they reach the build."""
    with open(patch_path, 'r', encoding='utf-8') as handle:
        contents = handle.read()
    if '@@ -XX' in contents or '+XX' in contents:
        raise PatchManifestError(
            f'Patch contains placeholder hunk markers and cannot be applied safely: {patch_path}'
        )
    _validate_git_diff_headers(patch_path, contents)
    _validate_unified_diff_hunks(patch_path, contents)


def list_patches(root_dir='../patches', suffix='*.patch', features=None, validate=True):
    """List all patch files claimed by manifests, preserving manifest declaration order.

    The returned order is: manifests iterated alphabetically by filename
    (a stable cross-manifest order), and within each manifest the patches
    are returned in the exact sequence in which they are listed under the
    ``patches:`` key. The previous behaviour sorted the final list by
    basename, which discarded the manifest authors' intent — see §1.3 in
    REMEDIATION_PLAN.md.
    """
    manifest_list = load_patch_manifests(root_dir=root_dir)
    selected_features = set(features or [])
    selected_manifests = [
        manifest
        for manifest in manifest_list
        if not selected_features or manifest["name"] in selected_features
    ]
    if selected_features and len(selected_manifests) != len(selected_features):
        missing = sorted(selected_features - {manifest["name"] for manifest in selected_manifests})
        raise PatchManifestError(f'Unknown manifest feature(s): {", ".join(missing)}')

    claimed_paths = []
    for manifest in selected_manifests:
        for patch_name in manifest["patches"]:
            patch_path = os.path.join(root_dir, patch_name).replace('\\', '/')
            claimed_paths.append(patch_path)

    if len(set(claimed_paths)) != len(claimed_paths):
        duplicates = sorted(
            {
                path for path in claimed_paths
                if claimed_paths.count(path) > 1
            }
        )
        raise PatchManifestError(
            f'Duplicate patch claims detected: {", ".join(os.path.basename(path) for path in duplicates)}'
        )

    if not selected_features:
        all_patch_paths = sorted(list_files(root_dir, suffix), key=os.path.basename)
        claimed_normalized = {os.path.normpath(p) for p in claimed_paths}
        unclaimed_paths = [
            path for path in all_patch_paths
            if not is_bootstrap_patch(path) and os.path.normpath(path) not in claimed_normalized
        ]
        if unclaimed_paths:
            raise PatchManifestError(
                'Unclaimed patch files detected: '
                + ', '.join(os.path.basename(path) for path in unclaimed_paths)
            )

    if validate:
        for patch_path in claimed_paths:
            validate_patch_file(patch_path)

    return claimed_paths

def is_bootstrap_patch(name):
    return bool(re.match(r'\d+\-.*', os.path.basename(name)))


@dataclass
class ConflictReport:
    """Report of two manifests modifying the same Gecko source file."""
    file_path: str
    manifest_a: str
    manifest_b: str
    severity: str = "warning"  # "info", "warning", or "error"
    reason: str = ""

    def __str__(self):
        tail = f" — {self.reason}" if self.reason else ""
        return (
            f"[{self.severity.upper()}] {self.file_path} is modified by both "
            f"'{self.manifest_a}' and '{self.manifest_b}'{tail}"
        )


def _parse_expected_overlaps_fallback(handle):
    """
    Minimal parser for the fixed expected_overlaps.yaml schema.

    Used when PyYAML is not installed (e.g. local validation runs without
    a virtualenv). Only handles the exact shape documented in
    patches/manifests/expected_overlaps.yaml: a top-level ``expected:`` list
    whose items have ``file:``, ``manifests: [a, b]`` and ``reason:`` keys.
    """
    entries = []
    in_expected = False
    current = None
    for raw_line in handle:
        line = raw_line.split('#', 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith('expected:'):
            in_expected = True
            continue
        if not in_expected:
            continue
        if line.startswith('  - '):
            if current is not None:
                entries.append(current)
            current = {}
            line = '    ' + line[4:]
        if current is None:
            continue
        body = line.strip()
        if body.startswith('file:'):
            current['file'] = _strip_wrapping_quotes(body.split(':', 1)[1].strip())
        elif body.startswith('manifests:'):
            value = body.split(':', 1)[1].strip()
            if value.startswith('[') and value.endswith(']'):
                items = [
                    _strip_wrapping_quotes(part.strip())
                    for part in value[1:-1].split(',')
                    if part.strip()
                ]
                current['manifests'] = items
        elif body.startswith('reason:'):
            current['reason'] = _strip_wrapping_quotes(body.split(':', 1)[1].strip())
    if current is not None:
        entries.append(current)
    return {'expected': entries}


def _load_expected_overlaps(root_dir):
    """
    Load patches/manifests/expected_overlaps.yaml if present.

    Returns a dict mapping ``(file_path, frozenset({manifest_a, manifest_b}))``
    to the human-readable reason for the intentional overlap. A missing file
    yields an empty allowlist; a missing PyYAML falls back to a minimal parser
    so local runs without the dev dependency still see documented overlaps.
    """
    allowlist = {}
    overlaps_path = os.path.join(root_dir, 'manifests', 'expected_overlaps.yaml')
    if not os.path.exists(overlaps_path):
        return allowlist
    data = None
    try:
        import yaml  # local import keeps validate-only path independent
        try:
            with open(overlaps_path, 'r', encoding='utf-8') as handle:
                data = yaml.safe_load(handle) or {}
        except (OSError, yaml.YAMLError):
            return allowlist
    except ImportError:
        try:
            with open(overlaps_path, 'r', encoding='utf-8') as handle:
                data = _parse_expected_overlaps_fallback(handle)
        except OSError:
            return allowlist
    for entry in (data.get('expected') or []):
        file_path = entry.get('file')
        manifests = entry.get('manifests') or []
        if not file_path or len(manifests) != 2:
            continue
        key = (file_path, frozenset(manifests))
        allowlist[key] = entry.get('reason', '') or ''
    return allowlist


def _extract_gecko_files(patch_path):
    """Extract Gecko source file paths from a patch file's diff headers."""
    files = set()
    try:
        with open(patch_path, 'r', encoding='utf-8', errors='replace') as handle:
            for line in handle:
                line = line.strip()
                if line.startswith('--- a/'):
                    files.add(line[6:])
                elif line.startswith('+++ b/'):
                    files.add(line[6:])
    except (OSError, UnicodeDecodeError):
        pass
    # Remove /dev/null entries
    files.discard('/dev/null')
    return files


def _extract_hunks(patch_path):
    """Yield (file_path, old_start, old_count) for every hunk in patch_path.

    Operates on the source-file side of the unified diff (``--- a/...``):
    ``old_start`` is the first line number the hunk touches and
    ``old_count`` is the number of lines it spans. This is the side that
    determines whether two patches collide on the same source region —
    a zero ``old_count`` (pure insertion) is normalised to 1 for
    overlap-detection purposes, so we don't miss adjacent edits.
    """
    hunks = []
    current_file = None
    try:
        with open(patch_path, 'r', encoding='utf-8', errors='replace') as handle:
            for line in handle:
                if line.startswith('--- a/'):
                    current_file = line.rstrip('\r\n')[6:]
                    continue
                if line.startswith('--- '):
                    current_file = None
                    continue
                if line.startswith('@@') and current_file is not None:
                    match = HUNK_HEADER_FULL_RE.match(line)
                    if match:
                        old_start = int(match.group(1))
                        old_count = (
                            int(match.group(2)) if match.group(2) is not None else 1
                        )
                        hunks.append((current_file, old_start, old_count))
    except (OSError, UnicodeDecodeError):
        pass
    return hunks


def _hunks_overlap(a_start, a_count, b_start, b_count):
    """Return True iff two hunk line-ranges intersect.

    Each hunk is treated as the closed interval [start, start+count-1].
    Pure insertions (count == 0) are bumped to a single-line region so
    an insertion at the same point as another edit is still flagged.
    """
    a_end = a_start + max(a_count, 1) - 1
    b_end = b_start + max(b_count, 1) - 1
    return not (a_end < b_start or b_end < a_start)


def detect_conflicts(manifests, root_dir='../patches'):
    """
    Detect when two different manifests modify the same Gecko source file.

    Args:
        manifests: List of parsed manifest dicts from load_patch_manifests()
        root_dir: Root directory for patch files

    Returns:
        List of ConflictReport instances
    """
    allowlist = _load_expected_overlaps(root_dir)

    # Build a map: gecko_file -> [(manifest_name, patch_file), ...]
    file_map = {}
    for manifest in manifests:
        for patch_name in manifest["patches"]:
            patch_path = os.path.join(root_dir, patch_name).replace('\\', '/')
            if not os.path.exists(patch_path):
                continue
            gecko_files = _extract_gecko_files(patch_path)
            for gecko_file in gecko_files:
                if gecko_file not in file_map:
                    file_map[gecko_file] = []
                file_map[gecko_file].append((manifest["name"], patch_name))

    # Find conflicts: files modified by more than one manifest
    conflicts = []
    for gecko_file, sources in file_map.items():
        manifest_names = sorted(set(entry[0] for entry in sources))
        if len(manifest_names) > 1:
            # Generate pairwise conflict reports
            for i in range(len(manifest_names)):
                for j in range(i + 1, len(manifest_names)):
                    pair = frozenset({manifest_names[i], manifest_names[j]})
                    allow_key = (gecko_file, pair)
                    if gecko_file.endswith("moz.build"):
                        # moz.build changes are expected to be shared.
                        severity = "warning"
                        reason = "moz.build is conventionally co-edited"
                    elif allow_key in allowlist:
                        # Intentional ordered composition documented in
                        # patches/manifests/expected_overlaps.yaml.
                        severity = "info"
                        reason = allowlist[allow_key]
                    else:
                        severity = "error"
                        reason = ""
                    conflicts.append(ConflictReport(
                        file_path=gecko_file,
                        manifest_a=manifest_names[i],
                        manifest_b=manifest_names[j],
                        severity=severity,
                        reason=reason,
                    ))

    # Hunk-level overlap: even when file-level co-editing is allowlisted,
    # actually-overlapping hunk ranges on the same source file will make
    # `git apply` fail. We surface those as their own error-level reports
    # so reviewers see the concrete line ranges, not just the file.
    # See §1.12 in REMEDIATION_PLAN.md.
    hunk_cache = {}
    for gecko_file, sources in file_map.items():
        if len(sources) < 2:
            continue
        if gecko_file.endswith('moz.build'):
            # moz.build hunks co-occur by design; not a useful overlap signal.
            continue
        # Per-patch hunks for this file
        per_patch = {}
        for manifest_name, patch_name in sources:
            patch_path = os.path.join(root_dir, patch_name).replace('\\', '/')
            if patch_path not in hunk_cache:
                hunk_cache[patch_path] = _extract_hunks(patch_path)
            per_patch[(manifest_name, patch_name)] = [
                (start, count)
                for (file_, start, count) in hunk_cache[patch_path]
                if file_ == gecko_file
            ]
        keys = sorted(per_patch.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                ka, kb = keys[i], keys[j]
                # Same manifest editing same hunk-range twice is also bad
                # but already caught at apply time; we focus on cross-manifest.
                if ka[0] == kb[0]:
                    continue
                # If this file-pair is already allowlisted as an ordered composition,
                # don't generate a separate hunk-level error — the sequencing is
                # intentional and documented in expected_overlaps.yaml.
                if (gecko_file, frozenset({ka[0], kb[0]})) in allowlist:
                    continue
                for (a_start, a_count) in per_patch[ka]:
                    a_end = a_start + max(a_count, 1) - 1
                    for (b_start, b_count) in per_patch[kb]:
                        if not _hunks_overlap(a_start, a_count, b_start, b_count):
                            continue
                        b_end = b_start + max(b_count, 1) - 1
                        conflicts.append(ConflictReport(
                            file_path=gecko_file,
                            manifest_a=ka[0],
                            manifest_b=kb[0],
                            severity="error",
                            reason=(
                                f"hunk overlap: {os.path.basename(ka[1])} "
                                f"@ {a_start}-{a_end} vs "
                                f"{os.path.basename(kb[1])} @ {b_start}-{b_end}"
                            ),
                        ))

    severity_order = {"error": 0, "warning": 1, "info": 2}
    return sorted(conflicts, key=lambda c: (severity_order.get(c.severity, 9), c.file_path))


def print_conflict_report(conflicts):
    """Pretty-print conflict detection results."""
    if not conflicts:
        print("No patch conflicts detected.")
        return

    errors = [c for c in conflicts if c.severity == "error"]
    warnings = [c for c in conflicts if c.severity == "warning"]
    infos = [c for c in conflicts if c.severity == "info"]

    print(f"\n{'='*60}")
    print(
        f"Patch Conflict Report: {len(errors)} errors, "
        f"{len(warnings)} warnings, {len(infos)} expected overlaps"
    )
    print(f"{'='*60}\n")

    for conflict in conflicts:
        print(f"  {conflict}")

    if errors:
        print(f"\n  {len(errors)} hard conflict(s) detected!")
        print(f"  These manifests modify the same non-build Gecko source files.")
        print(
            f"  If the overlap is intentional, document it in "
            f"patches/manifests/expected_overlaps.yaml."
        )
    print()


def conflict_exit_code(conflicts, strict=False):
    """
    Decide the process exit code for --check-conflicts.

    In strict mode, any "error"-severity conflict that is not in the
    allowlist causes a non-zero exit. Warnings (moz.build) and info
    (documented overlaps) never fail CI.
    """
    if not strict:
        return 0
    errors = [c for c in conflicts if c.severity == "error"]
    return 1 if errors else 0


def script_exit(statuscode):
    """Exit the script"""
    if (time.time() - start_time) > 60:
        # print elapsed time
        elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
        print(f"\n\aElapsed time: {elapsed}")
        sys.stdout.flush()

    sys.exit(statuscode)


def run(cmd, exit_on_fail=True, do_print=True):
    """Run a command without invoking a shell.

    ``cmd`` may be a list/tuple (preferred) or a string. Strings are
    tokenised with :func:`shlex.split` so callers do not need to do it
    themselves, but the resulting argv list is then executed with
    ``shell=False``. Shell metacharacters (``>``, ``|``, ``&``, ``~``
    expansion, etc.) are therefore *not* honoured — express those in
    Python (e.g. ``stdout=open(...)``, ``os.path.expanduser``) before
    calling :func:`run`.
    """
    if not cmd:
        return 0
    if isinstance(cmd, str):
        argv = shlex.split(cmd, posix=(os.name != 'nt'))
    else:
        argv = list(cmd)
    if do_print:
        print(shlex.join(argv))
        sys.stdout.flush()
    completed = subprocess.run(argv, shell=False, check=False)
    retval = completed.returncode
    if retval != 0 and exit_on_fail:
        print(f"fatal error: command {argv!r} failed")
        sys.stdout.flush()
        script_exit(1)
    return retval


def patch(patchfile, reverse=False, silent=False):
    """Run a patch file via the GNU patch utility (no shell)."""
    args = ['patch', '-p1']
    if reverse:
        args.append('-R')
    args += ['-i', patchfile]
    if not silent:
        print(f"\n*** -> {shlex.join(args)}")
    sys.stdout.flush()
    stdout = subprocess.DEVNULL if silent else None
    completed = subprocess.run(args, shell=False, check=False, stdout=stdout)
    if completed.returncode != 0:
        print(f"fatal error: command {args!r} failed")
        sys.stdout.flush()
        script_exit(1)
    return completed.returncode


__all__ = [
    'get_moz_target',
    'load_patch_manifests',
    'list_patches',
    'patch',
    'run',
    'script_exit',
    'temp_cd',
    'get_options',
    'validate_patch_file',
    'detect_conflicts',
    'print_conflict_report',
    'ConflictReport',
]


if __name__ == '__main__':
    print('This is a module, not meant to be called directly.')
    sys.exit(1)
