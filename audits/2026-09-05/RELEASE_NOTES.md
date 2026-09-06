Camoufox 155.0.1-beta.31 brings the fork onto Gecko 155.0.1, restores Fission
and RLBox build protection, and updates the Python and Go dependencies.

Changes include consistent AudioBuffer offset reads, WebGL byte-readback
handling for PBOs and packing layouts, CSS/screen coherence, main-world init
script lifecycle fixes, Playwright 1.62 protocol support, native animation
semantics and bounded input-event waits. Browser installation now verifies
GitHub SHA-256 digests and stages updates with rollback protection.

The release is built from `a4ee8f934ca1cde9ac6ace007caba8e93fe37316`.
[Full seven-target validation build](https://github.com/Mx-ms-procoder/camoufox_tuned/actions/runs/34050776230).
Each archive includes `build-info.json`; matching SHA256SUMS files accompany
the assets. The embedded patch list is in manifest order, while execution uses
bootstrap patches followed by feature patches sorted by filename.

Remaining limits: personas are not fully isolated per BrowserContext; use
separate browser processes for independent identities. Graphics masking does
not cover every packed, float or integer WebGL format. CPU mapping for PBO
noise may affect readback performance. Full network/TLS parity and universal
undetectability are not established.

See the repository's `audits/2026-09-05/REPORT.md` and `REMEDIATION.md` for
findings, reproducible evidence and the current validation status.
