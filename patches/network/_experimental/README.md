# network/_experimental — patches not on the default apply path

This directory mirrors `bundle/_experimental/` (the parked uTLS sidecar):
diffs that are written against assumptions about a specific Mozilla
upstream layout, but that the static audit on 2026-05-18 could not
verify against an actual checked-out `mozilla-unified` at the
`upstream.sh` pin.

**They are NOT listed in `patches/manifests/network.yaml`. The default
`make build` will not touch them.** Apply manually only after diffing
the targeted file in the local Firefox source against the upstream
this patch was written against (Mozilla mc-150).

## Files

### `http2-fingerprint.patch`

K-21 (AUDIT_2026-05-18.md). Routes `Http2Session::SendHello()` through
`IdentityStateProvider::GetHttp2State()` so the initial SETTINGS frame
and initial connection-level WINDOW_UPDATE pick up the values that
`pythonlib/camoufox/tls_profiles.get_http2_config()` emits when the
operator sets `CAMOUFOX_HTTP2_FINGERPRINT_EXPERIMENTAL=1`.

The Python and `IdentityStateProvider.hpp` halves of this work are
already on the default path; the consumer side is parked here because
`netwerk/protocol/http/Http2Session.cpp` evolves between Firefox
versions in ways that blind patching cannot reliably track.

To apply once you have a local source tree:

```sh
cd mozilla-unified
patch -p1 --dry-run < ../camoufox_tuned/patches/network/_experimental/http2-fingerprint.patch
# If hunks fail, hand-port — the helper function and the call sites are
# the only things that need to land. See the patch header for a
# function-by-function description.
patch -p1 < ../camoufox_tuned/patches/network/_experimental/http2-fingerprint.patch
```

Then add the patch to `patches/manifests/network.yaml` under your own
fork's branch.
