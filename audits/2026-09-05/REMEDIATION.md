# Umsetzung und verbleibende Grenzen

Stand: 6. September 2026. Ausgangspunkt ist Commit
`c8105670e50cd27cd14582131664d73f10616a3c`; die ursprünglichen Messungen in
[REPORT.md](REPORT.md) und `evidence/` bleiben nachvollziehbar.
Zielstand: Gecko **155.0.1**, Camoufox **beta.31**, Python-Paket **0.4.13**,
Playwright **1.62.0**. Der vollständige Build von Commit `a4ee8f934ca1cde9ac6ace007caba8e93fe37316` ist auf allen sieben Zielplattformen erfolgreich.
Der Release-Run für `build-0.21` und die Laufzeitprüfungen sind noch in Arbeit.
[Erfolgreicher Build](https://github.com/Mx-ms-procoder/camoufox_tuned/actions/runs/34050776230).

## Zuordnung zu den Audit-Befunden

| Nr. | Umsetzung | Nachweis / verbleibende Prüfung |
|---|---|---|
| 1 | Alle aktiven Patches auf originales Gecko 155.0.1 portiert; erledigten Vulkan-Fix entfernt. Neue Geolocation-, Font-, Wasm-, WebRTC- und macOS-APIs berücksichtigt. | 57 Patches lassen sich mit GNU patch `--fuzz=0` vollständig anwenden. Das ersetzt keinen Compiler-/Laufzeitnachweis. |
| 2 | Fission aktiviert, `webContentIsolationStrategy=1`. | Konfiguration korrigiert; tatsächliche Prozessaufteilung im neuen Browser prüfen. |
| 3 | RLBox-Ausschluss entfernt; Mozilla-Bootstrap einschließlich WASI auch für Linux aktiviert. | Linux-Buildprotokoll bestätigt RLBox, wasm2c und erzeugte Sandbox-C-Stubs; siehe remediation/rlbox-build-evidence.json. Laufzeitschutz ist dadurch nicht vollständig bewiesen. |
| 4 | Sicherheitsmonitor vergleicht den vollständigen aktuellen Release-Stand, Fehler sind kein Erfolg mehr. | Python-Regressionstests für veraltete Versionen und fehlerhafte Antworten. |
| 5–6 | WebGL-Readback-Noise in den gemeinsamen Host-Pfad verschoben, einschließlich PBO; tatsächlicher Ausschnitt, Stride, Skip-Werte und Grenzen werden berücksichtigt. Interne Compositor-Lesewege bleiben unverändert. | Sieben C++-Layouttests. Browser-/GPU-Test steht aus. Float-, gepackte und Integer-Formate werden weiterhin nicht vollständig maskiert. |
| 7 | Stateless Audio-Hash nutzt absoluten Sample-Index; `copyFromChannel` reicht den Offset weiter. | 16 Audio-Helper-Checks einschließlich Teilbereichen; native AudioBuffer-Rückprüfung steht aus. |
| 8 | CSS-Screen-Abfrage übernimmt gültige konfigurierte Screen-Dimensionen auch ohne Storage-Eintrag. | Quellcodekorrektur; RDM-/Viewport-Probe mit neuem Browser erforderlich. |
| 9 | `mw:`-Init-Skripte werden mit Opt-in im Seitenkontext ausgeführt; Main-World-Kontext wird bei Navigation erneuert. | Juggler-Parser-/Lifecycle-Tests; vollständige Navigation im Browser erforderlich. |
| 10 | Fehlendes `viewport.isMobile` im Juggler-Schema ergänzt, Python an Playwright 1.62 gebunden. | Schema und Python-Tests; weitere Protokollkompatibilität benötigt Browser-Smoke-Tests. |
| 11 | Downloader standardmäßig auf diesen Fork; SHA-256 aus GitHub-Assetmetadaten, exakter Assetname und Repository-URL; Staging, Commit-Sperre und Rollback. Paket enthält Build-Provenienz. | Tests für Download-Abbruch, falschen Hash, Rollback, konkurrierende Installer und Sperrfreigabe. Schutz hängt weiterhin an GitHub/Repository-Zugriffssicherheit. |
| 12 | Python-Lockdatei einschließlich transitiver Sicherheitsuntergrenzen aktualisiert. Go-Toolchain auf 1.27.1. | 76 Python-Versionen ohne nicht zurückgezogene PyPI-Advisories; Momentaufnahme, keine Erreichbarkeits- oder Zukunftsgarantie. Go-Build/Vet erfolgreich; govulncheck: 0 verwendete verwundbare Pakete/Symbole. GO-2026-5932 betrifft das nicht importierte OpenPGP-Paket; siehe remediation/go-vulnerabilities.txt. |
| 13 | Unbegrenztes IP-Ergebnis-Caching entfernt; erste erfolgreiche Antwort gewinnt, mit Zeitlimits und gemeinsamem Executor. | Tests mit wechselnden Ausgängen und verzögertem Provider. Gleichzeitige Proxyrotation zwischen Messung und Browserrequest bleibt möglich. |
| 14 | Kumulative Glyphenverschiebung entfernt; keine zusätzliche Verschiebung von Null-Advance-Glyphen und inneren Clusterteilen. | Patchprüfung; komplexes Shaping visuell und mit nativen Textmetriken prüfen. |
| 15 | Patch zum Nullsetzen endlicher CSS-Animationen entfernt. | Native Gecko-Semantik wiederhergestellt; Browserprobe erforderlich. |
| 16 | Ungenutzten schreibenden Content→Parent-Storage-IPC entfernt; lesende Schlüssel und Zahlenwerte validiert. Automatische Privatfenster-Berechtigung für alle Add-ons entfernt. | Angriffsfläche reduziert. Persona weiterhin nicht vollständig pro BrowserContext isoliert: für unabhängige Identitäten getrennte Browserprozesse verwenden. |
| 17 | DOM-Auswertung repariert, native WebDriver-Property-Form erwartet; offizieller Firefox lässt sich ohne Juggler erfassen. Optionaler strenger Baseline-Check. | Offizieller Firefox 155.0.1 auf Windows headless wurde mit 48 Feldern gemessen; Baseline und Binär-/Installer-Hashes liegen unter remediation/. Historische FF150-Baseline bleibt partiell. Kein vollständiger Paritätsnachweis durch übersprungene Felder. |
| 18 | ACK-/TabSwitch-Wartezeiten begrenzt; EventWatcher entfernt Listener und Pending-Waiter auch bei Fehler/Dispose. | Fünf Node-Tests. Präzisierung: Der Callback hatte bereits ein 25-s-Limit; unbeschränkt waren insbesondere davorliegende TabSwitch-Wartepfade. Ein ewiger globaler Deadlock wurde nicht nachgewiesen. |
| 19 | Panel-Whitelist wird Kalibrierungshinweis, Rotation berücksichtigt; freie positive endliche DPRs zugelassen. Nativen Gecko-Zeitzonen-Cache wiederhergestellt. | Python-Kohärenztests und Patchvergleich; Performance-Benchmarks im neuen Browser stehen aus. |

## Zusätzliche Qualitätsverbesserungen

- Docker verwendet Python 3.12, die Hash-Lockdatei und denselben Browsercache beim Build und unter dem Dienstbenutzer. Unterdrückte Installations-/Go-Downloadfehler entfernt.
- `glxtest` und `vaapitest` bleiben im Browserpaket, damit native GPU-Erkennung funktionieren kann.
- Jedes Paket enthält `build-info.json` mit Engine, Fork-Commit, geordneter Patchliste und SHA-256; CI erstellt zusätzliche Archivprüfsummen.
- Die durch den Bootstrap ersetzte RemoteSettings-Implementierung und der inaktive alternative Enterprise-Policy-Provider sind auf Gecko-Verhalten zurückgeführt.
- cbindgen-Workaround liest `BudgetType::COUNT` aus dem aktuellen Rust-Quellcode und bricht bei einer unbekannten Struktur ab.

## Verbleibende Architekturarbeit

Eine universelle, widerspruchsfreie Maskierung ist nicht nachgewiesen. Neben der
Persona-Trennung bleiben vollständige WebGL-Formatabdeckung, der Aufwand großer
Canvas-Kopien und End-to-End-Kohärenz von TLS/HTTP2, Proxy-Ausgang, DNS, WebRTC,
Zeitzone und Locale eigenständige Aufgaben. Das experimentelle uTLS-Sidecar wird
weiterhin nicht vom normalen Launcher verwendet und besitzt kein vollständiges
Firefox-155-Profil. PBO-Noise kann durch das notwendige CPU-Mapping GPU-Stalls
verursachen; dies ist gegen reale Workloads zu messen.

Quellen: [Mozilla-Releases](https://product-details.mozilla.org/1.0/firefox_versions.json),
[Mozilla-Sicherheitsmeldungen](https://www.mozilla.org/en-US/security/advisories/),
[offizielle Go-Downloads](https://go.dev/dl/). Die Nachprüfung fand zusätzlich
eine PKCS7-Sicherheitslücke in `cryptography 49`; die Lockdatei verwendet deshalb
Version 50. [Advisory GHSA-g6cj-pr64-35w5](https://osv.dev/vulnerability/GHSA-g6cj-pr64-35w5).

## Ergänzungen nach dem erfolgreichen Build

Die nachfolgenden Build-Fixes des Nutzers sind im Release-Commit enthalten:
Geolocation-Service-Typ in nsDocShell korrigiert, libc6-i386 für Windows/Wine
explizit installiert, den bereits nativen Accept-Language-Override erhalten,
den überflüssigen Realm-Patch entfernt und die erforderlichen
nsPIDOMWindowInlines.h-Includes ergänzt. Auch dieser finale Patchstand lässt
sich mit `--fuzz=0` anwenden (57/57).

Der neue Test `tests/release_smoke.py` schreibt separate Ergebnisse, ohne die
ursprünglichen Befunde zu überschreiben. Eine Negativkontrolle bestätigt mit
Playwright 1.62 den Kontext-Startfehler des alten Browsers wegen `isMobile`.

Im eingebetteten `build-info.json` von build-0.21 ist die Patchliste in
Manifest-Reihenfolge enthalten; sie ist **keine Ausführungsreihenfolge**.
Die tatsächliche Reihenfolge lautet: Bootstrap-Patches zuerst, danach Features
nach Dateinamen sortiert. Die Packaging-Korrektur auf dem Folgecommit schreibt
diese Reihenfolge explizit. Die Patch-Hashes und der Release-Commit sind davon
nicht betroffen. Der vorhandene Release-Tag wird nicht verschoben.
