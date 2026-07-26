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

## 1.6 — Anti-Detect-Audit 2026-07-26 (11 reale Bugs, am build-0.14-Binary)

Systematisches Audit aller Vektoren, die Meta/Google 2026 abfragen. Anlass:
frische Profile werden beim Facebook-Login mit generischem Fehler geblockt.
**Alle Änderungen sind uncommitted** (Branch `windows-msvc-migration`).

### Gefunden und behoben

| # | Befund | Verifikation |
| - | ------ | ------------ |
| 1 | **`fingerprint_seed` steuerte UA/OS nicht.** Browserforges Ziehung (wählt UA ⇒ Betriebssystem), `handle_screenXY` und der GeoIP-Locale-Pick liefen auf globalem `random`/`numpy`. Dasselbe **persistente Profil** war Lauf 1–2 macOS, Lauf 3 Linux — bei gleichen Cookies. Genau das Device-Change-Signal, das Meta als übernommene Session wertet. Fix: `_seeded_identity_rng()` in `utils.py`, domain-separiert je Aufrufstelle, Zustand wird restauriert. | live: 4× gleicher Seed identisch, persistentes Profil 3× stabil |
| 2 | **`toDataURL()`/`toBlob()` hatten kein Canvas-Noise** — der Patch hing nur an `getImageData`. Uniforme Fläche: Readback 390/4096 Pixel verrauscht, `toDataURL` **1 Farbe**. Damit war (a) der Wert, den Fingerprinter hashen, der **echte Host-Hash** (auf allen Profilen der Maschine gleich) und (b) die Differenz beider APIs ein Camoufox-Detektor ohne Fehlalarm. Fix: zweiter Hunk in `GetImageBuffer`. | `additions/camoucfg/CanvasNoise_test.cpp` 8/8 — u. a. „Encode- und Readback-Pfad byte-identisch trotz verschiedener Strides". **Wirkt erst nach Rebuild.** |
| 3 | **Screen-Tabellen mischten CSS- und Panel-Auflösung.** `screen.width` ist CSS-Pixel, `CSS × dpr` ist das implizierte Panel. macOS listete `2560×1600@2` ⇒ 5120×3200 (3 von 10 Einträgen unmöglich); Windows `1536×864@1.0` (das ist 1080p@125 %, dpr müsste 1.25 sein) und `3840×2160@1.5` ⇒ 5760×3240. | alle 50 Einträge bestehen `_panel_exists`, Negativkontrolle weist die 3 historischen Fehler zurück |
| 4 | **`X11; Ubuntu; Linux x86_64` crashte den Launch** (~1/40). `ua_parser` meldet die Distribution, nicht „Linux"; mit gepinntem Seed war das Profil dauerhaft unbrauchbar. | 60/60 Launches sauber |
| 5 | **Software-Renderer im Zufalls-Pool** (SwiftShader, llvmpipe, Microsoft Basic Render, ~2 %) — bedeutet „VM/Container", die Population mit dem höchsten Risiko-Score. Explizite Anforderung bleibt möglich. | 0 von 900 Stichproben |
| 6 | **TLS-Profil fiel auf ein Firefox-135-Capture zurück** — 152 fehlte in `SUPPORTED_FIREFOX_VERSIONS`, der Fallback war ausgerechnet das einzige Profil mit aktiven NSS-Overrides. Meldete `major_version:135` bei UA 152. Neu: `get_firefox_profile_for_version()` baut für unregistrierte Versionen ein natives Profil (degradiert ab FF153 sauber). | JA3/JA4/Akamai **byte-identisch** vor/nach ⇒ Overrides waren wirkungslos, Wire-FP ist echtes FF152 |
| 7 | **`humanize=True` warf eine Exception** (`isinstance(True, int)` ⇒ Bool in `humanize:maxTime`). Die komplette Verhaltensschicht war über ihre dokumentierte API unbenutzbar. Zusätzlich `humanize_disabled`-LeakWarning. | live, 11 Tasten: **aus 58 ms / 2 mousemove — an 1505 ms / 127** |
| 8 | **GeoIP-Locale zog `nds-DE`/`bar-DE`** (11,25 % der deutschen Identitäten) aus der vollen CLDR-Liste — Sprachen ohne Firefox-Build, also ein `navigator.language`, den echtes Firefox nie sendet. Fix: `FIREFOX_UI_LANGUAGES` aus `browser/locales/shipped-locales`; `sco`/`szl`/`oc`/`hsb` bleiben (haben echte Builds). | 0 Fehlzüge in 3.900 Ziehungen, 13 Länder |
| 9 | **`Accept-Language` fehlte Firefox' `en-US, en`-Anhang.** `locale_service_default_accept_languages` hängt ihn bei jeder Locale außer `en, lt, my, ro, sco, sl, szl` an; echtes FF-DE sendet `de,en-US;q=0.9,en;q=0.8`, Camoufox sendete `de-DE,de;q=0.9` — bei **jeder** nicht-englischen Identität, auf **jeder** Anfrage. | live via `omni.ja`-Patch: vorher `de-DE,de;q=0.9`, nachher `de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7`. **Wirkt erst nach Rebuild.** |
| 10 | **`en-DE`/`en-PL`/`en-FR`** — Firefox behält bei `en` nur CA/GB/ZA, alles andere wird `en-US`. Traf ~1/3 der Identitäten in nicht-englischen Ländern. | 0 unmögliche Tags in 3.000 Ziehungen, 12 Länder |
| 11 | **Die Population clusterte.** 150 unabhängig geseedete Profile ⇒ nur 13 Screen-Configs / 39 Profile, **ein Profil = 17 %**, Top-5 = 53 % — „viele Accounts, wenige Geräte". Tabellen als reale Panel×Skalierung-Paare neu gebaut (50 Einträge). | danach 17 Configs / 44 Profile / Top-5 45 %, 0 Launch-Fehler |

### Als Fehlalarm verworfen (nicht erneut aufrollen)

- `", or similar"` bei WebGL-Renderern = **echtes Firefox** (`dom/canvas/SanitizeRenderer.cpp:366`).
- `Accept-Language ... q=0.9` = **echtes Firefox**. `netwerk/base/rust-helper/src/lib.rs` wörtlich: *„Since we need to emulate chrome behavior i.e languages should get q=1.0,0.9,0.8"*. Die `q=0.5`-Annahme ist veraltet.
- `voices == 0` = Messfehler; `getVoices()` füllt asynchron, mit Polling 53–131 Stimmen.
- WebGPU `NO_ADAPTER` = Firefox' eigene gfxInfo-Blocklist, kohärent.
- `permissions.query(notifications)='prompt'` vs `Notification.permission='default'` = dieselbe Schreibweise desselben Zustands.
- `document.fonts.check()` liefert für **jeden** Namen `true` — als Font-Probe wertlos; nur Metrik-Messung zählt.
- `hardwareConcurrency`/`mediaDevices` korrekt gespooft (Config 24 Kerne ≠ Host 16).
- WebRTC-IPv6 leakt mit Proxy nicht (`getMaskForIP` → `::`).
- Die 17 %-Restkollision ist **kein Bug**: `Apple M1, or similar` hat 0,819 Mac-Gewicht in `webgl_data.db`, echte Macs konzentrieren sich so. Weiter glätten tauscht Realismus gegen einen anderen Tell.

### ⚠️ Falschbelege in der eigenen Test-Infrastruktur

- **`cf_turnstile_test.py` beweist nichts.** Es nutzt `demo.turnstile.workers.dev`
  mit Sitekey `1x00000000000000000000AA` — Cloudflares *always-passes*-Testkey.
  Der gibt **jedem** Client `XXXX.DUMMY.TOKEN.XXXX`, das Skript meldet dadurch
  immer `solved: True`. Frühere „Turnstile bestanden"-Schlüsse sind haltlos.
- Pixelscans `/s/api/co` liefert **pro Aufruf andere Payloads**. Ein
  `osFontsStatus:false` aus einer Einzelstichprobe wurde durch den
  Cross-OS-Gegentest widerlegt. „Masking detected" bleibt **unzugeordnet**.

### Externe Verdikte nach den Fixes

CreepJS `0 % headless`, `0 % stealth`, `chromium: false`, Worker-Realm
`confidence: high`. Pixelscan **„No automated behavior detected"**.
facebook/instagram/google/youtube: alle HTTP 200 mit funktionierendem
Login-Formular, kein Block-Text, keine sichtbare Challenge.

### Offen

1. **Endabnahme:** `login_acceptance.py` (persistentes Profil + `humanize=True`
   + `geoip=True` + Warm-up-Browsing, dann echter Login mit Protokoll der
   Plattform-Reaktion; Credentials nur via ENV). Braucht Proxy-Zugangsdaten und
   Testaccount. Denselben Profilordner mit Datacenter- **und** Residential-Exit
   laufen lassen — nur das trennt „Browser erkannt" von „IP verbrannt".
2. **Pixelscan „Masking detected"** — Attribution nicht gelungen.
3. **Linux-Font-Bundle**: `bundle/fonts/linux/` enthält nur Tor-Browser-Fonts
   (Arimo/Cousine/Tinos + Noto-Skripte), **kein** DejaVu/Liberation/Ubuntu/
   Cantarell. Bewusste Upstream-Entscheidung mit `DO NOT MODIFY`; eine reine
   Namensliste ohne die Dateien wäre wirkungslos. Gemeldet, nicht geändert.

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
