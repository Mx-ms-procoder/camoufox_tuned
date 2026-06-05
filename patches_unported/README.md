# Unported patches (deferred from the Firefox 150 port)

These 6 fork-only patches were temporarily moved out of `patches/` (and removed
from `patches/manifests/`) during the Firefox 135 → 150 port so the rest of the
patch set (upstream camoufox's coherent 150.0.2 patches + the fork's working
patches) applies cleanly and `apply-check` goes green. They are **not applied**
by `scripts/patch.py`.

They have no upstream-camoufox counterpart, so they were authored against
Firefox 135 and need rebasing onto 150 before being moved back into `patches/`
and re-added to the relevant manifest.

| patch | status | notes |
|-------|--------|-------|
| `core/macos-backgroundtasks-disabled.patch` | rebase | 1 hunk, trivial context drift (`#if defined(MOZ_BACKGROUNDTASKS)` wrap in `nsAppRunner.cpp`) |
| `identity/webdriver-webidl-gate.patch` | rebase (priority) | adds `dom.webdriver.enabled` pref + Navigator.webidl gate; anti-detection-relevant |
| `librewolf/remove_addons.patch` | rebase | 7 hunks across `browser/extensions/moz.build` + `browser/locales/*`; context drift |
| `librewolf/sed-patches/allow-searchengines-non-esr.patch` | rebase | 1 hunk, `enterprise_only` bool flip in policies-schema.json |
| `librewolf/sed-patches/disable-pocket.patch` | **obsolete** | Pocket was removed from Firefox in 2025; nothing to patch on 150 |
| `librewolf/context-menu.patch` | **obsolete** | only removes Pocket context-menu items, gone on 150 |

To re-port one: extract the matching files from the Firefox 150 source, apply
the patches that precede it (basename order), apply this patch with the rejects
fixed against the new context, regenerate, then restore it to `patches/` and its
manifest.
