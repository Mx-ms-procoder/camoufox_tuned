# Disabled tests inventory

K-13 (`AUDIT_2026-05-18.md`) flagged nine `*.disabled` test files in this
directory with no tracking. They are kept on disk (not deleted) because
the upstream Playwright suite still ships them and re-enabling is the
correct long-term direction. Until then this file is the single place
that records *why* each was disabled and what would have to change to
flip it back on.

If you re-enable one of these, drop the corresponding row from this
table in the same commit so the inventory stays accurate.

| File | Reason known to be disabled | What to fix before re-enabling |
|------|------------------------------|---------------------------------|
| `test_browsercontext_client_certificates.py` | Camoufox does not currently expose Playwright's per-context client-certificate API surface; tests stub a feature that is not wired through Juggler. | Wire the `clientCertificates` browser-context option through `additions/juggler/protocol/PageHandler.js` and ship a config-side toggle. |
| `test_check.py` | Depends on `page.check()` / `page.uncheck()` semantics that diverge from Firefox-native behaviour after the `force-default-pointer` patch. | Adjust the patch (`patches/identity/force-default-pointer.patch`) to not break synthetic clicks on `<input type=checkbox>` or pin the test to the new behaviour. |
| `test_click.py` | Same root cause as `test_check.py`: pointer-event semantics under `force-default-pointer`. | Same fix; consider extracting a small "click oracle" helper test that this test depends on. |
| `test_dispatch_event.py` | Synthetic-event paths under Juggler's `dispatchEvent` differ from upstream Playwright; assertions on `event.isTrusted` fail. | Decide whether Camoufox should mimic upstream (`isTrusted=false` for dispatched events) and update either the patch or the test. |
| `test_element_handle.py` | Mix of bounding-box and screenshot diffs; screenshot baselines were never re-captured for the Camoufox-rendered chrome. | Re-capture baselines in `tests/golden-firefox/` against the current Firefox 150 binary. |
| `test_fill.py` | `page.fill()` on contenteditable elements behaves differently after `shadow-root-bypass.patch`; the test pre-dates that patch. | Either narrow the patch's scope or update the assertion to expect the new bypass semantics. |
| `test_focus.py` | Focus tracking across cross-origin iframes is affected by `disable-remote-subframes.patch`. | Refactor the patch to leave focus events untouched, or split focus tests into a remote-subframes variant. |
| `test_launcher.py` | Exercises legacy launcher entry points that the Python launcher (`camoufox.utils.launch_options`) supersedes. | Decide whether the legacy launcher is supported — if yes, port the test; if no, delete this file. |
| `test_popup.py` | New-window/popup gating depends on `cross-process-storage.patch`; popup window references come back null in headless mode. | Verify against a headful run; if it passes there, mark the headless path as `pytest.skip`. |

Last reviewed: 2026-05-18 (K-13).
