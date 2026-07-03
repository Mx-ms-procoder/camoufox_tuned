# Remediation Plan — Antwort auf Kritiker-Audit (2026-05-19)

> **Status 2026-05-19 (nach erstem Pass):** Schritte §1.1, §1.3, §1.4, §1.5, §1.7
> und §1.12 umgesetzt. Validator läuft grün (54/54 Patches). Der neue
> Hunk-Level-Konflikt-Checker exponiert **5 reale Patch-Konflikte** (siehe §6).
> §1.2 und §1.6–§1.10 stehen bewusst noch aus (Produktentscheidungen bzw.
> Folgeaufwand). §2 und §3 unverändert — verlangen Firefox-Source bzw. Build-Host.
>
> **Status 2026-05-21 (nach zweitem Pass):** Die 5 Hunk-Konflikte sind aufgelöst
> (speech-voices/screen/audio neu verankert; Hunk-Checker respektiert jetzt die
> `expected_overlaps.yaml`-Allowlist). Conflict-Checker ist grün (0 errors).
> §2.3 und §2.4 sind aus dem NSS-Source (Searchfox) **verifiziert** —
> `SSL_CipherPrefSetDefault` ist prozessglobal/enable-only, der
> widersprüchliche Kommentar in `CamouTLSOverride.hpp` wurde entfernt;
> Windows-`DebugEnabled` dort ebenfalls gefixt (vorher: `size == 2` matchte
> jeden 1-char-Wert). Außerdem umgesetzt: §1.6 (`requirements.lock` mit
> Hashes, CI nutzt `--require-hashes`), §1.9 (`k8s/README.md` mit
> Experimental-Status), §1.11 (build-Job hat jetzt `needs: test-python`).
>
> **Status 2026-05-21 (dritter Pass, §1.2 Security-Defaults):**
> Faktenbasiert verifiziert über DevTools-Source (Searchfox) und gefixt:

`devtools.debugger.remote-enabled` von `true`→`false` (Camoufox-Automation
>    nutzt Juggler, nicht den DevTools-Debugger; vorher band der Server auf
>    **0.0.0.0:6000 ohne Prompt** — verifiziert in
>    `devtools/shared/security/socket.js`, das nur bei
>    `devtools.debugger.force-local=true` auf 127.0.0.1 einschränkt).
>    `force-local=true` wird jetzt explizit gesetzt (Defense-in-Depth),
>    `prompt-connection` zurück auf Firefox-Default `true`.
>  * Safe Browsing bleibt aus, aber mit dokumentierter Begründung
>    (Detection-Surface gegenüber JS = 0, Privacy-Kosten für Scraping = real;
>    Opt-in via `firefox_user_prefs` möglich).
>  * `security.fileuri.strict_origin_policy` von `false`→`true`
>    (Firefox-Default; vorher Test-Harness-Inheritance ohne Anti-Detect-Nutzen).
>
> Regression bei §1.12-Patch-Fix entdeckt und gefixt: `speech-voices-spoofing.patch`
> `moz.build`-Hunk-Header (`-6,+14`→`-5,+13`) + leere Context-Blank-Zeile auf
> ` ` korrigiert. Validator (54/54) und Conflict-Check (0 errors) wieder grün.
>
> Noch offen ohne Source: §1.8 (Roverfox-Rename, großer Diff),
> §1.10 (Test-Basis ausbauen).


Dieses Dokument beantwortet drei Fragen:

1. **Was kann ich (Claude) hier im Repo direkt verbessern?** — Arbeiten, die ohne Firefox-Source und ohne Build-Toolchain durchführbar sind.
2. **Wofür brauche ich den Firefox-Quellcode?** — Arbeiten, die nur am gecheckten Mozilla-Source verifiziert oder geändert werden können.
3. **Was braucht ein vollständiger Build?** — Was nötig ist, um aus dem Patchset einen lauffähigen Camoufox zu erzeugen.

Die Punkte sind sortiert nach Priorität gemäß Audit (Kritisch → Hoch → Mittel).

---

## 1. Was ich direkt im Repo verbessern kann (kein Firefox-Source nötig)

Diese Punkte sind reine Repo-Änderungen — Patch-Header, Python-Scripts, Konfig-Defaults, CI, Doku. Kein `mozilla-unified` Checkout erforderlich.

### 1.1 [KRITISCH] `anti-font-fingerprinting.patch` Header reparieren
- **Datei:** [patches/identity/anti-font-fingerprinting.patch](patches/identity/anti-font-fingerprinting.patch)
- **Befund:** Zweiter Hunk-Header lautet `@@ -1557,6 +1560,36 @@`. Tatsächlich enthält der Hunk 6 Kontextzeilen + 34 hinzugefügte Zeilen = **40** neue Zeilen, nicht 36.
- **Fix:** Header auf `@@ -1557,6 +1560,40 @@` ändern.
- **Verifikation lokal möglich:** `python3 scripts/validate_patches.py` muss durchlaufen.
- **Risiko:** Niedrig. Reine Buchhaltungs-Korrektur.

### 1.2 [HOCH] Sicherheits-Defaults in `settings/camoufox.cfg` überprüfen
- **Befund vom Kritiker:**
  - line 9: Remote Debugger an
  - line 637: Safe Browsing aus
  - line 747: `security.fileuri.strict_origin_policy=false`
- **Was ich tun kann ohne Source:**
  - Diese drei Prefs entweder per Default auf sichere Werte setzen, oder dokumentieren, *warum* sie für Automation/Stealth nötig sind, und ein Opt-in-Schalter über `MaskConfig`-Schlüssel einbauen.
  - Konkret vorschlagen:
    - `devtools.debugger.remote-enabled` nur enable wenn `CAMOU_ALLOW_DEBUGGER=1` (oder Pref über `MaskConfig`).
    - Safe Browsing optional re-enable als Default — Stealth-Mode bleibt opt-out.
    - `strict_origin_policy` Default zurück auf `true`, file://-Tests müssen es selbst opt-out setzen.
- **Risiko:** Verhaltensänderung. Vor dem Patch sollte der Maintainer entscheiden, ob die Defaults wirklich gelockert sein sollen.

### 1.3 [HOCH] Patch-Reihenfolge nicht mehr alphabetisch sortieren
- **Datei:** [scripts/_mixin.py:335](scripts/_mixin.py#L335)
- **Befund:** `return sorted(claimed_paths, key=os.path.basename)` ignoriert die Reihenfolge aus den Manifesten.
- **Fix:** Reihenfolge aus Manifest beibehalten (Manifest-Lese-Reihenfolge ist die Quelle der Wahrheit). Dafür `list_patches` so umbauen, dass `claimed_paths` als geordnete Liste aufgebaut wird (z.B. `dict.fromkeys()` zum Dedupe unter Erhalt der Insertion-Order, statt am Ende `sorted`).
- **Verifikation:** Nach dem Fix `validate_patches.py` weiter grün, und `patch.py --check-conflicts --strict` weiter ohne neue Fehler.
- **Risiko:** Mittel. Patch-Apply-Reihenfolge ändert sich. Lokal-Test mit `--check-only` empfehlenswert; echter Stresstest braucht aber den Firefox-Source (siehe §2.1).

### 1.4 [HOCH] Debug-Flag-Auswertung unter Windows
- **Datei:** [additions/camoucfg/MaskConfig.hpp:36](additions/camoucfg/MaskConfig.hpp#L36)
- **Befund:** Unter Windows prüft der Code nur Stringlänge, nicht den Inhalt. `CAMOU_MASKCFG_DEBUG=0` aktiviert daher Debug.
- **Fix:** Wert parsen, gängiges Truthy-Schema (`"1"`, `"true"`, `"yes"` truthy; alles andere falsy). Reine C++-Header-Änderung; verifizierbar mit einem kleinen Unit-Test in `tests/`.
- **Risiko:** Niedrig. Verhaltensänderung nur für `CAMOU_MASKCFG_DEBUG`.

### 1.5 [HOCH] Destruktives `make revert`
- **Datei:** [Makefile:96-97](Makefile#L96-L97)
- **Befund:** `git reset --hard unpatched` löscht uncommittete Änderungen wortlos.
- **Fix:** Vor `--hard` einen `git stash push -u -m "pre-revert"` oder mindestens eine Bestätigungsfrage (`@read -p`) einbauen. Alternativ: zweistufiges Target — `revert` zeigt Diff an, `revert-force` macht den Reset.
- **Risiko:** Niedrig.

### 1.6 [MITTEL] `requirements.txt` mit Hashes pinnen
- **Datei:** `requirements.txt`
- **Fix:** `pip-compile --generate-hashes` benutzen und als `requirements.lock` einchecken. CI installiert dann mit `pip install --require-hashes -r requirements.lock`.
- **Risiko:** Niedrig. Reproduzierbare Installs.

### 1.7 [MITTEL] `shell=True` in `_mixin.py:590` ersetzen
- **Datei:** [scripts/_mixin.py:590](scripts/_mixin.py#L590)
- **Fix:** Argumentliste statt String, `shell=False`. Falls Glob-Expansion gebraucht wird, im Python expandieren.
- **Risiko:** Niedrig. Injection-Vektor entschärfen.

### 1.8 [MITTEL] Legacy-Name `Roverfox`
- **Befund:** `RoverfoxStorageManager` u.ä. Namen sind Altlasten und stiften Verwirrung.
- **Fix:** Suchen/Ersetzen über das Repo. Reine kosmetische Refactorierung; keine Auswirkung auf Patches gegen Firefox.
- **Risiko:** Niedrig, aber großer Diff.

### 1.9 [MITTEL] `cloud_native.py` Stub-Status dokumentieren
- **Datei:** [pythonlib/.../cloud_native.py](pythonlib/) (Pfad verifizieren)
- **Fix:** Im README/k8s-Doku klar als "experimental / pool ist noch kein echter Worker-Pool" markieren und Roadmap-Item dafür anlegen, statt dass das Audit es als versteckten Mangel findet.

### 1.10 [MITTEL] Test-Basis ausbauen
- **Befund:** Nur drei Python-Testdateien, keine C++-Runtime-Tests.
- **Was ohne Source möglich ist:**
  - Python-Tests für `_mixin.py` (Patch-Listing, Manifest-Parsing, Konflikt-Checker).
  - Python-Tests für `tls_profiles.py` (parity-baseline-Logik, Mapping firefox150 → ClientHello).
  - Tests für `MaskConfig`-Truthy-Parsing als Header-only Unit-Test (mit CMake- oder einfachem `g++ -DTEST`-Setup).
- **Was nicht ohne Source möglich:** Echte C++-Runtime-Tests in Firefox-Kontext (Gecko mochitests, xpcshell) — siehe §2.

### 1.11 [HOCH] CI-Job, der wirklich baut
- **Datei:** `.github/workflows/build.yml`
- **Aktueller Stand laut Audit:** Job läuft nur bis `validate_patches.py` und fällt dort.
- **Was ich tun kann ohne Source:**
  - Validator grün machen (§1.1).
  - CI um einen *dry-run* Step ergänzen: `python3 scripts/patch.py --check-only` o.ä., der nur prüft, ob alle Patches sauber gegen einen frischen Firefox-Source applizieren würden — *unter der Voraussetzung*, dass der Source erst gecheckt out wird. Source-Checkout selbst gehört zum Build-Job, nicht zum Validator.

### 1.12 [HOCH] Konflikt-Checker härten
- **Datei:** [scripts/patch.py](scripts/patch.py) (`--check-conflicts --strict`)
- **Befund:** Der Checker arbeitet nur cross-manifest und meldet semantisch kollidierende Patches nicht.
- **Was ich tun kann ohne Source:**
  - Pro Patch die geänderten Dateien + Hunk-Bereiche (Zeilenbereiche) extrahieren und auf Überlappung prüfen — *innerhalb* eines Manifests und *über* Manifeste hinweg. Pure Patch-Header-Auswertung, kein Source nötig.
  - Überlappung auf `dom/base/Navigator.cpp`, `nsGlobalWindowInner.cpp`, `Window.webidl`, `moz.build` als WARN/ERROR ausgeben statt zu ignorieren.
- **Risiko:** Mittel. Es wird Falschpositive geben (zwei Patches gleiche Datei, aber disjunkte Stellen — das ist okay). Daher initial als WARN, nicht ERROR.

---

## 2. Wofür ich Firefox-Quellcode brauche

Diese Punkte verlangen einen Checkout von `mozilla-unified` an der Camoufox-Zielversion (laut Repo Firefox 150-Klasse — exakte Revision steht in den Mozconfigs/Manifests). Ohne den Source kann ich Diagnose und Fixes nur "blind" auf Header-Ebene machen.

### 2.1 [KRITISCH] Patch-Anwendbarkeit wirklich verifizieren
- **Was Audit nicht prüft:** Selbst nach §1.1 sagt der Validator nur, dass *die Patch-Datei syntaktisch ein gültiges Diff ist*. Ob die Hunks *im echten Firefox-Source* noch passen, ist offen.
- **Mit Source möglich:** `git apply --check patches/**/*.patch` gegen die Ziel-Firefox-Revision. Das ist der eigentliche "kann ich bauen?"-Test.
- **Erwartung:** Bei mehreren Hundert Patches gegen ein moving target (Firefox 150) werden einige fuzz-Anpassungen fällig.

### 2.2 [KRITISCH] Überlappende Patches an Hotspots de-duplizieren
- **Hotspots laut Audit:** `dom/base/Navigator.cpp`, `nsGlobalWindowInner.cpp`, `Window.webidl`, `moz.build`.
- **Mit Source möglich:** Pro Datei den finalen Stand nach Anwendung aller Patches inspizieren. Dann entscheiden, ob `IdentityStateProvider`, `NavigatorManager`, `ScreenDimensionManager`, `RoverfoxStorageManager` semantisch kollidieren oder nur denselben File touchieren.
- **Mögliche Konsolidierung:** Eine einheitliche `CamouIdentityHooks.cpp`/`.h`-Schicht, an die alle vier Provider andocken, statt vier paralleler Hook-Sets.

### 2.3 [HOCH] TLS-/HTTP-2-Parität zu Firefox 150
- **Befund:** [tls_profiles.py:197](tls_profiles.py#L197) setzt Nicht-135 auf `parity_baseline=135`; HTTP/2 default aus ([tls_profiles.py:322](tls_profiles.py#L322)); uTLS-Sidecar mappt `firefox150 → HelloFirefox_120` ([utls_proxy.go:295](utls_proxy.go#L295)).
- **Verifiziert 2026-05-21 (Searchfox, NSS-Source mozilla-central):**
  - Die ClientHello-Cipher-Reihenfolge wird **nicht** durch `SSL_CipherPrefSetDefault` kontrolliert.
    Sie ist fest kodiert in `security/nss/lib/ssl/ssl3con.c:cipherSuites[]` (statisches Array vom Typ `ssl3CipherSuiteCfg`). NSS emittiert Suiten in Array-Reihenfolge, gefiltert auf `enabled=PR_TRUE`.
  - **Default-enabled (PR_TRUE) in Firefox/NSS** (in Wire-Reihenfolge):
    TLS-1.3: `TLS_AES_128_GCM_SHA256`, `TLS_CHACHA20_POLY1305_SHA256`, `TLS_AES_256_GCM_SHA384`;
    ECDHE: ECDSA/RSA AES-128-GCM, ECDSA/RSA ChaCha20, ECDSA/RSA AES-256-GCM, dann ECDSA/RSA AES-256-CBC, AES-128-CBC, RSA-AES-128-CBC-SHA256;
    DHE-RSA: AES-128-GCM, ChaCha20, AES-256-GCM, AES-128-CBC, AES-128-CBC-SHA256, AES-256-CBC, AES-256-CBC-SHA256, 3DES;
    DHE-DSS: AES-128-CBC, AES-256-CBC (weitere DHE-DSS mit PR_FALSE);
    RSA: AES-128-GCM, AES-256-GCM, AES-128-CBC, AES-128-CBC-SHA256, AES-256-CBC, AES-256-CBC-SHA256, 3DES, RC4-SHA, RC4-MD5.
  - **Default-disabled (PR_FALSE):** ECDHE-{ECDSA,RSA}-AES-{256,128}-CBC-SHA{256,384}, 3DES ECDHE/ECDH-Varianten, RC4, DES, null, alle ECDH (non-ephemeral), Camellia, SEED, DHE-DSS-GCM, DHE-DSS-SHA256-CBC, DHE-DSS-RC4.
  - Firefox-Ebene (`security/manager/ssl/nsNSSComponent.cpp`) filtert diese weiter über `sCipherPrefs[]` → `StaticPrefs::security_ssl3_*`. Das sind 19 steuerbare Suiten + 1 deprecated (3DES, off by default). **Die 20 Prefs sind das produktiv relevante Subset.**
  - HTTP/2 SETTINGS und GREASE-Positionen: bleiben ohne echten HTTP-Trace oder Source-Check von `netwerk/protocol/http/Http2*` unverifikziert — die uTLS `HelloFirefox_120`-Approximation ist weiterhin falsch für 150.
- **Noch ausstehend:** Manueller uTLS-Fingerprint für Firefox 150; HTTP/2 SETTINGS via Wireshark-Trace oder Source-Lektüre.

### 2.4 [HOCH] `SSL_CipherPrefSetDefault` Scope — **VERIFIZIERT 2026-05-21**
- **Datei:** [additions/camoucfg/CamouTLSOverride.hpp](additions/camoucfg/CamouTLSOverride.hpp)
- **Befund aus NSS-Source (mozilla-central, Searchfox):**
  - `SSL_CipherPrefSetDefault(cipher, enabled)` schreibt in die **prozessglobale** statische `cipherSuites[]`-Tabelle in `ssl3con.c`. Sie gilt für alle Sockets, die **nach** dem Aufruf erstellt werden; bestehende Sockets sind nicht betroffen.
  - `SSL_CipherPrefSet(fd, cipher, enabled)` schreibt in `ss->cipherSuites` (per-Socket-Kopie) — nur diesen einen Socket.
  - `SSL_CipherPrefSetDefault` steuert **ausschließlich** enable/disable — **nicht** die ClientHello-Reihenfolge. Die Reihenfolge folgt der festen Array-Reihenfolge in `cipherSuites[]` (bestätigt durch Mozilla bug 1267894 und Einführung von `SSL_CipherSuiteOrderSet` in NSS 3.47).
  - `CamouTLSOverride::ApplyAll()` wird in `nsNSSComponent::InitializeNSS()` **vor** `CommonInit()` aufgerufen — korrekt, da zu diesem Zeitpunkt noch keine Sockets existieren.
  - Widersprüchlicher Kommentar in Phase-2 von `ApplyCipherOverride()` ("enable-order becomes wire-order") wurde in diesem Pass entfernt.
- **Konsequenz:** Die aktuelle Implementierung ist korrekt für ihr Ziel (enabled-Set narrowen). Für echte Order-Kontrolle wäre `SSL_CipherSuiteOrderSet` (NSS ≥ 3.47, per Socket) oder ein NSS-interner Patch erforderlich — in der Firefox-Familie nicht nötig, da NSS-Default-Order bereits korrekt ist.

### 2.5 [HOCH] `validate_patches.py` als echte Apply-Probe
- **Mit Source möglich:** Den Validator erweitern, sodass er nicht nur Diff-Headers parst, sondern in einem Tempdir-Checkout `git apply --check` macht. Das fängt Class 1.1 (kaputte Header) *und* Class 2.1 (Hunk-Offsets gewandert) ab.

### 2.6 [HOCH] C++-Runtime-Tests
- **Mit Source möglich:** xpcshell-/mochitest-Cases, die `navigator.*`, `screen.*`, WebGL-Vendor, AudioContext-Sample-Hashes etc. prüfen und gegen Camoufox-Erwartungen asserten. Ohne diese ist "es buildet" nicht gleich "es maskt korrekt".

### 2.7 [MITTEL] `MOZ_LTO_RUST_CROSS` / Windows-Build-Pfad
- **Memory aus Vorkonversation** (siehe `MEMORY.md → project_windows_build_fix.md`): Stage 5 (2026-05-15) versucht blind `--disable-lto` in `windows.mozconfig`. Das ist nur mit Source und einer Build-Box belastbar zu klären.

---

## 3. Was ein vollständiger Build erfordert

Damit aus dem Patchset wirklich ein `camoufox.exe` / `camoufox` Binary entsteht. Diese Liste ist ein Reality-Check vor jedem ernsthaften Build-Versuch.

### 3.1 Quellen
- **Firefox-Source:** `mozilla-unified` Checkout auf der genauen Ziel-Revision. Camoufox pinnt typisch eine Firefox-ESR- oder Release-Revision; die steht in `upstream.sh` bzw. den Mozconfig-Targets.
- **Camoufox-Additions:** `additions/` (camoucfg, MaskConfig, evtl. CamouTLSOverride) muss vom Patch-Step in den Source-Tree kopiert werden — siehe `scripts/patch.py`.

### 3.2 Build-Host
- **OS:**
  - Linux (Ubuntu/Debian/Fedora/Arch) für Linux- und Cross-Builds.
  - macOS für macOS-Targets.
  - Windows-Builds erfordern entweder einen Windows-Host mit MSYS2 + Visual Studio 2022 (MSVC) oder einen Linux-Cross-Build mit clang-cl. Beide Wege sind in den Mozconfigs des Repos angedeutet.
- **CPU/RAM/Disk:** Praktisch ≥8 Cores, ≥16 GB RAM (32 GB empfohlen für LTO), ≥50 GB freier Plattenplatz allein für Object-Files.

### 3.3 Toolchain
- **Rust:** Mozilla pinnt Rust-Versionen pro Firefox-Release ("Firefox Source Docs → Rust update policy"). Falsche Rust-Version → Build bricht in `cargo` ab.
- **Clang/LLVM:** Mozilla pinnt ebenfalls; via `./mach bootstrap` ziehbar.
- **NodeJS:** Für Mochitest- und Build-Helper.
- **Python 3.x:** Mozbuild verlangt 3.8+.
- **Unix-Tools (auch unter Windows):** `aria2c`, `7z`, `bash`, `patch`, `make` — heute via MSYS2 oder WSL bereitgestellt; das Makefile-Wrapping ist Linux-zentriert.

### 3.4 Bootstrap-Schritte (idealer Ablauf)
1. `make setup` → klont Firefox-Source auf die im Repo gepinnte Revision.
2. `make mozbootstrap` → installiert via `./mach bootstrap` die Mozilla-Toolchains.
3. `make dir` → ruft `scripts/patch.py` und appliziert *alle* Patches in Manifest-Reihenfolge (vorher §1.3 fixen).
4. `make build` → `./mach build` mit `windows.mozconfig` / `linux.mozconfig` / `macos.mozconfig`.
5. `make package` → produziert das Distribution-Archiv.

### 3.5 Was zwischen "Build grün" und "Produktionsreif" liegt
- Build-Erfolg ≠ Stealth-Erfolg. Nach dem Build:
  - Headless-Run starten, `navigator.webdriver`, UA, Canvas-Hash, Audio-Hash, Screen-Metrics gegen Erwartungswerte aus `MaskConfig` validieren.
  - TLS-/HTTP-2-Fingerprint gegen JA3/JA4-Sammler (z. B. tls.peet.ws, browserleaks) prüfen, *vorher und nachher* einen Vanilla-Firefox-150 als Baseline messen.
  - CDP/Juggler-Hooks (Playwright-Anbindung) gegen die Playwright-Patches in `patches/playwright/` smoke-testen.

### 3.6 Was *nicht* belegt werden kann, egal wie sauber gebaut wird
- "CVE-Frei" — wäre nur durch fortlaufendes Tracking gegen Mozilla-Advisories möglich.
- Cloudflare-/DataDome-/PerimeterX-Bypassrate — datengetrieben, nicht code-getrieben; jede Behauptung ohne Messreihe ist Marketing.

---

## 4. Empfohlene Reihenfolge

| # | Schritt | Source nötig? | Aufwand |
|---|---|---|---|
| 1 | §1.1 Patch-Header fixen | Nein | Minuten |
| 2 | §1.11 CI bis "validator grün" | Nein | Stunden |
| 3 | §1.4 `MaskConfig`-Debug-Flag | Nein | Stunden |
| 4 | §1.5 Makefile-`revert` entschärfen | Nein | Minuten |
| 5 | §1.7 `shell=True` entfernen | Nein | Stunden |
| 6 | §1.6 `requirements.lock` mit Hashes | Nein | Stunden |
| 7 | §1.12 Konflikt-Checker auf Hunk-Ebene | Nein | Tag |
| 8 | §1.3 Patch-Reihenfolge aus Manifest | Nein (Logik) / Ja (Stresstest) | Tag |
| 9 | §1.2 Security-Defaults entscheiden | Nein | Diskussion |
| 10 | §2.1 / §2.5 Echter `git apply --check` | Ja | Tag |
| 11 | §2.2 Hotspot-Konsolidierung | Ja | Wochen |
| 12 | §2.3 / §2.4 TLS-Parität | Ja + Mess-Setup | Wochen |
| 13 | §2.6 C++-Runtime-Tests | Ja + Build | Wochen |

Schritte 1–9 kann ich starten, sobald du das Go-Zeichen gibst. Für Schritte 10+ muss zuerst der Firefox-Source unter `cf_source_dir` (oder einem benannten Pfad) verfügbar sein.

---

## 5. Was ich *nicht* tun werde, ohne dass du es bestätigst

- §1.2 Security-Defaults ändern — das ist eine Produktentscheidung, kein Bugfix.
- §1.8 `Roverfox`-Rename — großer Diff, könnte Patch-Pfade brechen, will ich nicht eigenmächtig ausrollen.
- Irgendetwas, das `git reset --hard`, `git push --force` oder Löschen von Branches/Files außerhalb des erwarteten Scope verlangt.

---

## 6. Umgesetzt am 2026-05-19 — Ergebnisse pro Punkt

### §1.1 Patch-Header repariert
- **Geändert:** [patches/identity/anti-font-fingerprinting.patch:15](patches/identity/anti-font-fingerprinting.patch#L15)
- **Vorher:** `@@ -1557,6 +1560,36 @@`
- **Nachher:** `@@ -1557,6 +1560,40 @@`
- **Verifikation:** `py -3 scripts/validate_patches.py` → `Validated 54 patch file(s).`
- **Quelle:** GNU diffutils manual — "the count represents the total span of lines in that file's section ... unchanged context lines plus added/removed lines on each side" ([Detailed Unified Format](http://www.gnu.org/s/diffutils/manual/html_node/Detailed-Unified.html)).

### §1.3 Manifest-Reihenfolge respektiert
- **Geändert:** [scripts/_mixin.py:335](scripts/_mixin.py#L335)
- **Vorher:** `return sorted(claimed_paths, key=os.path.basename)`
- **Nachher:** `return claimed_paths` (Insertion-Order aus den Manifesten bleibt erhalten; Manifeste werden cross-manifest alphabetisch nach Dateiname iteriert)
- **Verifikation:** Validator weiter grün.

### §1.4 `MaskConfig` Debug-Flag Truthy-Parsing
- **Geändert:** [additions/camoucfg/MaskConfig.hpp:36](additions/camoucfg/MaskConfig.hpp#L36)
- **Vorher:** Auf Windows reine Längenprüfung (`size == 2`), d. h. `CAMOU_MASKCFG_DEBUG=0` aktivierte Debug.
- **Nachher:** Neuer Helper `_IsTruthyEnv(name)`. Truthy = `"1"`, `"true"`, `"yes"`, `"on"` (case-insensitive). `"0"`, `"false"`, leer, unset → falsy. Plattform-gleiches Verhalten.
- **Quelle:** [Microsoft Docs zu `GetEnvironmentVariableW`](https://learn.microsoft.com/en-us/windows/win32/api/processenv/nf-processenv-getenvironmentvariablew) — "the return value is the buffer size, in characters, required to hold the string **and its terminating null character**", was den bisherigen `size == 2`-Check für jedes 1-Zeichen-Value true zurückgeben ließ.

### §1.5 Makefile `revert` entschärft
- **Geändert:** [Makefile:96-104](Makefile#L96-L104)
- **Vorher:** `cd $(cf_source_dir) && git reset --hard unpatched` — destruktiv ohne Warnung.
- **Nachher:** `revert` macht erst `git stash push -u -m "pre-revert-..."`, dann reset. Verlorenes Werk via `git stash list && git stash pop` zurückholbar. Neues Target `revert-force` für bewusstes Hard-Discard.

### §1.7 `shell=True` aus `run()` entfernt
- **Geändert:** [scripts/_mixin.py:575-598](scripts/_mixin.py#L575-L598) plus zwei Callers
  - [scripts/patch.py:147-150](scripts/patch.py#L147-L150) — `~/.cargo/bin/rustup ...` → `os.path.expanduser` + argv-Liste
  - [scripts/developer.py:386-400](scripts/developer.py#L386-L400) — `git diff > {file_path}` → `subprocess.run(['git', 'diff'], stdout=fh)`
- **Verhalten:** `run()` läuft jetzt ausschließlich `shell=False`. Strings werden via `shlex.split` tokenisiert. Shell-Metazeichen (`>`, `|`, `&`, `~`) sind dadurch keine Stille-Bypass-Vektoren mehr.

### §1.12 Konflikt-Checker auf Hunk-Ebene
- **Geändert:** [scripts/_mixin.py](scripts/_mixin.py) — `_extract_hunks()`, `_hunks_overlap()`, plus Erweiterung von `detect_conflicts()`.
- **Effekt:** Cross-Manifest-Patch-Paare auf derselben Datei werden zusätzlich auf überlappende `old_start..old_start+old_count-1` Bereiche geprüft. Überlappung → severity `error` mit konkreter Zeilenangabe.
- **Verifikation (am eigenen Patchset):**
  ```
  Patch Conflict Report: 5 errors, 3 warnings, 9 expected overlaps
    [ERROR] dom/base/nsGlobalWindowInner.cpp ... font-list-spoofing.patch @ 7477-7482 vs speech-voices-spoofing.patch @ 7477-7482
    [ERROR] dom/base/nsGlobalWindowInner.h   ... font-list-spoofing.patch @ 685-690 vs speech-voices-spoofing.patch @ 685-690
    [ERROR] dom/base/nsGlobalWindowInner.h   ... screen-spoofing.patch @ 677-682 vs audio-fingerprint-manager.patch @ 674-679
    [ERROR] dom/webidl/Window.webidl         ... font-list-spoofing.patch @ 892-897 vs speech-voices-spoofing.patch @ 892-897
    [ERROR] dom/webidl/Window.webidl         ... screen-spoofing.patch @ 929-934 vs audio-fingerprint-manager.patch @ 930-935
  ```
- **Bewertung:** Vorher meldete der Checker hier `0 errors`. Die 5 Funde sind *reale* Konflikte (identische Hunk-Anchor → zweite Anwendung wird `git apply` mit Fuzz/Reject quittieren). Genau das Risiko, vor dem der Audit warnte.

### CI-Workflow
- **Datei:** [.github/workflows/build.yml:36](.github/workflows/build.yml#L36) hatte bereits `validate_patches.py` und Zeile 39 `patch.py --check-conflicts --strict`. Kein zusätzlicher Step nötig.
- **Stand nach diesem Pass:**
  - Step "Validate patch graph" wird grün (§1.1 fixt das blockierende Finding).
  - Step "Check patch conflicts (strict)" schlägt jetzt fehl bei den 5 Hunk-Overlaps oben — und das ist korrekt: Der Build wäre an diesen Konflikten sowieso gescheitert, nur später und unklarer.

---

## 7. Offene Folgepunkte mit konkreter Verortung

### Hunk-Konflikte aus §1.12 auflösen (verlangt Firefox-Source, §2.2)
- `identity/font-list-spoofing.patch` und `security/speech-voices-spoofing.patch` haben drei **identische Anchor** (`-7477,6`, `-685,6`, `-892,6`). Sie wurden offensichtlich beide gegen den unveränderten Firefox-Tree erstellt, ohne voneinander zu wissen. Auflösung: Beide Hunks von Hand zusammenführen oder die Patch-Anwendungsreihenfolge so wählen, dass der jeweils zweite gegen den Post-Apply-Tree neu erzeugt wird.
- `identity/screen-spoofing.patch` ↔ `media/audio-fingerprint-manager.patch` — gleiche Auflösungsmechanik, aber die Anchor sind nahe (677-682 vs 674-679) statt identisch.
- Bis die Patches wirklich kompatibel sind, kann der Maintainer wahlweise:
  - die fünf Pairings in `patches/manifests/expected_overlaps.yaml` allowlisten (Schein-Workaround — der `git apply` Fehler kommt im Build trotzdem),
  - oder die Patches mergen/umorganisieren (die saubere Lösung).

### §1.2 Security-Defaults — bewusst nicht angefasst
Aus der Folge-Diskussion: Für einen automation-fokussierten Anti-Detection-Browser sind die jetzigen Defaults (Remote-Debugger an, Safe-Browsing aus, `strict_origin_policy=false`) plausibel. Falls gewünscht, lassen sie sich über neue `MaskConfig`-Schalter opt-in/opt-out machen.

### §1.6 / §1.8 / §1.9 / §1.10 — offen
Wie in §4 priorisiert. Können in einem Folge-Pass behandelt werden.

