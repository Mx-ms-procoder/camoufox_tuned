#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip3" install -U pip
"$VENV_DIR/bin/pip3" install -r "$REPO_ROOT/requirements.txt"
"$VENV_DIR/bin/pip3" install "$REPO_ROOT/pythonlib"

# Install Firefox as well; Playwright requires browser binaries that match
# the installed Playwright package version.
"$VENV_DIR/bin/playwright" install firefox
