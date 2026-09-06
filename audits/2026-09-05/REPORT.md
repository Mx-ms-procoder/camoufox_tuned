# Schwachstellenanalyse Camoufox_tuned
Stand: 5. September 2026. Untersucht: Branch `windows-msvc-migration`, Commit `c8105670e50cd27cd14582131664d73f10616a3c`.

Nachfolgende Korrekturen und ihr Validierungsstand stehen in [REMEDIATION.md](REMEDIATION.md). Dieser Bericht beschreibt den ursprünglichen Prüfstand.

Der größte Handlungsbedarf liegt beim Sicherheitsstand von Gecko und bei abgeschwächter Isolation. Daneben wurden mehrere Fehler der Fingerprint-Schichten im installierten Browser reproduziert. Zusätzliche Maskierung allein würde diese Probleme nicht lösen: Die vorhandenen API-Pfade müssen dieselben Daten und dieselbe Browsersemantik liefern.

## Prüfgegenstand und Aussagekraft

Der lokale Branch stimmt mit dem abgefragten GitHub-Branch überein. Er enthält Firefox **152.0.4-beta.27**, einschließlich ausgewählter späterer Upstream-Korrekturen. Die Versionsbezeichnung allein beschreibt seinen Patchstand deshalb unvollständig. Der neueste abgefragte Upstream-Release ist **152.0.4-beta.30 vom 1. September**. Auch dieser liegt beim Gecko-Sicherheitsstand hinter Mozilla zurück. [Upstream-Release](https://github.com/daijro/camoufox/releases/tag/v152.0.4-beta.30), [Mozilla-Versionen](https://product-details.mozilla.org/1.0/firefox_versions.json).

Tatsächlich getestet wurde `C:/Users/maxim/AppData/Local/camoufox/camoufox/Cache/camoufox.exe`, Version **152.0.4-beta.27**, BuildID **20260826163234**, EXE-SHA256 **2f0d7c2015477a9a76fe317d1d43502c5eb1c4816f4b3afba2158293fe22be43**. Die GitHub-Build-Pipeline für den geprüften Commit war erfolgreich. Builddatum, Version und Konfiguration passen zum untersuchten Stand; eine lückenlose, kryptografisch bestätigte Zuordnung aller Binärbestandteile zum Fork-Commit wurde nicht hergestellt. [Build](https://github.com/Mx-ms-procoder/camoufox_tuned/actions/runs/32962260634), [Binär-Hashes](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/binary-hashes.json).

Geprüft wurden Patchserie, C++-Zusätze, Juggler, Python-Launcher, Einstellungen, Build-/Installationspfade, Tests und die festgeschriebenen Python-Abhängigkeiten. Hinzu kamen 45 gefundene Issues und 35 Pull Requests, gezielte Detailabfragen, fünf Upstream-Releases, Mozilla-Advisories und originale Gecko-152.0.4-Quellen. Die Issue-Auswahl ist eine gezielte Recherche, keine vollständige Sichtung jedes historischen GitHub-Kommentars. [GitHub-Snapshot](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/github-snapshot.json), [Quellenmanifest mit Hashes](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/public-fetch-manifest.json).

**Evidenzklassen:** B = im Quellcode, einer deterministischen Probe oder dem installierten Browser bestätigt; W = wahrscheinlich, mit nachvollziehbarem Codepfad und/oder passendem Upstream-Befund; T = theoretisches oder noch ungetestetes Risiko. Ein bestätigter veralteter Versionsstand beweist nicht automatisch die Ausnutzbarkeit jeder CVE im konkreten Build.

**Severity:** Kritisch/Hoch bei Sicherheit bezeichnen mögliche Kompromittierung beziehungsweise Verlust einer wesentlichen Schutzgrenze. Hoch bei Fingerprint-Kohärenz bedeutet einen zuverlässig auslesbaren Widerspruch oder das Umgehen einer vorgesehenen Maskierung, keine automatisch nachgewiesene Codeausführung. Die Priorität berücksichtigt beides; es wurden keine künstlich präzisen CVSS-Werte für Eigenbefunde vergeben.

## Priorisierte Befunde

| Rang | Befund | Severity / Bereich | Evidenz | Priorität |
|---|---|---|---|---|
| 1 | Gecko 152.0.4 liegt hinter kritischen Sicherheitskorrekturen | Kritisch / Sicherheit | B Versionslücke; W konkrete CVE-Betroffenheit | P0 |
| 2 | Site Isolation durch Fission-Einstellungen abgeschaltet | Hoch / Sicherheit | B Konfiguration | P0 |
| 3 | RLBox-Sandboxen für Drittbibliotheken beim Build deaktiviert | Hoch / Sicherheit | B Buildvorgabe | P0 |
| 4 | Sicherheitsmonitor meldete fälschlich Entwarnung | Hoch / Sicherheitsprozess | B; lokal repariert | P0 |
| 5 | WebGL2-PBO-Auslesen umgeht konfigurierte Readback-Noise | Hoch / Fingerprint | B Browser | P1 |
| 6 | WebGL-Packing verändert nicht angeforderte Bufferbereiche | Mittel / Korrektheit | B Browser | P1 |
| 7 | AudioBuffer liefert je nach Leseweg andere Samples | Hoch / Fingerprint, Mittel / Kompatibilität | B Browser | P1 |
| 8 | CSS-Bildschirmgröße widerspricht screen.width bei Viewport-Override | Hoch / Kohärenz | B Browser | P1 |
| 9 | Main-World-Init-Skripte erreichen die Seite trotz Opt-in nicht | Hoch / zugesicherte Funktion | B Browser | P1 |
| 10 | Moderne Playwright-Nachricht wird vom Protokoll abgelehnt | Hoch / Start-/Kontextkompatibilität | B Schema; W Installationsauswirkung | P1 |
| 11 | Downloader kann den Fork durch Upstream ersetzen; Integritäts-/Rollback-Lücke | Hoch / Distribution, Mittel / Integrität | B Code; T Missbrauch | P1 |
| 12 | 12 gepinnte Python-Pakete mit Advisory-Treffern | Potenziell Hoch, abhängig vom Aufrufpfad | B Versionsabgleich; meist T Erreichbarkeit | P1 |
| 13 | Öffentliche IP wird bei rotierenden Proxy-Ausgängen dauerhaft gecacht | Hoch / Netzwerkkohärenz | B gemockter Ablauf | P1 |
| 14 | Font-Abstände beschädigen komplexes Shaping wahrscheinlich weiter | Mittel / Darstellung, Kohärenz | B Code; W Browserauswirkung | P1 |
| 15 | Endliche Animationen werden grundsätzlich auf 0 verkürzt | Mittel / Kompatibilität, Fingerprint | B Browser | P1 |
| 16 | Kontext-Isolation der Persona ist architektonisch unvollständig | Mittel; bei mehreren Identitäten Hoch / Isolation | B Architektur; W/T Folgen | P2 |
| 17 | Test-Baseline und World-Auswahl lassen wichtige Regressionen unentdeckt | Mittel / Qualitätssicherung | B Code und Abdeckung | P1 |
| 18 | Fehlende Input-ACK kann globale Eingabekette blockieren | Mittel / Stabilität | W; lokale Kurzprobe ohne Hänger | P2 |
| 19 | Überstrenge Geräteplausibilität und vermeidbare Arbeit in heißen Pfaden | Mittel / Qualität, Performance | B/W, siehe Details | P2 |

### 1. Sicherheitsstand von Gecko — P0

**Ursache:** [upstream.sh](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/upstream.sh) pinnt 152.0.4. Mozilla nennt bereits für **152.0.6 vom 14. Juli** zwei kritische Korrekturen: **CVE-2026-15718** in JavaScript/WebAssembly und **CVE-2026-15719** in DOM/Navigation/Site Isolation. Mozilla nennt öffentlich verfügbaren Exploit-Code, aber keine bekannten Angriffe in freier Wildbahn. Aktueller Release laut offizieller Versionsdatei: **155.0.1**. Weitere Sicherheitsreleases: 153, 154 und 155. [MFSA 2026-67](https://www.mozilla.org/en-US/security/advisories/mfsa2026-67/), [153](https://www.mozilla.org/en-US/security/advisories/mfsa2026-68/), [154](https://www.mozilla.org/en-US/security/advisories/mfsa2026-74/), [155](https://www.mozilla.org/en-US/security/advisories/mfsa2026-82/).

**Auswirkung:** Für einen Browser, der fremdes JavaScript und Medien verarbeitet, ist der Rückstand ein vorrangiges Sicherheitsrisiko. Im geprüften Fork wurde kein dokumentierter Backport dieser Korrekturen gefunden. Ein Exploit wurde nicht ausgeführt; die exakte Anwendbarkeit einzelner CVEs auf sämtliche eigenen Änderungen bleibt gesondert zu prüfen. Die Abschaltung der RLBox-Bibliothekssandboxen deaktiviert nicht JavaScript-WebAssembly und beseitigt diesen Befund nicht.

**Verbesserung:** Auf einen aktuell unterstützten Gecko-Stand rebasen oder nachweislich alle erforderlichen Security-Backports einspielen. Jede CVE mit Patch/Commit und Release-Artefakt verknüpfen. Für kritische aktive oder öffentlich ausnutzbare Lücken eine kurze verbindliche Reaktionsfrist vorsehen. Ein bloßer UA-/Versionsstring-Wechsel oder das Update auf Camoufox beta.30 reicht nicht. Der eingebaute Updater ist in [base.mozconfig](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/assets/base.mozconfig:21) und [camoufox.cfg](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/settings/camoufox.cfg:680) deaktiviert; der eigene Veröffentlichungsprozess muss diese Aufgabe zuverlässig übernehmen.

### 2. Fission abgeschaltet — P0

**Ursache/Evidenz:** [camoufox.cfg:92](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/settings/camoufox.cfg:92) setzt `fission.autostart=false` und `fission.webContentIsolationStrategy=0`; dieselben Werte stehen im installierten Cache. Die Begründung im Kommentar, Site Isolation sei ein zu vermeidendes WAF-Signal, rechtfertigt diese Sicherheitsabsenkung nicht. Mozilla beschreibt ausdrücklich die zusätzliche Prozessgrenze zum Schutz der Daten anderer Sites. [Mozilla zur Site Isolation](https://blog.mozilla.org/security/2021/05/18/introducing-site-isolation-in-firefox/).

**Auswirkung:** Eine zentrale zusätzliche Barriere gegen seitenübergreifende Angriffe entfällt. Dies ist ein bestätigter Hardening-Verlust, kein hier demonstrierter Cross-Origin-Read. Die übrige Content-Prozess-Sandbox ist damit nicht pauschal abgeschaltet.

**Verbesserung:** Fission als Standard wieder aktivieren. Vor Veröffentlichung gezielt OOP-Iframes, Popups, Navigation, Juggler-Zielzuordnung und Kontextzustand testen. Eventuelle Automationsfehler dort korrigieren. Eine notwendige Legacy-Ausnahme sollte eng begrenzt und als abweichendes Sicherheitsprofil sichtbar sein.

### 3. RLBox-Abschaltung — P0

**Ursache/Evidenz:** [base.mozconfig:31](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/assets/base.mozconfig:31): `--without-wasm-sandboxed-libraries`. Damit werden normalerweise isolierte native Bibliotheken ohne diese zusätzliche Einhegung gebaut. Betroffen sind laut Mozilla unter anderem Font-, XML-, Audio- und Wörterbuchverarbeitung. Der Buildschalter ist bestätigt; die effektiven Configure-Flags des installierten xul.dll wurden nicht separat extrahiert. [Mozilla RLBox](https://firefox-source-docs.mozilla.org/rlbox/index.html).

**Auswirkung:** Speicherfehler einer Bibliothek können größere Auswirkungen innerhalb des Prozesses haben. Zusätzlich ist der alternative Noop-Pfad weniger verbreitet und verlangt besondere Prüfung der Callback-/Threading-Annahmen. Hieraus wird kein konkreter Hunspell- oder WOFF2-Exploit abgeleitet.

**Verbesserung:** Standard-Sandboxen wieder aktivieren und Plattformprobleme gezielt beheben. Falls ein eingeschränkter Container eine bestimmte Unterstützung nicht bietet, separat isolierten Build mit expliziter Begründung führen. Unter ASan/TSan Bibliotheks-Callbacks, paralleles Laden vieler Fonts und Audio-Dekodierung prüfen. Upstream-Problem [#740](https://github.com/daijro/camoufox/issues/740) ist kein genereller Grund, diesen Schutz überall zu entfernen.

### 4. Sicherheitsmonitor mit falschem Grün — P0, lokal repariert

**Ursache:** Der alte Parser erwartete Tabellenzeilen, Mozilla liefert Datumsüberschriften mit Advisory-Links und verschachtelten Spans. Zusätzlich erkannte der Versionsparser bloße Hauptversionen wie `153` nicht. Netzwerkfehler führten ebenfalls zu einem erfolgreichen Exit.

**Reproduktion:** Gespeicherter echter Mozilla-Index → **0 Datensätze, Exit 0, „no newer MFSA found“**. Nach Reparatur → **163 Datensätze, vier neuere Advisories, Exit 1**. [Vorher](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/source-probes.json), [Nachher](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/security-monitor-after.json).

**Umgesetzt:** HTMLParser für das aktuelle Format, historischer Fallback, Hauptversions-Erkennung, Status `error`/Exit 2 bei fehlgeschlagenem Abruf oder nicht auswertbarer Antwort. Sieben Regressionstests ergänzen die Suite. [Script](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/scripts/check_upstream_security.py), [Tests](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/pythonlib/tests/test_upstream_security_check.py).

**Noch erforderlich:** Änderung veröffentlichen und den Check in der tatsächlich verwendeten Release-Pipeline erzwingen. Der bestehende Wochenplan allein garantiert keine zeitnahe Reaktion; GitHub-Zeitpläne laufen auf dem Default-Branch. Aktuellen Release-Kandidaten und veröffentlichtes Artefakt getrennt prüfen. Diese Reparatur aktualisiert den Browser selbst noch nicht.

### 5. WebGL2-PBO umgeht Noise — P1

**Ursache:** [webgl-readback-noise.patch](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/patches/media/webgl-readback-noise.patch:11) verändert den direkten TypedArray-Pfad für `UNSIGNED_BYTE`. Der Pixel-Pack-Buffer-Pfad mit anschließendem `getBufferSubData` wird nicht entsprechend transformiert. Andere Datentypen werden ausdrücklich ausgeschlossen; deren Erreichbarkeit und Verhalten sind zusätzlich zu testen.

**Reproduktion:** Dasselbe 64×64-Bild über beide Wege auslesen. Seed 0: **0 abweichende Bytes**. Seed 111: **1.160**, Seed 222: **1.211**. Der PBO-Hash bleibt bei allen drei Seeds identisch und entspricht dem direkten Ergebnis mit Seed 0. Wiederholtes identisches Zeichnen liefert im direkten Pfad dagegen denselben seedabhängigen Hash. [Browser-Evidenz](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/runtime-results.json).

**Auswirkung/Verbesserung:** Die konfigurierte Readback-Schicht ist über einen regulären WebGL2-Pfad umgehbar. Noise an einer gemeinsamen, semantisch passenden Extraktionsgrenze anwenden; direkte/PBO-/zulässige Float-/Integer-Pfade auf Gleichwertigkeit prüfen. Dabei Buffer-Wiederverwendung, Offsets und mehrfaches Auslesen berücksichtigen. Die Probe beweist den Pfadunterschied, nicht die Identifizierung einer bestimmten realen GPU.

### 6. WebGL-Packing beschädigt fremde Bereiche des Zielarrays — P1

**Ursache:** [CanvasNoise.hpp](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/additions/camoucfg/CanvasNoise.hpp) kennt weder `PACK_ROW_LENGTH` noch `PACK_SKIP_PIXELS`/`PACK_SKIP_ROWS` und nimmt Alignment 4 an. Bei unerwartetem Layout wird ersatzweise der gesamte Buffer als Pixelspan behandelt.

**Reproduktion:** 8×8-Readback in einen größeren mit Sentinelwerten gefüllten Buffer, RowLength 64 und je 8 Skip-Pixel/-Zeilen. Ohne Noise: **0** Änderungen außerhalb des angeforderten Rechtecks. Seeds 111/222: **20/27 Bytes**, jeweils ohne GL-Fehler. [Evidenz](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/runtime-results.json).

**Auswirkung:** Verfälschte Anwendungsdaten und ein messbarer API-Widerspruch. Alle beobachteten Änderungen lagen innerhalb des zugewiesenen JS-Arrays; **kein nachgewiesener Heap-Overflow**.

**Verbesserung:** Tatsächliches Packlayout, Startoffset, Elementbreite, Rechteckursprung und geprüfte Größenrechnung übergeben. Bei nicht unterstütztem Layout keine pauschale Buffer-Transformation durchführen. Fehler- und Nullflächenpfade müssen unverändert bleiben. Der zusätzliche Helper-Test verändert bei einer Nullfläche Bytes, der echte Browser-Nullflächenaufruf tat dies nicht; letzteres wird deshalb nicht als Browserlücke gewertet.

### 7. AudioBuffer ist abhängig von der Lesereihenfolge — P1

**Ursache:** [audio-fingerprint-manager.patch:319](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/patches/media/audio-fingerprint-manager.patch:319) transformiert bei `RestoreJSChannelData` den ganzen Kanal. `CopyFromChannel` transformiert beim Shared-Buffer-Pfad dagegen nur den Ausschnitt, mit neu gestarteter Zustandsfolge und ohne ursprünglichen Sampleoffset.

**Reproduktion:** Offline gerenderter Kanal mit 2.048 Samples; 128 Samples ab Offset 256 kopieren, dann `getChannelData`, dann denselben Ausschnitt erneut kopieren. Seed 0: **0/128 Abweichungen**. Seeds 111 und 222: jeweils **128/128**. Der zweite Ausschnitt stimmt mit dem vollständigen Kanal überein. [Evidenz](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/runtime-results.json).

**Auswirkung/Verbesserung:** Derselbe logisch unveränderte Buffer liefert unterschiedliche Daten. Das beeinträchtigt Verarbeitung und macht die Änderung erkennbar. Eine kanonische Transformation pro Bufferzustand verwenden oder einen wirklich zufallszugriffsfähigen Algorithmus mit absolutem Sampleindex definieren. Ein zusätzlicher Offsetparameter allein genügt nicht, wenn der Zustand von vorherigen Samples abhängt. Mutationen, Kanalwechsel, Slice-Längen, Wiederherstellung sowie Float-/Byte-Analyser gesondert abdecken.

### 8. Screen und CSS widersprechen sich mit Viewport — P1

**Reproduktion:** Konfigurierte Bildschirmbreite **1664**, Playwright-Viewport **800**: `screen.width=1664`, `matchMedia('(device-width:1664px)')=false`, Abfrage für 800 ergibt true. Mit `no_viewport=True` ergibt dieselbe konfigurierte 1664-Abfrage true. Die abweichende Testbreite vermeidet eine zufällige Übereinstimmung mit dem Host. [Gegenprobe](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/screen-probe.json).

**Ursache:** Juggler setzt bei einer Viewport-Vorgabe den RDM-Modus ([TargetRegistry.js:747](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/additions/juggler/TargetRegistry.js:747)). Gecko hat dafür einen eigenen CSS-Gerätegrößenpfad. Der hinzugefügte Kontextmanager in [screen-spoofing.patch](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/patches/identity/screen-spoofing.patch:363) greift auf separate Storewerte zu; die MaskConfig-/Viewport-/Screen-Pfade sind nicht durchgehend zusammengeführt. [Original-Gecko](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/gecko152-nsMediaFeatures.cpp).

**Verbesserung:** Bildschirm, Viewport und RDM-Emulation ausdrücklich getrennt modellieren und konsistent aus einer Persona beziehen. CSS-device-width muss zur gewählten Bildschirmsemantik passen. Matrix aus Default-Viewport, explizitem Viewport, no_viewport, DPR, Zoom, iframe und Worker einführen. no_viewport ist im getesteten Fall ein funktionierender Workaround, kein allgemeiner Fix.

### 9. Main-World-Init-Skripte bleiben wirkungslos — P1

**Reproduktion:** Rohkonfiguration **`allowMainWorld=true`**; `context.add_init_script('mw: window.__audit_init_marker = "present";')`. Ein Seitenskript liest den Marker selbst und schreibt das Ergebnis ins DOM: **null bei allen drei Seeds**. Die Prüfung verwendet ausdrücklich den Engine-Schlüssel; `main_world_eval` ist nur das entsprechende Python-Launcher-Argument. [Probe](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/run_runtime_probes.py), [Resultate](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/runtime-results.json).

**Ursache:** Die lokale Init-Script-Weiterleitung enthält die neuere Behandlung gewrappter `mw:`-Skripte nicht. Normale Auswertung im isolierten World kann deshalb eine erfolgreiche Änderung vortäuschen, die für Seitenskripte nicht existiert.

**Verbesserung:** Den relevanten Fix aus [Upstream #745](https://github.com/daijro/camoufox/pull/745) inklusive Auflösung des aktuellen Main-World-Globals prüfen und portieren. Ohne Opt-in muss Isolation erhalten bleiben; mit Opt-in muss ein tatsächliches Seitenskript die Wirkung bestätigen. Nicht sämtliche Automation pauschal in die Main World verlagern. Eine von Upstream genannte intermittierende Redirect-Regression wurde hier nicht zusätzlich reproduziert.

### 10. Playwright-Version und Juggler-Schema driften — P1

**Ursache:** [pythonlib/pyproject.toml:38](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/pythonlib/pyproject.toml:38) erlaubt `playwright >=1.55.0` ohne Obergrenze. Das lokale Protokoll kennt das inzwischen gesendete `viewport.isMobile` nicht.

**Reproduktion:** Der Validator aus den tatsächlichen lokalen JS-Dateien akzeptiert die alte Nachricht; dieselbe Nachricht mit `isMobile:false` wird mit „property … is not described in this scheme“ abgewiesen. [Probe](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/protocol_probe.cjs), [Ausgabe](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/protocol-probe.json). Der Laufzeittest verwendete bewusst Playwright 1.55.0; ein kompletter Start mit der neuesten Version wurde nicht behauptet.

**Verbesserung:** Kompatibilitätsmatrix aus Python-Paket, Protokollschema und Browser-Artefakt versionieren. Bis zur Portierung unterstützte Playwright-Versionen begrenzen; danach aktuelle Felder und weitere Schemaänderungen übernehmen. Installation/Start müssen inkompatible Paare früh erklären. [Issue #728](https://github.com/daijro/camoufox/issues/728), [PR #743](https://github.com/daijro/camoufox/pull/743), [Release-Floor #746](https://github.com/daijro/camoufox/pull/746).

### 11. Distribution und Integritätsprüfung — P1

**Ursache:** [pkgman.py:197](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/pythonlib/camoufox/pkgman.py:197) lädt fest aus `daijro/camoufox`. Der Installer übernimmt keine Release-Asset-Digestprüfung und entfernt die bisherige Installation vor erfolgreichem Download/Entpacken ([pkgman.py:320](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/pythonlib/camoufox/pkgman.py:320)).

**Auswirkung:** Ein Fetch oder Cache-Neuaufbau kann eigene Änderungen durch den öffentlichen Upstream ersetzen. Download-/Entpackfehler können eine zuvor funktionierende Installation beseitigen. Fehlende Artefaktprüfung schwächt die Lieferkette; ein aktiver MITM wurde nicht nachgewiesen, HTTPS-Zertifikatsprüfung ist hier aktiv.

**Verbesserung:** Fork-Repository, Kanal und erwartete Build-ID explizit auswählen. Manifest mit Gecko-Revision, Fork-Commit, Patchserienhash, Paket-/Protokollstand und Artefakthash ausliefern; Digest vor Installation prüfen, möglichst mit signierter Herkunftsbestätigung. In temporäres Versionsverzeichnis installieren, prüfen, dann atomar aktivieren und eine Rollback-Version behalten. Positiv: lokale ZIP-Extraktion prüft Pfadausbrüche und Symlinks bereits. [Upstream #726](https://github.com/daijro/camoufox/pull/726) wurde geschlossen, aber nicht gemergt; „closed“ bedeutet hier keinen gelieferten Fix.

### 12. Dependencies — P1, aufrufpfadabhängig

**Methode:** Alle **74 Pins** aus [requirements.lock](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/requirements.lock) wurden gegen die versionsbezogenen PyPI-Advisories abgefragt; **12 Paketversionen** lieferten Treffer, keine Abruffehler. CVE-/GHSA-/PYSEC-Aliase sind keine zusätzlichen unabhängigen Lücken. Die Tabelle nennt Zielstände aus den abgefragten Fixangaben, keine blind anwendbare neue Lockdatei. [Vollständige Daten](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/dependency-advisories.json).

| Paket im Lock | Advisory-Beispiel / Auslöser | Einordnung im Fork | Fixziel aus Abgleich |
|---|---|---|---|
| aiohttp 3.13.5 | u. a. CVE-2026-69244, Parser-DoS | Client/Server-Pfad entscheidet; kein erreichbarer Exploit hier belegt | mindestens 3.14.3 |
| cryptography 43.0.3 | u. a. CVE-2026-26007, Schlüsselvalidierung; weitere Zertifikats-/Wheel-Themen | konkrete Primitive/Wheels prüfen | 49.0.0 für alle erfassten Treffer |
| pyOpenSSL 24.2.1 | CVE-2026-27448/27459, SNI-/DTLS-Callbacks | lokale Testserver-Nutzung beweist diese Callbacks nicht | 26.0.0; zusammen mit cryptography aktualisieren |
| Pillow 10.4.0 | u. a. CVE-2026-25990, präparierte PSD; weitere Decoderfehler | lokaler sichtbarer Einsatz bei Screenshot-Tests; fremde Bildformate gesondert prüfen | 12.3.0 für erfassten Gesamtstand |
| lxml 5.3.2 | CVE-2026-41066, XXE in iterparse/ETCompatXMLParser | kein entsprechender untrusted-XML-Pfad im überprüften Launcher belegt; normale Parser nicht pauschal gleichsetzen | 6.1.0 |
| orjson 3.10.18 | CVE-2025-67221, tiefe dumps-Rekursion | Konfigurationsserialisierung vorhanden; Angreiferkontrolle nicht gezeigt | mindestens 3.11.6; Advisories nennen teils 3.11.5 |
| requests 2.32.5 | CVE-2026-25645, temporärer Pfad in extract_zipped_paths | normale HTTPS-Nutzung belegt keinen Trigger | 2.33.0 |
| h2 4.3.0 | CVE-2026-71554, doppelte Pseudoheader | Serverrolle und konkrete Nutzung prüfen | 4.4.1 |
| click 8.1.8 | CVE-2026-7246, click.edit | kein Aufruf von click.edit gefunden | 8.3.3 |
| Twisted 24.7.0 | CVE-2026-42304, DNS-Dekompression | vorhandener HTTP-Testserver ist kein DNS-Server | 26.4.0 |
| pytest 8.3.5 | CVE-2025-71176, lokaler Unix-/tmp-DoS | kein Windows-Browser-Runtime-Befund | 9.0.3 |
| setuptools 82.0.1 | CVE-2026-59890, macOS-/Unicode-MANIFEST | Build-/sdist-Risiko | 83.0.0 |

Primärquellen für besonders relevante Beispiele: [aiohttp-Advisory](https://github.com/aio-libs/aiohttp/security/advisories/GHSA-cq5v-8q36-5273), [lxml-Advisory](https://github.com/lxml/lxml/security/advisories/GHSA-vfmq-68hx-4jfw), [orjson-Versionsdaten](https://pypi.org/pypi/orjson/3.10.18/json), [Pillow-Versionsdaten](https://pypi.org/pypi/Pillow/10.4.0/json). Für jedes weitere Paket steht die versionsgenaue Primär-URL in der Evidenzdatei.

**Verbesserung:** Runtime-, Build- und Testabhängigkeiten trennen, Resolver-Lock mit Hashes neu erzeugen und den unterstützten Python-/OS-Bereich prüfen. Die alte pyOpenSSL-Bindung nicht beim cryptography-Upgrade übergehen. Neue Hauptversionen können Python-3.9-Unterstützung ändern; zunächst Supportentscheidung treffen. Browserforge-/Profil-Daten ebenfalls versionieren. Native Gecko-Bibliotheken, mitgelieferte OpenSSL-Wheels und der experimentelle Go-Proxy benötigen zusätzlich einen Artefakt-SBOM-/OSV-/govulncheck-Abgleich; der Python-Pin-Scan deckt sie nicht ab.

### 13. Rotierende Proxys und IP-Cache — P1

**Ursache:** [ip.py:87](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/pythonlib/camoufox/ip.py:87) verwendet `lru_cache(maxsize=None)` für die öffentliche IP, mit Proxy-URL als Schlüssel.

**Reproduktion:** Erster Ausgang `192.0.2.10`; derselbe Proxy-Endpunkt würde anschließend `198.51.100.20` liefern. Zweiter Aufruf gibt weiterhin die erste IP zurück, **ohne Netzwerkanfrage**. TEST-NET-Adressen und gemockte Antworten, kein echter Proxywechsel. [Evidenz](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/source-probes.json).

**Auswirkung/Verbesserung:** GeoIP, Zeitzone und WebRTC-Maskierung können an einer alten Exit-IP hängen, obwohl HTTP bereits einen anderen Ausgang verwendet. Cache an die konkrete Proxy-Lease/Session binden, kurz befristen und bei Rotation invalidieren. IPv4/IPv6 getrennt erfassen und die Persona vom gleichen nachgewiesenen Ausgang ableiten. Nebenbei hält der unbeschränkte Cache alle unterschiedlichen Schlüssel, gegebenenfalls einschließlich Proxy-Zugangsdaten, im Prozessspeicher.

### 14. Fonts: kumulative Glyphenverschiebung — P1

**Ursache/Evidenz:** [anti-font-fingerprinting.patch:832](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/patches/identity/anti-font-fingerprinting.patch:832) verändert Advances und addiert zusätzlich `cumulativeOffset` zu Glyphenpositionen. Der zum Upstream-Bericht über thailändischen/komplexen Text passende Mechanismus ist lokal noch vorhanden. [Issue #741](https://github.com/daijro/camoufox/issues/741), [Fix #743](https://github.com/daijro/camoufox/pull/743).

**Auswirkung:** Lange Shaping-Runs, kombinierende Zeichen und Ligaturen können verrutschen; Layout und gemessene Textbreite werden auffällig. Die konkrete Thai-Darstellung wurde hier nicht im Browser visuell reproduziert, daher W.

**Verbesserung:** Kumulative Positionierung nicht zusätzlich zur bereits veränderten Fortschreibung anwenden. Kombinierende Nullbreitenzeichen und Clustergrenzen respektieren; Thai, Arabisch, Devanagari, Ligaturen und vertikalen Text gegen native Referenzen testen. Systemfont- und Fontlisten-Schichten sind bereits vorhanden; nicht einfach weitere Schriftarten ausblenden. Bundled Fonts sind auch im lokalen macOS-Build aktiviert, sodass der frühere reine Buildschalterfehler nicht übernommen wurde.

### 15. Animationen verlieren reguläre Semantik — P1

**Ursache:** [no-css-animations.patch](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/patches/security/no-css-animations.patch:5) setzt die Dauer endlicher Effekte in `GetComputedTimingAt` auf null.

**Reproduktion:** Effekt mit angeforderten **1000 ms** meldet in ComputedTiming **0 ms Dauer und 0 ms activeDuration**. Bei allen Seeds bestätigt. [Browser-Evidenz](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/runtime-results.json).

**Auswirkung/Verbesserung:** Sichtbare Übergänge, Synchronisation und Anwendungen mit Web Animations können anders reagieren; der API-Widerspruch ist leicht messbar. Normale Browsersemantik als Default wiederherstellen. Falls beschleunigte Animationen für eigene Tests gewünscht sind, expliziten Testmodus mit dokumentiertem Verhalten verwenden und nicht als allgemeine Sicherheitsverbesserung führen.

### 16. Persona-Zustand und IPC — P2

**Ursache:** [IdentityStateProvider.hpp](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/additions/camoucfg/IdentityStateProvider.hpp) und [MaskConfig.hpp](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/additions/camoucfg/MaskConfig.hpp) cachen Konfiguration pro Prozess via `call_once`. Daneben existieren zahlreiche per-userContextId-Manager. Nach Entfernung der Page-Setter ist deren privater Initialisierungspfad nicht über alle Flächen einheitlich; globale Fallbacks bleiben wichtig. Per-Kontext-Proxys erzeugen dadurch nicht automatisch per-Kontext-WebRTC-/Locale-/Font-Personas.

**Zusätzlich:** [cross-process-storage.patch](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/patches/core/cross-process-storage.patch:9) prüft am Parent nur das Präfix `roverfox.s.`. Es fehlt dort eine Bindung des angefragten Schlüssels an den berechtigten Senderkontext. Missbrauch setzt Zugriff auf diesen privilegierten IPC-Pfad, etwa nach einer Content-Prozess-Kompromittierung, voraus; gewöhnliches Seiten-JavaScript hat diesen Zugriff nicht. Kein Sandbox-Escape nachgewiesen.

**Verbesserung:** Zunächst eine Persona pro Browserprozess als klare unterstützte Grenze definieren. Für mehrere Personas einen privilegierten, kontextgebundenen Initialisierungsweg mit unveränderlichem Zustand und vollständigem OriginAttributes-Schlüssel entwickeln; privateBrowsingId/Partitionierung, Worker-Vererbung, Prozesswechsel und Bereinigung abdecken. Parentseitige Schlüssel-/Größen-/Typvalidierung und Senderprüfung ergänzen. Page-Setter nicht wieder öffnen.

**T-Risiko:** Profilweit konstante Seeds können selbst ein wiedererkennbares Merkmal zwischen Websites sein. Ob sitegebundene Salts sinnvoll sind, hängt vom Ziel ab: stabile Testpersona versus Schutz vor Cross-Site-Linkability. Das ist eine explizite Produktentscheidung, kein pauschal fehlender Schalter.

### 17. Regressionstests prüfen wichtige Aussagen nicht — P1

**Evidenz:** Die [Firefox-150-Baseline](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/tests/fingerprint_parity/baseline_stock_firefox_150.json) enthält **41 ausstehende von 46 Messfeldern**. Sie kennzeichnet das ehrlich; sie ist dennoch kein belastbarer Paritätsnachweis für Firefox 152. [harness.py:234](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/tests/fingerprint_parity/harness.py:234) liest ein Page-Global über die normale Auswertung, die im isolierten World dessen Inhalt verfehlen kann. Die Stealth-Invarianten erwarten zudem eine vollständig verschwundene webdriver-Property; der getestete Browser liefert `false` bei vorhandener boolescher Property. Vorhandensein allein beweist keine Automation.

**Auswirkung:** 90 ursprüngliche Python-Tests und 37 bestehende C++-Checks waren grün, obwohl die hier geprüften API-Invarianten verletzt wurden. Patch-Konfliktanalyse meldet außerdem **28 Überlappungen als Fehler, 3 Warnungen und 7 erwartete Fälle**; ihr Reportmodus endet trotzdem erfolgreich. Das beweist keinen fehlerhaften Build — der HEAD-Build war erfolgreich — verlangt aber eine bewusst gepflegte Konfliktliste.

**Verbesserung:** Versionsgleiche echte Firefox-Referenzen pro OS/DPR aufzeichnen; Automationseinflüsse separat kennzeichnen. Seitenskripte müssen selbst messen und Ergebnisse über DOM oder lokalen Server zurückgeben. CI muss den fertig gebauten Browser starten und API-Gleichheit, Header, Kontextwechsel und Absturzfreiheit testen. Bestätigte Widersprüche als Regressionen aufnehmen, ausstehende Baselinewerte nicht als bestandene Abdeckung zählen. Patchreihenfolge und bewusst akzeptierte Überlappungen maschinenlesbar pflegen.

### 18. Input-Deadlock bleibt strukturell möglich — P2

**Ursache:** [PageHandler.js:559](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/additions/juggler/protocol/PageHandler.js:559) wartet auf ein passendes Mouse-ACK innerhalb einer global serialisierten Eingabekette. Bounds-Prüfung, gerundete Plattformkoordinaten und ACK-Erwartung sind nicht zentral gekoppelt; die Warteoperation hat dort keine klar begrenzte Frist. [Issue #751](https://github.com/daijro/camoufox/issues/751), [offener PR #755](https://github.com/daijro/camoufox/pull/755).

**Reproduktionsergebnis:** Die lokale kurze Headless-Probe mit Bewegung an y=0 und anschließender Bewegung funktionierte sowohl mit als auch ohne Humanize. **Kein lokaler Hänger bestätigt.** Der Upstream-Fix war zum Abrufzeitpunkt offen. Ein bloßes Ersetzen von `<0` durch `<=0` behandelt nicht sämtliche im neueren PR beschriebenen Koordinaten-/ACK-Ursachen.

**Verbesserung:** Bounds und Dispatch im selben Koordinatensystem zentralisieren; nicht zustellbare Events dürfen keine Renderer-ACK erwarten. Watcher im finally freigeben, begrenzte Wartezeit und Wiederherstellung der Eingabekette ergänzen. Headed Windows/macOS/Linux, mehrere DPR-Werte, Zero-Displacement und wiederholte Randbewegungen testen. [Lokales Ergebnis](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/mouse-probe.json).

### 19. Bestehendes von gut auf sehr gut verbessern — P2

| Ursache und Evidenz | Auswirkung / Gewissheit | Konkrete Verbesserung |
|---|---|---|
| `_panel_exists` verwirft 1080×1920 bei DPR 1, obwohl die eigene Aspect-Regel es akzeptiert. [Probe](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/source-probes.json) | B: legitime Portrait-Geometrie wird durch eine endliche Whitelist abgelehnt | Orientierung, externe Monitore und Skalierung modellieren; ungewöhnlich von unmöglich unterscheiden; weiche Plausibilitätswarnung statt pauschalem Ausschluss |
| `public_ip` kehrt aus einem ThreadPoolExecutor-Kontext zurück, dessen Beendigung auf laufende Requests wartet | B: erste Antwort nach 20 ms, Funktion erst nach 203 ms bei 200-ms-Mitläufer | Gemeinsames Zeitbudget, explizite Future-/Session-Lebensdauer und beschränkten Pool einsetzen; nicht bei jedem Lookup bis zum langsamsten Anbieter warten |
| [timezone-spoofing.patch:351](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/patches/identity/timezone-spoofing.patch:351) erzeugt bei vorhandenem Override jedes Mal neue DateTimeInfo | W: zusätzliche Allokationen/ICU-Cacheverlust in häufigen Date-Pfaden; kein gemessener Durchsatzwert | Pro Realm und tatsächlicher Zeitzonenänderung cachen; korrekte DST-/Reset-Logik beibehalten, CPU und Allokationen benchmarken |
| [canvas-noise.patch](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/patches/identity/canvas-noise.patch:38) klont und transformiert für getImageData die gesamte Surface | B Codekomplexität; W hohe Last bei vielen kleinen Readbacks | Für kleine Rects nur benötigte Daten transformieren oder an den Surface-Zustand gebundenen Cache nutzen; absolute Pixelkoordinaten und Invalidierung erhalten |
| [CanvasNoise.hpp](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/additions/camoucfg/CanvasNoise.hpp) bildet zwei Bits mit minus 1 auf -1,0,1,2 ab | B Helper: maximale positive Änderung 2 trotz behaupteter ±1; rechnerisch asymmetrisch | Unverzerrte symmetrische Verteilung spezifizieren, Grenzen/Clipping testen und Dokumentation berichtigen |

## Abgleich mit wichtigen Upstream-Problemen

| Upstream | Einschätzung für diesen Fork |
|---|---|
| [#749](https://github.com/daijro/camoufox/issues/749) / [#750](https://github.com/daijro/camoufox/pull/750), öffentliche window.setXxx-Setter | Eigenständig bereits entfernt; im Page-World-Test **keine entsprechenden Setter** gefunden. Kein aktueller Befund. |
| [#738](https://github.com/daijro/camoufox/issues/738) / [#745](https://github.com/daijro/camoufox/pull/745), Init-Skripte | Betrifft den Fork, lokal bestätigt; siehe 9. |
| [#728](https://github.com/daijro/camoufox/issues/728), neues Playwright-Protokoll | Fehlendes isMobile lokal bestätigt; siehe 10. |
| [#741](https://github.com/daijro/camoufox/issues/741) / [#743](https://github.com/daijro/camoufox/pull/743), komplexe Fonts | Relevanter Code noch vorhanden; visuelle Auswirkung wahrscheinlich. |
| [#731](https://github.com/daijro/camoufox/issues/731), Speech-Voice-Schema | Eigener Launcher verwendet bereits vollständige Voice-Objekte; der Browser blockiert nicht konfigurierte Host-Voices im vorgesehenen Pfad. Kein gleichartiger Default-Befund; Live-Voice-Enumeration nicht umfassend getestet. |
| [#729](https://github.com/daijro/camoufox/issues/729), WebGL-/Screen-Plausibilität | Eigene Kohärenzprüfung vorhanden. Kein pauschal fehlender Schutz; RDM-Screen-Widerspruch und zu harte Panelregeln bleiben eigene konkrete Befunde. |
| [#721](https://github.com/daijro/camoufox/issues/721), ungenutzter Canvas-Seed | Das verwendete canvas:noiseSeed wirkt im eigenen 2D- und direkten WebGL-Pfad. Der alte Dead-Path-Befund gilt dort nicht mehr; PBO-Abdeckung bleibt unvollständig. |
| [#675](https://github.com/daijro/camoufox/pull/675), route verändert Header | Codefix vorhanden; im lokalen HTTP/1-Test mit route.continue keine zusätzlichen Pragma-/Cache-Control-Header. |
| [#751](https://github.com/daijro/camoufox/issues/751) / [#755](https://github.com/daijro/camoufox/pull/755), Eingabe hängt | Strukturelles Restrisiko; kurze lokale Reproduktion negativ. |
| [#753](https://github.com/daijro/camoufox/issues/753) / [#754](https://github.com/daijro/camoufox/pull/754), appVersion aus Preset | Der dort beanstandete neue Presetpfad ist lokal nicht derselbe. AppVersion im getesteten Windows-Profil passt. Nicht ungeprüft als eigener Bug übernommen. |
| [#650](https://github.com/daijro/camoufox/issues/650) / [#693](https://github.com/daijro/camoufox/pull/693), Windows-Start | Installierter Browser startet in allen ausgeführten Kurzproben; keine aktuelle SxS-Startstörung nachgewiesen. |
| [#708](https://github.com/daijro/camoufox/pull/708), macOS bundled fonts | Lokaler Buildschalter ist vorhanden; macOS-Laufzeit nicht getestet. |
| [#734](https://github.com/daijro/camoufox/issues/734), [#245](https://github.com/daijro/camoufox/issues/245), Resize/Langzeit-Speicher | Offene Zieltests; Headless-Kurzproben schließen diese Probleme nicht aus. |
| [#737](https://github.com/daijro/camoufox/issues/737), Search-Service-Initialisierung | Nicht gezielt reproduziert; Suchdienst-Patches rechtfertigen keine pauschale Einstufung als behoben. |
| Allgemeine „Site X detects“-Issues | Kein Beweis einer konkreten Engine-Lücke. IP-Reputation, Kontozustand, Verhalten und Serveränderungen sind mögliche zusätzliche Ursachen; keine Tests gegen echte Konten oder CAPTCHA-Anbieter durchgeführt. |

## Architektur und Abdeckung der gewünschten Oberflächen

| Oberfläche | Bereits vorhanden / geprüfte positive Evidenz | Noch zu schließen oder zu messen |
|---|---|---|
| Navigator / Betriebssystem | UA, appVersion, Plattform, Sprachen und Kerne in Hauptseite und Dedicated Worker konsistent; webdriver=false | Cross-OS-Personas, Shared-/Service-Worker, OOP-Iframes, UA-BuildID und mehrere Kontexte |
| WebRTC | no_host, default_address_only, proxy_only_if_behind_proxy; SDP-Sanitizer erhält DTLS-Fingerprints; lokales Offer akzeptiert | Echter Proxy-/STUN-/TURN-/IPv6-/mDNS-Netzwerkvergleich; Reconnect, Routewechsel und Kontextproxy. Kein vollständiger IP-Leak-Freibrief |
| WebGL | Eigene Renderer-/Parameterprofile und wirkende direkte Noise | PBO, Packlayout, weitere Pixeltypen, Extension-/Limit-/Shader-Kohärenz, Hardware/Software-Backend |
| Canvas | Seedabhängige Daten; deterministische Helper; Alpha und Rowpadding in vorhandenen Tests erhalten | Crop-/Export-/Offscreen-/Worker-Gleichheit und Performance. Die exportHash-Werte der Probe mit Standard-DrawingBuffer-Lebensdauer wurden bewusst nicht als Leak-Beweis gewertet |
| AudioContext / AudioBuffer | Sample-/Kontext- und Seed-Schichten vorhanden; Helper aktiv | Bestätigten Slice-/Reihenfolgefehler beheben; Wiedergabe, Analyser und Latenzwerte gegen tatsächliches Backend prüfen |
| Fonts / Sprache | Fontlisten, CSS-Systemfonts, Bundled Fonts und Voice-Konfiguration | Komplexes Shaping, Fallback/Unicode-Abdeckung, TextMetrics, FontFace-/CSS-Messungen; Voice-Laufzeittest |
| Locale / Zeitzone | de-DE als Default; explizites ja-JP/en-US bleibt respektiert; Berlin -60 im Januar und -120 im Juli; Dedicated Worker passt | Andere Zeitzonen, historische Übergänge, Date/Intl/Timestamp-Parität, parallele Kontexte; Realm-Cache |
| HTTP-Header | Lokaler UA entspricht Navigator; Accept-Language passt; gzip/deflate/br/zstd; Routefix bestätigt | HTTPS/HTTP2, Redirects, Auth-/Proxy-Header, WebSocket und HTTP3; kein Paketmitschnitt durchgeführt |
| TLS / HTTP2 | Firefox-152-Profil wählt native-nss-runtime; **keine CAMOU_TLS-Overrides, keine HTTP2-Overrides** im lokalen Quellenprobe-Ergebnis | Tatsächlichen Handshake am Draht pro OS/Proxy/ALPN messen. Alte starre Firefox-135-Profile wurden nicht als aktueller Standard unterstellt |
| DNS / Proxy | SOCKS-Remote-DNS und kein direkter Proxy-Failover gesetzt; IP-Lookup prüft TLS | Rotierende Ausgänge, IPv6 und Fehlerfälle auf Netzwerkebene verifizieren |
| Screen / Eingabe | Viele native Hooks, eigene Plausibilität, Randkorrekturen vorhanden | RDM-Kohärenz, DPR/Zoom/Portrait, ACK-Resilienz, echte Touch-/Pointer-Fähigkeiten |
| Isolation / Lifecycle | Isolierte Automation-World und entfernte Setter schützen die Page-Oberfläche | Fission/RLBox, privilegierte Persona-Initialisierung, Crash-Recovery, BFCache und Langzeit-Ressourcen |
| Weitere APIs | Fehlende eigene Patchdatei ist noch kein Leak-Beweis | Capability-gesteuerte Bestandsaufnahme für WebGPU, OffscreenCanvas/ImageBitmap, WebCodecs/MediaCapabilities, CSS-Farb-/Gamut-/Pointer-Medienmerkmale und Timing. Nur tatsächlich exponierte APIs bewerten; keine erfundenen Chrome-Fähigkeiten hinzufügen |

Die Architektur deckt viele wesentliche Oberflächen ab. Die belegten Defizite liegen vor allem in **unvollständigen alternativen API-Pfaden**, **mehreren konkurrierenden Zustandsquellen**, **veralteter Engine** und **fehlenden Tests am fertigen Browser**. Mehr unabhängige Zufallswerte würden die Kohärenz eher erschweren. Eine Persona sollte aus überprüften, zusammenpassenden Daten bestehen und konsistent über alle beteiligten Prozesse und Auslesewege sichtbar sein.

## Validierung und Grenzen

- **97/97 Python-Tests** nach der Monitor-Reparatur bestanden: 90 bestehende, sieben neue. [JUnit](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/python-tests.xml).
- **37/37 vorhandene C++-Helperchecks** bestanden: Canvas 8, Audio 12, SDP 17, lokal mit g++/C++17 kompiliert. Das ist keine MSVC-Gecko-Vollbuildprüfung. [Ausgabe](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/cpp-tests.txt).
- Patchmanifest-Validierung erfolgreich; 2 Bootstrap- plus 58 Feature-Patches. Überlappungsreport wie oben erläutert.
- Aktuelle Browser-Evidenz: drei frische Prozessläufe mit Seeds 0/111/222, separate Screen-Modi und zwei Humanize-Modi. Hauptproben wurden während der Entwicklung wiederholt; die gespeicherten JSON-Dateien enthalten den finalen Stand. Alle Testseiten waren lokal bzw. data:-Seiten, ohne echte Benutzerprofile.
- Python 3.12 in isolierter Audit-Umgebung; Playwright **1.55.0**. Direkte Abhängigkeiten wurden passend gewählt, einige transitive Testabhängigkeiten neu aufgelöst. Das ist **kein vollständiger Ausführungstest der gesamten ursprünglichen Lockdatei**. [Umgebung](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/test-environment.txt).
- Kein vollständiger Gecko-Neubau, kein Exploit-PoC gegen CVEs, kein ASan/TSan-/Fuzzing-Durchlauf, kein mehrstündiger Leak-/CPU-Test, keine Windows-Headed-/Linux-/macOS-Matrix, kein echter STUN/Proxy-/TLS-/HTTP2-Mitschnitt.
- Das Audit beansprucht weder Fehlerfreiheit aller Quellzeilen noch universelle Unerkennbarkeit. Nicht reproduzierte Upstream-Reports und Versions-Advisories wurden nicht zu bestätigten Remote-Exploits hochgestuft.

## Konkrete Reihenfolge der Verbesserung

1. **Sicherheitsbasis herstellen:** unterstützten Gecko rebasen, relevante CVEs dokumentieren, Fission/RLBox zurückbringen und notwendige Juggler-Anpassungen testen. Den reparierten Monitor in den Releasepfad übernehmen.
2. **Reproduzierte Widersprüche beseitigen:** WebGL-PBO/Packlayout, Audio-Slices, Viewport-Screen, Main-World-Init und Animationen. Jede Korrektur gegen die gespeicherten Proben am neu gebauten Browser verifizieren.
3. **Installierbare Kombination absichern:** Playwright-Kompatibilitätsgrenzen, eigener Artefaktkanal, Digest/Provenienz, atomare Installation und aktualisierte getrennte Dependency-Locks.
4. **Qualität erhöhen:** Font-Shaping, Proxy-Lease-Zustand und private Persona-Verteilung vereinheitlichen; Referenzmatrix und Langzeit-/Plattformtests aufbauen. Erst anschließend weitere tatsächlich exponierte API-Flächen ergänzen.

Bereits geändert wurden nur der Sicherheitsmonitor, sein Workflow-Kommentar und sieben Regressionstests; zusätzlich wurden Audit-Proben und Evidenzdateien angelegt. Die Browser-Engine wurde nicht neu gebaut, installiert oder veröffentlicht. Die übrigen Empfehlungen sind damit klar vom bereits umgesetzten Fix getrennt.

[Reproduktionsanleitung](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/REPRODUCE.md).
