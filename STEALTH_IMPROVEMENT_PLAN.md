# Stealth-Improvement-Plan

**Stand:** 2026-07-21, nach dem FF150→**152**-Rebase + Windows-**MSVC**-Migration
(7/7 grün, commit-Stand `a9d43ad`+), **empirisch am gebauten Windows-Binary gemessen**.
**Vorgänger-Stand:** 2026-07-04, build-0.13 (FF150).

---

## 0 — Was sich seit build-0.13 geändert hat

- **FF152-Rebase**: 56 Feature-Patches auf FF152.0.4-beta.27 rebased, 0 Rejects,
  7/7 CI grün. Anti-Detect-Kern (UA/platform/WebGL/canvas/screen/audio) **per
  Audit als weiter funktionierend bestätigt** (siehe §2).
- **Windows mingw→MSVC**: löst den DllMain-Deadlock an der Wurzel
  (`--enable-bootstrap`, echte VS2022-winsysroot). Das Windows-Binary **startet
  und rendert lokal** (`--version`, Headless-Screenshot) — erstmals in der Saga.
- **Voice-Spoofing** neu verdrahtet (config-driven `MaskConfig::MVoices`), ESM-
  Juggler beibehalten.

---

## 1 — Sprung 2 (CI-Wartung) — ✅ WEITGEHEND ERLEDIGT (durch die MSVC-Migration)

Der 2026-07-04-Plan kritisierte `build.yml` mit **3352 Zeilen / ~30 inline
mingw-Fixups / floatende Pins**. Die MSVC-Migration hat das als Nebeneffekt
gelöst:

- `build.yml` ist jetzt **551 Zeilen** (war 3352). Die ~9 großen mingw-Fixup-
  Steps (GCC-13-Header, freestanding Maybe.h, STL-Wrapper, MinGW source gaps,
  App-SDK, Shader-Compiler) sind **gelöscht** — der clang-cl/MSVC-Pfad braucht
  sie nicht.
- cbindgen ist `=0.29.4` gepinnt (nicht floatend).
- **Verbleibend/offen (P2 klein):** die wenigen verbliebenen inline-Fixups
  (`BudgetType::COUNT`, `ffmpeg-vulkan-nullhandle`, `denormaldisabler-cstdint`)
  sind bereits als **versionierte Patches** bzw. ein ungated Step extrahiert.
  Restaudit floatender Pins (nasm, node, rustup) bleibt sinnvoll (P2.1), aber
  niedrige Priorität.

---

## 2 — Empirisches Stealth-Audit am FF152-Build (2026-07-21)

Gemessen mit einem juggler-freien Probe-Harness (lokaler HTTP-Server + headless
`camoufox.exe`), einmal **roh** (ohne Config) und einmal **konfiguriert** (via
`launch_options`, coherente Identität).

### ✅ Bestätigt intakt (konfiguriert)
| Vektor | Ergebnis |
| --- | --- |
| `navigator.webdriver` | `false` |
| Automation-Globals / `cdc_`/`__playwright`/`__juggler` | **keine** (Option-B hält) |
| User-Agent | zu `Firefox/…` gespooft (kein „Camoufox"-Token bei Config) |
| platform / oscpu / appVersion | kohärent mit UA (z. B. MacIntel + „Intel Mac OS X 10.15") |
| WebGL vendor/renderer | gespooft (echte Intel-GPU versteckt → „Apple M1") |
| screen / dpr / colorDepth | kohärent (Retina 2560×1600, dpr 2) |
| canvas | Noise pro Identität aktiv (Hash ändert sich) |
| `navigator.vendor`/`productSub`/`buildID` | `""` / `20100101` / `20181001000000` (RFP-Wert, korrekt) |

### 🔴 Gefundene Schwachstellen → in dieser Session GEFIXT
1. **Juggler-Automation kaputt** — `chrome://juggler/content/JugglerFrameChild.sys.mjs`
   „Missing chrome URL". Ursache: `additions/juggler/jar.mn` Zeile 22 hatte
   **doppeltes `content/content/`** (Fork wich von Upstream ab), Datei landete
   unter falscher URL. **Fix:** auf `content/JugglerFrameChild.sys.mjs`
   korrigiert (matcht Upstream + das funktionierende Parent-Muster).
2. **Voice-Spoofing leakte die Host-Voices** — eine Windows-Maschine exponierte
   `„Microsoft Hedda - German (Germany)"` über `speechSynthesis.getVoices()`,
   was eine gespoofte macOS/en-US-Identität sofort verrät. Ursache: die
   pythonlib setzte `voices:blockIfNotDefined` nicht → `nsSynthVoiceRegistry`
   registrierte die echten Plattform-Voices zusätzlich. **Fix:** identity.py
   setzt jetzt `voices:blockIfNotDefined=true` (verifiziert: Host-Voices → 0).

### 🟠 Offen / beobachten (kein Quick-Fix)
3. **Voice-Registrierung** — mit `blockIfNotDefined` verschwinden die Host-
   Voices (gut), aber die **Config-Voices erschienen lokal nicht** (0 statt der
   ~53). D. h. `MVoices()::AddVoiceImpl(nullptr,…)` registriert im gebauten
   Binary aktuell nicht enumerierbar. Netto: **0 Voices** (kein Leak, aber
   „Mac mit 0 Stimmen" ist ein milder Tell). **Nächster Schritt:** nach dem
   Rebuild erneut messen; falls weiter 0, die AddVoiceImpl-Timing/Service-Frage
   (SAPI-Async überschreibt evtl. die Registry) prüfen.
4. **UA-Versions-Skew** — der gespoofte UA sagt `Firefox/150.0` (rv:150), die
   Engine ist aber **152**. Die browserforge-Fingerprint-DB ist 150-era. Risiko
   niedrig-mittel (nur 2 Versionen; sophistizierte UA-vs-Feature-Cross-Checks).
   **Fix (Datenaufgabe):** Fingerprint-DB/Version-Constraint auf 152 heben.
5. **WebRTC** — ohne Proxy leakt die echte **öffentliche** IP (STUN-srflx); die
   LAN-IP wird per mDNS korrekt verborgen. Erwartet (der IP-Spoof ersetzt sie
   mit der Proxy-IP). **Option:** WebRTC standardmäßig blocken, wenn kein Proxy
   gesetzt ist (defense-in-depth).
6. **Timezone/Locale** ohne Proxy — reale TZ (`Europe/Berlin`) + `en-US`-Locale
   → Mismatch. Erwartet (TZ kommt aus Proxy-GeoIP). Nur relevant ohne Proxy.

---

## 3 — Sprung 1 (Fingerprint-Parity-Beweis) — ❌ WEITER OFFEN, neu für FF152

Unverändert offen, jetzt **für FF152** neu zu fassen:

- `probes.html` deckt **weiterhin 0 WebRTC- und 0 Font-Vektoren** ab (P1.1).
  → Das juggler-freie Probe-Harness aus §2 (`C:\ff152\work\probe_audit.py`)
  deckt WebRTC/Fonts/Voices bereits ab und kann die Basis für `probes.html`
  werden.
- Baseline `baseline_stock_firefox_150.json`: **42 `__CAPTURE_PENDING__`** und
  gegen **FF150** — für FF152 wertlos, muss gegen Stock-FF**152** neu erfasst
  werden (P1.2, braucht eine Stock-FF152-Installation).
- Harness **nicht in CI** verdrahtet (P1.3).

**Empfehlung:** das §2-Harness als CI-Smoke-Test nach der Build-Matrix
verdrahten (misst das gebaute Binary gegen harte Invarianten: webdriver=false,
keine Automation-Globals, UA-Token≠Camoufox, keine Host-Voice-Leaks, WebRTC-
LAN-IP verborgen) — das ist auch **ohne** Stock-Baseline sofort wertvoll.

---

## 4 — Priorisierung (aktualisiert)

| Prio | Item | Status |
| ---- | ---- | ------ |
| — | Juggler jar.mn-Fix | ✅ gefixt (Rebuild validiert) |
| — | Voice Host-Leak (`blockIfNotDefined`) | ✅ gefixt |
| 1 | Voice-Registrierung (0 Voices) post-Rebuild klären | offen |
| 2 | Invarianten-Smoke-Test in CI (§2-Harness) | offen, hoher Wert |
| 3 | UA-Skew 150→152 (Fingerprint-DB) | offen |
| 4 | WebRTC default-block ohne Proxy | offen, optional |
| 5 | Stock-FF152-Baseline + probes.html WebRTC/Font | offen, braucht Workstation |
| 6 | P2.1 Rest-Pins auditieren | offen, niedrig |

**Nicht umfasst (bewusst):** Runtime-Detection-Scores (CreepJS/DataDome) als
ehrlicher Endbeweis — Sprung 3, braucht externe Dienste.
