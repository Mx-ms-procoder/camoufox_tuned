#!/usr/bin/env python3

from _mixin import list_bootstrap_patches, list_patches


if __name__ == "__main__":
    # Validate the manifest-claimed feature patches AND the numeric-prefixed
    # bootstrap patches (playwright/juggler). The latter are not claimed by any
    # manifest, so they used to escape validation entirely — which is how a
    # malformed hunk header in 0-playwright.patch / 1-leak-fixes.patch could sit
    # undetected. Validating both here means the test-python CI job fails fast
    # on a broken bootstrap patch instead of only surfacing it in the matrix.
    feature_files = list_patches(root_dir='./patches')
    bootstrap_files = list_bootstrap_patches(root_dir='./patches')
    print(
        f"Validated {len(bootstrap_files)} bootstrap "
        f"+ {len(feature_files)} feature patch file(s)."
    )
