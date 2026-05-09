$f = "scripts_macros\captcha\scanner.py"
$c = [System.IO.File]::ReadAllText($f)

# Fix 1: Add allText declaration
$old = "let scriptSrcs = [];`r`nlet currentPath"
$new = "let scriptSrcs = [];`r`nlet allText = `"`";`r`nlet currentPath"
if ($c.Contains($old)) {
    $c = $c.Replace($old, $new)
    Write-Host "FIX1a: Added allText declaration"
} else {
    Write-Host "FIX1a: Target not found (maybe LF only?)"
    $old2 = "let scriptSrcs = [];`nlet currentPath"
    $new2 = "let scriptSrcs = [];`nlet allText = `"`";`nlet currentPath"
    if ($c.Contains($old2)) {
        $c = $c.Replace($old2, $new2)
        Write-Host "FIX1a: Added allText declaration (LF)"
    }
}

# Fix 1b: Add allText update in updateGlobals()
$old = "    iframeSrcs = [];`r`n    scriptSrcs = [];"
$new = "    iframeSrcs = [];`r`n    scriptSrcs = [];`r`n    allText = document.body ? document.body.textContent.toLowerCase() : `"`";"
if ($c.Contains($old)) {
    $c = $c.Replace($old, $new)
    Write-Host "FIX1b: Added allText update in updateGlobals()"
} else {
    Write-Host "FIX1b: Target not found (trying LF)"
    $old2 = "    iframeSrcs = [];`n    scriptSrcs = [];"
    $new2 = "    iframeSrcs = [];`n    scriptSrcs = [];`n    allText = document.body ? document.body.textContent.toLowerCase() : `"`";"
    if ($c.Contains($old2)) {
        $c = $c.Replace($old2, $new2)
        Write-Host "FIX1b: Added allText update in updateGlobals() (LF)"
    }
}

[System.IO.File]::WriteAllText($f, $c)
Write-Host "Scanner.py fixes written."
