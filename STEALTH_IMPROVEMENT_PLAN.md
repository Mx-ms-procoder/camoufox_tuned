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

## 1.5 — Externe Validierung (2026-07-24, am echten build-0.14-Binary)

Erstmals gegen echte externe Detection-Referenzen getestet, nicht nur
Eigen-Probes:

- **CreepJS** (`abrahamjuliot.github.io/creepjs`): **`0% headless`, `0% stealth`,
  `6% like headless`** — CreepJS flaggt uns **nicht** als Automation/Bot. FP-
  Konsistenz `confidence: high` (lang/timezone/GPU/worker kohärent). UA korrekt
  als `Firefox 152` geparst. `ua parsed: Firefox 152` (UA-Skew-Fix wirkt extern).
- **WebGPU — getestet, KEIN Leak (bewiesen, nicht angenommen):** Default meldet
  CreepJS `webgpu: unsupported` (Firefox-eigene gfxInfo-Blocklist → `navigator.gpu`
  undefined; kohärent, häufiger Real-Zustand — Camoufox spooft oft ältere GPUs,
  die WebGPU eh nicht könnten). **Selbst mit erzwungenem Blocklist-Bypass**
  (`gfx.webgpu.ignore-blocklist`, `dom.webgpu.allow-in-parent`) auf einer
  Maschine mit **echter RTX 4070** gibt `requestAdapter()` **null** — stderr:
  *"Failed to find D3D12 adapter with the same LUID that the compositor is
  using!"*. Ursache: Camoufox' **Software-Compositor (SWGL)** hat keine D3D12-
  LUID → WebGPU kann keine Hardware-GPU enumerieren → **die echte GPU leakt NIE
  über WebGPU**, auch nicht bei Zwangs-Aktivierung. Der WebGL-Spoof wird nicht
  durch WebGPU unterlaufen.
- **WebRTC über SOCKS5:** 6 freie SOCKS5-Proxys getestet → **0 ICE-Candidates,
  kein IP-Leak** (freie SOCKS5 unterstützen kein UDP-ASSOCIATE, daher STUN aus →
  die „fabricated priority"-Konsistenz (Upstream-Feature) blieb ungetestet, aber
  es leakt nichts).
- **Voices — Selbstkorrektur:** CreepJS zeigte **131 lokale Stimmen**. Der frühere
  „voices==0"-Befund war ein **Test-Methodik-Fehler** meinerseits: `getVoices()`
  lädt in JEDEM Gecko async (MDN) — ein sofortiger Call gibt überall 0; mit
  `onvoiceschanged`/Retry: **105–131 Stimmen, korrekt.** Kein echter Bug. Der
  `call_once`-Config-Read-Retry (`c401984`) bleibt sinnvolle Robustheit, war aber
  nicht der Voice-Fix, für den ich ihn hielt.

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
1. **Juggler-Automation komplett kaputt (Playwright hängt bei `new_page`)** —
   Root-Cause: der **gesamte Juggler des Forks war ein alter Hand-Rebase
   (17.–25. Mai, FF146-Ära)**, dem eine Reihe FF152-Fixes fehlte, die Upstream
   (`daijro/camoufox` v152.0.4-beta.27) längst hat. Die Juli-FF152-Rebase
   aktualisierte die `patches/`, resyncte aber die alten `additions/juggler/`
   nie mit Upstreams FF152-Juggler. Fünf Fixes (alle gegen Upstream verglichen,
   **lokal am gebauten Binary via omni.ja-Patch verifiziert** — `new_page` +
   `goto` + `evaluate` + DOM-Query + `webdriver=false` laufen):
   - `jar.mn`: doppeltes `content/content/` → `content/JugglerFrameChild.sys.mjs`.
   - `TargetRegistry.js` **gBrowser-Wait**: FF150+ meldet `readyState=complete`
     bevor `gBrowser` befüllt ist → `onOpenWindow` bailte → kein PageTarget.
   - `TargetRegistry.js` **Actor-Race**: `_browserIdToActor`/`onActorCreated`/
     `onActorDestroyed` + PageTarget-Konsum + `setActor`-Naming (FF152: Content-
     Actor entsteht vor `TabOpen`); `JugglerFrameParent` delegiert jetzt.
   - `FrameTree.onWindowEvent` + `PageAgent` (wholesale von Upstream, 0 Camou):
     **`ownerGlobal` ist auf FF152 null** bei `DOMDocElementInserted`/`load` →
     Fallback `ownerGlobal || defaultView`; dazu FF152 `synthesizeTouchEvent`
     (altes `windowUtils.sendTouchEvent` entfernt). **Das** war der letzte
     Blocker: ohne den Fallback feuerte `NavigationCommitted`/`pageready` nie →
     `Page.ready` erreichte den Client nie → `new_page`/`goto` hingen.
   - `documentGlobal || ownerGlobal` an activateAndRun + 2× Screencast +
     `PageHandler.topChromeWindow` (FF152 `ownerGlobal`-Entfernung).

   Die [TUNED]-Camou-Grafts (God-mode-Master-Sandbox in FrameTree, humanize/
   Maus-Trajektorie in PageHandler, Config-Reads) sind dabei **erhalten**
   geblieben (3-Wege-Merge, nicht Wholesale-Swap wo Camou drin war).
2. **Voice-Spoofing leakte die Host-Voices** — eine Windows-Maschine exponierte
   `„Microsoft Hedda - German (Germany)"` über `speechSynthesis.getVoices()`,
   was eine gespoofte macOS/en-US-Identität sofort verrät. Ursache: die
   pythonlib setzte `voices:blockIfNotDefined` nicht → `nsSynthVoiceRegistry`
   registrierte die echten Plattform-Voices zusätzlich. **Fix:** identity.py
   setzt jetzt `voices:blockIfNotDefined=true` (verifiziert: Host-Voices → 0).

### ✅ NEU gefunden (2026-07-22, via Proxy+Turnstile-Test) — GEFIXT (2026-07-22)
0. **Timezone-Spoof leakte die ECHTE Zeitzone im Playwright/Juggler-Pfad.**
   **GEFIXT (belt+suspenders, beide vom User bestätigt):** (a) **#657-Root-Cause**
   in `timezone-spoofing.patch` übernommen (DateTimeInfo-Override-Ctor seedt jetzt
   `utcToLocalStandardOffsetSeconds_ = SecondsPerDay; resetState()` — greift beim
   nächsten Build); (b) **pythonlib-Workaround** (sofort, ohne Rebuild lokal
   verifiziert **6/6 Asia/Seoul**, vorher 8/8 Berlin): `sync_api`/`async_api`
   reichen die Config-`timezone` als Playwright-`timezone_id` an den Kontext durch
   (`_tzhelper.config_timezone` + `_inject_context_timezone` wrappt `new_page`/
   `new_context`; persistent_context bekommt `timezone_id` direkt). Nutzt den
   zuverlässigen Juggler-Kontext-TZ-Pfad. Original-Beschreibung unten. ⚠️ Der
   `TZ`-Env-Weg wurde verworfen (Windows ignoriert POSIX-`TZ`).
   Mit `Camoufox(proxy=…, geoip=True)` + südkoreanischem Proxy erzeugt die
   pythonlib **deterministisch** die korrekte Config (`timezone=Asia/Seoul`,
   `locale=ko/KR`, `webrtc:ipv4`=Proxy-IP — 4/4 verifiziert). **Alle** anderen
   Spoofs greifen im Playwright-Launch zuverlässig und variieren pro Identität
   (WebGL Apple M1/NVIDIA/Intel, Screen, platform MacIntel/Win32, canvas,
   `navigator.language=ko-KR`, WebRTC leakt die echte IP **nicht** mehr → Item 5
   mit Proxy **gelöst**). **Nur `Intl.DateTimeFormat().resolvedOptions().timeZone`
   leakt `Europe/Berlin` (echte Maschinen-TZ, offset −120) statt Asia/Seoul —
   8/8 auf der externen Seite reproduziert.** Netto-Fingerprint: koreanische IP +
   koreanische Sprache + **deutsche Zeitzone** = sofortiger Kohärenz-Tell genau
   auf externen Seiten. **Isoliert:** im *rohen* Launch (kein Juggler, Config per
   `CAMOU_CONFIG_FILE` direkt) greift die TZ korrekt (`Asia/Seoul`, −540, „한국
   표준시"). Also **kein** kaputter TZ-Patch und **kein** Config-Read-Ausfall
   (WebGL etc. lesen MaskConfig ja), sondern eine **Playwright/Juggler↔MaskConfig-
   TZ-Interaktion**: die pythonlib reicht die TZ **nicht** an den Playwright-
   Kontext (`timezone_id`) durch, und der MaskConfig-TZ-Override greift über den
   Juggler-Page-Erstellungspfad (`ww.openWindow`→neues Fenster/Content-Prozess)
   nicht rechtzeitig. **Fix-Richtung:** entweder `launch_options` setzt zusätzlich
   die Playwright-Kontext-`timezone_id` aus der Config, oder der TZ-Override wird
   im Juggler-Pfad vor dem ersten JS erzwungen (analog `hasFailedToOverrideTimezone`).
   **Hohe Priorität** — betrifft den Haupt-Nutzungsweg (pythonlib/Playwright).

### 🟡 Upstream-Vergleich (2026-07-22) — Anti-Detect-Patches sind ein ALTER Snapshot
Wie schon der Juggler ist auch der **Anti-Detect-Patch-Satz des Forks älter als
Upstream `v152.0.4-beta.27`** und fehlt Fixes. Basename-Diff (nach FF152-Rebase,
also inkl. Kontext-Rauschen): webrtc-ip 598, screen 344, anti-font 267, webgl 110,
navigator 92, audio 55, **timezone 51**. **Empirisch verifiziert (nicht jeder Drift
ist eine echte Lücke):**

- 🔴 **Timezone (#657):** Upstreams `timezone-spoofing.patch` hat in
  `js/src/vm/DateTime.cpp` einen Fix, den wir NICHT haben: *"Without this the
  RangeCache members are read uninitialized and getTimezoneOffset() intermittently
  returns 0 or garbage. (issue #657)"* → `utcToLocalStandardOffsetSeconds_ =
  SecondsPerDay; resetState();` im DateTimeInfo-Override-Ctor. **Das ist die
  Wurzel des oben (Item 0) empirisch gefundenen intermittierenden TZ-Leaks.**
- 🟡 **Self-disabling WebIDL-Setter:** Upstream exponiert `window.setTimezone()/
  setWebGLVendor()/setNavigatorPlatform()/setAudioFingerprintSeed()/…` **`[Func=
  IsFunctionEnabledForWebIDL]`-gated** → sichtbar nur bis zum ersten Aufruf, dann
  weg. Unser Fork hat sie per **Option B** (2026-07-03) ganz entfernt (permanent-
  exponiert = Tell). Upstreams Variante = Stealth UND zuverlässige per-Realm-
  Anwendung; unsere MaskConfig-only-Lösung racet (→ TZ-Leak). **Neubewertung von
  Option B nötig** — evtl. war das Wegnehmen zu aggressiv.
- ✅ **CSS `device-width` (screen-spoofing):** Upstream ergänzt RFP-CSSDeviceSize-
  Spoofing — aber **empirisch folgt unser `@media (device-width)` dem gespooften
  `screen.width` (5/5 seeds, 2560→2560, 1920→1920)** → bei uns **kein** Leak
  (anders gelöst). Patch-Diff war hier ein False-Positive.
- ⚪ **WebRTC fabricated-candidate-priorities/getStats:** relevant nur bei SOCKS5-
  Spoof-IP; bei HTTP-Proxy fällt STUN aus (kein Leak). Kein bestätigter Vuln.

**Lektion (wie Juggler):** Anti-Detect-Patches gegen den passenden Upstream-Tag
re-syncen — aber **jeden Drift empirisch prüfen** (CSS-device-size zeigt: nicht
alles ist eine echte Lücke). Prio: das **#657-TZ-Fix** übernehmen.

### 🟠 Offen / beobachten (kein Quick-Fix)
3. **prefers-color-scheme fest auf DARK** — `prefersDark=true` bei ALLEN
   Identitäten (juggler `TargetRegistry.updateColorSchemeOverride = colorScheme ||
   'dark'`; Upstream: `|| browserContext.colorScheme || 'none'`). 100% Dark über
   alle Sessions = statistischer Tell + nicht identitäts-kohärent. **Fix:** auf
   `'none'` (Upstream) angleichen oder identitäts-gekoppelt randomisieren.
4. **Voice-Registrierung** — mit `blockIfNotDefined` verschwinden die Host-
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
| — | Juggler-Automation (5 FF152-Fixes, s. §2.1) | ✅ gefixt (lokal am Binary verifiziert) |
| — | Voice Host-Leak (`blockIfNotDefined`) | ✅ gefixt |
| — | WebRTC-IP mit Proxy+geoip (echte IP weg) | ✅ verifiziert (Item 5, mit Proxy) |
| — | Timezone-Leak (§2 Item 0) | ✅ gefixt (#657-Patch + pythonlib, 6/6 verifiziert) |
| — | prefers-color-scheme forced-dark (§2 Item 3) | ✅ gefixt (juggler → `'none'`) |
| — | UA-Skew rv:150→152 | ✅ gefixt (`ff_version` aus binary `application.ini`, UA=152 verifiziert) |
| — | Neuere Vektoren (WebGPU-strings/Battery/Connection/Client-Hints/USB/HID/Serial) | ✅ auditiert, sauber (Firefox maskiert/absent) |
| 1 | WebGPU adapter **limits/features** (headful, echte GPU) spoofen | 🔴 NEU offen — über Upstream hinaus, Wurzel-Härtung |
| 1 | Voice-Registrierung (0 Voices) post-Rebuild klären | offen |
| 2 | Invarianten-Smoke-Test in CI (§2-Harness) | offen, hoher Wert |
| 3 | UA-Skew 150→152 (Fingerprint-DB) | offen |
| 4 | Anti-Detect-Patches gg. Upstream re-syncen (empirisch) | offen, mittel |
| 5 | Option-B-Setter-Entfernung neu bewerten | offen |
| 6 | WebRTC default-block ohne Proxy | offen, optional |
| 5 | Stock-FF152-Baseline + probes.html WebRTC/Font | offen, braucht Workstation |
| 6 | P2.1 Rest-Pins auditieren | offen, niedrig |

**Nicht umfasst (bewusst):** Runtime-Detection-Scores (CreepJS/DataDome) als
ehrlicher Endbeweis — Sprung 3, braucht externe Dienste.
