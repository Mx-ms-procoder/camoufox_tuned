#!/usr/bin/env bash
set -euo pipefail

# Dev convenience: fetch Mozilla's `mach bootstrap` helper and run it to set up
# build dependencies. This is NOT on the CI build path (CI uses `make fetch`,
# which downloads the checksum-verified release tarball) — it is copied into the
# source tree by scripts/copy-additions.sh for developers who want to bootstrap
# a tree by hand.
#
# H-3 (audit 2026-07-03): this previously did
#   wget https://hg.mozilla.org/mozilla-central/raw-file/default/.../bootstrap.py
#   python3 bootstrap.py
# i.e. it downloaded and executed whatever mozilla-central *tip* ("default")
# happened to serve at that moment, with no version pin and no integrity check —
# the exact pipe-to-shell supply-chain anti-pattern K-17 removed for rustup.
# We now:
#   1) pin the URL to an immutable release tag (release-tag raw-files do not
#      move) instead of the rolling `default` head, and
#   2) verify the download against a recorded SHA-256 before executing it,
#      aborting on mismatch.
# Bump BOOTSTRAP_TAG + BOOTSTRAP_SHA256 together whenever upstream.sh moves to a
# new Firefox version (the two must stay in lockstep with the build target).

BOOTSTRAP_TAG="FIREFOX_150_0_2_RELEASE"
BOOTSTRAP_SHA256="ff872951b4a535e17c8250c0cd7a1e3637acb65949976240fb3348661757993d"
BOOTSTRAP_URL="https://hg.mozilla.org/releases/mozilla-release/raw-file/${BOOTSTRAP_TAG}/python/mozboot/bin/bootstrap.py"

tmp="$(mktemp -t bootstrap.XXXXXX.py)"
trap 'rm -f "$tmp"' EXIT

wget -q --https-only -O "$tmp" "$BOOTSTRAP_URL"

actual_sha="$(sha256sum "$tmp" | awk '{print $1}')"
if [ "$actual_sha" != "$BOOTSTRAP_SHA256" ]; then
    echo "mozfetch: bootstrap.py SHA-256 mismatch for ${BOOTSTRAP_TAG}" >&2
    echo "  expected ${BOOTSTRAP_SHA256}" >&2
    echo "  actual   ${actual_sha}" >&2
    echo "  refusing to execute an unverified bootstrap script." >&2
    exit 1
fi

python3 "$tmp" --no-interactive --application-choice=browser
