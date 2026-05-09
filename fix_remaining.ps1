### Fix all remaining issues in one pass ###

# ═══════════════════════════════════════════════════════
# Fix #2: Dockerfile.slim - Add curl for health checks
# ═══════════════════════════════════════════════════════
$df = "Dockerfile.slim"
$dc = [System.IO.File]::ReadAllText($df)
$old = "    # Process management`n    tini"
$new = "    # HTTP client for health checks`n    curl `\`n    # Process management`n    tini"
if ($dc.Contains($old)) {
    $dc = $dc.Replace($old, $new)
    [System.IO.File]::WriteAllText($df, $dc)
    Write-Host "FIX2: Added curl to Dockerfile.slim"
} else {
    Write-Host "FIX2: SKIP - target not found"
}

# ═══════════════════════════════════════════════════════
# Fix #8: scanner.py - Add retry logic for auto_solve_captcha
# ═══════════════════════════════════════════════════════
$sf = "scripts_macros\captcha\scanner.py"
$sc = [System.IO.File]::ReadAllText($sf)

# Replace single-shot solver call with retry loop
$old_solve = "    print(f`"\n  `u{1F680}  [AutoSolver] Starte automatischen L`u{00F6}sungs-Prozess f`u{00FC}r: {name}`")"
$new_solve = "    MAX_SOLVER_RETRIES = 3`r`n    print(f`"\n  `u{1F680}  [AutoSolver] Starte automatischen L`u{00F6}sungs-Prozess f`u{00FC}r: {name} (max {MAX_SOLVER_RETRIES} Versuche)`")"
if ($sc.Contains($old_solve)) {
    $sc = $sc.Replace($old_solve, $new_solve)
    Write-Host "FIX8a: Added MAX_SOLVER_RETRIES constant"
}

# Wrap solver calls with retry
$old_try = "    try:`r`n        # 1. TikTok 3D Objects"
$new_try = "    for _attempt in range(MAX_SOLVER_RETRIES):`r`n      try:`r`n        # 1. TikTok 3D Objects"
if ($sc.Contains($old_try)) {
    $sc = $sc.Replace($old_try, $new_try)
    Write-Host "FIX8b: Wrapped solver in retry loop"
}

$old_except = "    except Exception as e:`r`n        print(f`"  `u{274C}  [AutoSolver] Fehler beim Import/Ausf`u{00FC}hren des Solvers: {e}`")`r`n        return False"
$new_except = "      except Exception as e:`r`n        print(f`"  `u{274C}  [AutoSolver] Versuch {_attempt+1}/{MAX_SOLVER_RETRIES} fehlgeschlagen: {e}`")`r`n        if _attempt < MAX_SOLVER_RETRIES - 1:`r`n            await asyncio.sleep(2)`r`n            continue`r`n        return False"
if ($sc.Contains($old_except)) {
    $sc = $sc.Replace($old_except, $new_except)
    Write-Host "FIX8c: Added retry exception handling"
}

[System.IO.File]::WriteAllText($sf, $sc)
Write-Host "Scanner.py retry fix written."

Write-Host "`nAll scanner/dockerfile fixes complete."
