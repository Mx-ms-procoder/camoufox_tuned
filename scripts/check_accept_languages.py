#!/usr/bin/env python3
"""Guard against drift between Firefox's accept-language table and our port.

pythonlib/camoufox/locale.py reproduces
locale_service_default_accept_languages()
(intl/locale/rust/locale_service_glue/src/lib.rs). That table is data, and
Mozilla edits it between releases — a rebase that changes one arm would
silently give every identity of that language an Accept-Language header no
Firefox emits, with nothing failing.

Re-parses the Rust source and diffs it against the port.

    python3 scripts/check_accept_languages.py [path/to/firefox-source]

Skips (exit 0) when no Firefox source tree is present, so it is safe to wire
into a job that runs before the tarball is unpacked.
"""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pythonlib'))

from camoufox.locale import (  # noqa: E402
    _FIREFOX_ACCEPT_LANGUAGES,
    _FIREFOX_NO_EN_FALLBACK,
    FIREFOX_SHIPPED_LOCALES,
)

RUST_REL = os.path.join(
    'intl', 'locale', 'rust', 'locale_service_glue', 'src', 'lib.rs'
)
SHIPPED_REL = os.path.join('browser', 'locales', 'shipped-locales')

# Arms the Rust match expresses as guards or blocks rather than plain
# "lang" => "value" pairs; locale.py implements each one explicitly.
GUARDED = frozenset(('en', 'zh', 'ca'))


def find_tree(argv):
    candidates = [a for a in argv[1:] if not a.startswith('-')]
    candidates += [
        os.environ.get('CAMOUFOX_FF_SOURCE', ''),
        os.path.join(os.path.dirname(__file__), '..', '..', 'firefox-source'),
    ]
    for path in candidates:
        if path and os.path.isfile(os.path.join(path, RUST_REL)):
            return path
    return None


def parse_rust(tree):
    src = open(os.path.join(tree, RUST_REL), encoding='utf-8').read()
    fn = src.split('pub extern "C" fn locale_service_default_accept_languages')[1]
    fn = fn.split('\n}\n')[0]

    table, no_en = {}, set()
    # "xx" => "a, b",            (an optional // comment may follow)
    for m in re.finditer(r'^\s*"([a-z-]+)" => "([^"]*)",\s*(?://.*)?$', fn, re.M):
        table[m.group(1)] = m.group(2)
    # "xx" => { add_en_us = false; "a, b" }
    for m in re.finditer(
        r'^\s*"([a-z-]+)" => \{\s*\n\s*add_en_us = false;\s*\n\s*"([^"]*)"\s*\n\s*\}',
        fn,
        re.M,
    ):
        table[m.group(1)] = m.group(2)
        no_en.add(m.group(1))
    if 'add_en_us = false;' in fn.split('"en" =>')[1].split('"et" =>')[0]:
        no_en.add('en')
    return table, no_en


def main():
    tree = find_tree(sys.argv)
    if not tree:
        print('No Firefox source tree found - skipping accept-language check.')
        return 0

    table, no_en = parse_rust(tree)
    problems = []

    for lang, value in sorted(table.items()):
        if lang in GUARDED:
            continue
        ours = _FIREFOX_ACCEPT_LANGUAGES.get(lang)
        if ours is None:
            problems.append(f"missing language {lang!r}: Firefox has {value!r}")
        elif ours != value:
            problems.append(f"{lang!r}: ours {ours!r} != Firefox {value!r}")

    for lang in sorted(set(_FIREFOX_ACCEPT_LANGUAGES) - set(table) - GUARDED):
        problems.append(f"stale language {lang!r} no longer in Firefox's table")

    if no_en != set(_FIREFOX_NO_EN_FALLBACK):
        problems.append(
            f"add_en_us=false set differs: ours {sorted(_FIREFOX_NO_EN_FALLBACK)} "
            f"!= Firefox {sorted(no_en)}"
        )

    shipped_path = os.path.join(tree, SHIPPED_REL)
    if os.path.isfile(shipped_path):
        shipped = {
            line.strip()
            for line in open(shipped_path, encoding='utf-8')
            if line.strip() and not line.startswith('#')
        }
        # ja-JP-mac only exists on macOS builds and is not a value the app
        # locale takes on the platforms we ship, so it is deliberately absent.
        shipped.discard('ja-JP-mac')
        if shipped != set(FIREFOX_SHIPPED_LOCALES):
            missing = sorted(shipped - set(FIREFOX_SHIPPED_LOCALES))
            extra = sorted(set(FIREFOX_SHIPPED_LOCALES) - shipped)
            problems.append(f"shipped-locales drift: missing {missing}, extra {extra}")

    if problems:
        print(f"accept-language table has drifted from {tree}:")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(
        f"accept-language table matches Firefox ({len(table)} arms, "
        f"{len(FIREFOX_SHIPPED_LOCALES)} shipped locales)."
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
