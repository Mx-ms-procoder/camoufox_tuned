# Reproduktion der Audit-Ergebnisse

Die gespeicherten Resultate beziehen sich auf Commit c8105670e50cd27cd14582131664d73f10616a3c und den in [REPORT.md](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/REPORT.md) angegebenen Windows-Build. Die Proben erzeugen eigene temporäre Browserprofile und verwenden lokale Testseiten.

Die Python-Testumgebung wurde außerhalb des Git-Repositories unter `C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/.audit-env` erstellt. Installierte Pakete stehen in [test-environment.txt](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/test-environment.txt). Diese Datei dokumentiert die tatsächlich verwendete Umgebung; sie ersetzt nicht die zu auditierende requirements.lock.

## Vorhandene Umgebung verwenden

PowerShell:

```powershell
$auditRepo = 'C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned'
$auditPython = 'C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/.audit-env/Scripts/python.exe'
$auditBrowser = 'C:/Users/maxim/AppData/Local/camoufox/camoufox/Cache/camoufox.exe'
Set-Location -LiteralPath $auditRepo
$env:PYTHONPATH = Join-Path $auditRepo 'pythonlib'
& $auditPython -m pytest pythonlib/tests -q --disable-warnings --junitxml=audits/2026-09-05/evidence/python-tests.xml
& $auditPython scripts/validate_patches.py
```

Erwartung: 97 Python-Tests bestehen. Die Patchmanifest-Prüfung ist keine vollständige Anwendung aller Patches auf einen frisch ausgecheckten Gecko-Baum und kein Browser-Build.

## Bestätigte Fehler erneut messen

```powershell
& $auditPython audits/2026-09-05/source_probes.py
& $auditPython audits/2026-09-05/check_monitor_after.py
node audits/2026-09-05/protocol_probe.cjs
& $auditPython audits/2026-09-05/run_runtime_probes.py $auditBrowser
& $auditPython audits/2026-09-05/screen_probe.py $auditBrowser
& $auditPython audits/2026-09-05/mouse_probe.py $auditBrowser
```

Die Programme schreiben JSON-/Text-Evidenz in den Audit-Unterordner. Ein normaler Prozess-Exit der Proben bedeutet, dass die Messung abgeschlossen wurde; die Programme sind Diagnoseproben und werten einen bekannten Browserfehler nicht automatisch als Prozessfehler.

Erwartete Kernergebnisse am untersuchten Build:

| Probe | Erwartetes Ergebnis |
|---|---|
| source_probes.py | Alter Monitor: 0 Records, Exit 0; unveränderte IP aus Proxy-Cache ohne zweite Netzwerkanfrage; Portrait-Panel abgelehnt |
| check_monitor_after.py | Repaired Monitor: 163 Records, status outdated, interner Exit 1, vier neuere Advisories; das Wrapperprogramm selbst endet regulär |
| protocol_probe.cjs | baselineAccepted=true, modernAccepted=false |
| run_runtime_probes.py, Seed 0 | Audio-Slices und WebGL direkt/PBO identisch |
| run_runtime_probes.py, Seeds 111/222 | 128 unterschiedliche Audio-Samples; 1160/1211 unterschiedliche WebGL-Bytes; 20/27 außerhalb des angeforderten Pack-Rechtecks veränderte Bytes |
| run_runtime_probes.py | initMarker=null trotz allowMainWorld=true; endliche Animation mit ComputedTiming 0 |
| screen_probe.py | Mit 800px-Viewport CSS-Gerätebreite 800 statt konfigurierten 1664; ohne Override stimmt 1664 |
| mouse_probe.py | Lokale kurze Headless-Probe ohne Hänger; keine Widerlegung sämtlicher Upstream-Deadlocks |

Die Header-Messung nutzt einen Python-HTTP/1-Server auf 127.0.0.1. Sie misst keine TLS-/HTTP2-Pakete und keine echte Proxy-Verbindung. Die Roh-Engine-Konfiguration lautet `allowMainWorld`; das Python-Launcher-Argument lautet `main_world_eval`. Gemessen wird durch Code der Seite selbst, anschließend werden die Ergebnisse über das DOM gelesen.

## C++-Helper

C++17-Compiler erforderlich. Die Untersuchung verwendete MinGW g++ aus `C:/msys64/mingw64/bin/g++.exe`.

```powershell
New-Item -ItemType Directory -Force -Path 'audits/2026-09-05/.build' | Out-Null
foreach ($auditTest in @('CanvasNoise', 'AudioNoise', 'SdpSanitize')) {
    & g++ -std=c++17 -O2 -I additions/camoucfg "additions/camoucfg/${auditTest}_test.cpp" -o "audits/2026-09-05/.build/${auditTest}_test.exe"
    if ($LASTEXITCODE -ne 0) { throw "Compilation failed: $auditTest" }
    & "./audits/2026-09-05/.build/${auditTest}_test.exe"
    if ($LASTEXITCODE -ne 0) { throw "Test failed: $auditTest" }
}
& g++ -std=c++17 -O2 -I additions/camoucfg audits/2026-09-05/noise_probes.cpp -o audits/2026-09-05/.build/noise_probes.exe
if ($LASTEXITCODE -ne 0) { throw 'Compilation failed: noise_probes' }
& ./audits/2026-09-05/.build/noise_probes.exe
```

37 vorhandene Checks bestanden. Die zusätzliche Noise-Probe dokumentiert zwei Codefehler und einen isolierten Helper-Grenzfall. Der Nullflächen-Grenzfall wurde vom installierten Browser **nicht** reproduziert und ist deshalb kein bestätigter Browser-Overflow.

## Öffentliche Quellen aktualisieren

```powershell
& $auditPython audits/2026-09-05/collect_public_evidence.py
& $auditPython scripts/check_upstream_security.py --json
```

Diese beiden Aufrufe benötigen Internet. Der Collector überschreibt den damaligen Mozilla-/PyPI-Snapshot mit dem neuen Abruf; die Werte im Bericht können anschließend vom Snapshot abweichen. Vor einer historischen Wiederholung die vorhandene Evidenzkopie behalten. Der GitHub-Snapshot wurde separat abgerufen; der Collector ist kein GitHub-Spiegel.

Der ursprüngliche defekte Monitor ist in [check_upstream_security.before.py](C:/Users/maxim/OneDrive/Dokumente/camoufox_updated_capctha/camoufox_tuned/audits/2026-09-05/evidence/check_upstream_security.before.py) erhalten. source_probes.py importiert absichtlich diese Datei für die Vorher-Probe; check_monitor_after.py importiert das reparierte Produktionsscript.
