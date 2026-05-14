#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Camoufox Firefox Patching Tool - Command-line interface for Windows

.DESCRIPTION
    This script provides a user-friendly way to patch Firefox with Camoufox patches
    from Windows command line. It wraps the Makefile build system.

.PARAMETER Action
    The action to perform: 'fetch', 'patch', 'build', 'run', 'clean', 'help'

.PARAMETER Target
    The build target: 'windows', 'linux', 'macos'

.EXAMPLE
    .\patch-firefox.ps1 -Action fetch
    .\patch-firefox.ps1 -Action patch
    .\patch-firefox.ps1 -Action build
    .\patch-firefox.ps1 -Action run
#>

param(
    [Parameter(Position=0)]
    [ValidateSet('fetch', 'patch', 'build', 'run', 'clean', 'help', 'status')]
    [string]$Action = 'help',

    [Parameter(Position=1)]
    [ValidateSet('windows', 'linux', 'macos')]
    [string]$Target = 'windows'
)

function Show-Help {
    Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║        Camoufox Firefox Patching Tool for Windows              ║
╚════════════════════════════════════════════════════════════════╝

USAGE:
    .\patch-firefox.ps1 [ACTION] [TARGET]

ACTIONS:
    fetch       - Download Firefox source code
    patch       - Apply Camoufox patches to Firefox
    build       - Build the patched Firefox
    run         - Run the built Firefox
    clean       - Clean build artifacts
    status      - Show build status
    help        - Show this help message

TARGETS:
    windows     - Build for Windows (default)
    linux       - Build for Linux
    macos       - Build for macOS

EXAMPLES:
    .\patch-firefox.ps1 fetch
    .\patch-firefox.ps1 patch
    .\patch-firefox.ps1 build windows
    .\patch-firefox.ps1 run

REQUIREMENTS:
    - Git for Windows
    - WSL2 (for Linux build) or native Linux
    - Make, Python 3, GCC/Clang

DOCUMENTATION:
    See README.md for detailed build instructions
    See plan.md for project status and roadmap
"@
}

function Test-Prerequisites {
    Write-Host "Checking prerequisites..." -ForegroundColor Cyan

    $missing = @()

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        $missing += "git"
    }

    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        $missing += "python"
    }

    if ($missing.Count -gt 0) {
        Write-Host "❌ Missing requirements: $($missing -join ', ')" -ForegroundColor Red
        Write-Host "Please install the missing tools and try again." -ForegroundColor Yellow
        return $false
    }

    Write-Host "✓ All prerequisites found" -ForegroundColor Green
    return $true
}

function Invoke-Action {
    param(
        [string]$ActionName,
        [string]$TargetName
    )

    Write-Host "━" * 64 -ForegroundColor Cyan
    Write-Host "  $ActionName for $TargetName" -ForegroundColor Yellow
    Write-Host "━" * 64 -ForegroundColor Cyan

    switch ($ActionName) {
        'fetch' {
            Write-Host "Fetching Firefox source..." -ForegroundColor Cyan
            & make fetch
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Firefox source fetched successfully" -ForegroundColor Green
            } else {
                Write-Host "❌ Failed to fetch Firefox source" -ForegroundColor Red
                return $false
            }
        }

        'patch' {
            Write-Host "Preparing and patching Firefox..." -ForegroundColor Cyan
            & make dir
            if ($LASTEXITCODE -ne 0) {
                Write-Host "❌ Failed to prepare source directory" -ForegroundColor Red
                return $false
            }
            Write-Host "✓ Firefox source prepared and patched" -ForegroundColor Green
        }

        'build' {
            Write-Host "Building patched Firefox (this may take a while)..." -ForegroundColor Cyan
            & make build
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Firefox built successfully" -ForegroundColor Green
            } else {
                Write-Host "❌ Build failed" -ForegroundColor Red
                return $false
            }
        }

        'run' {
            Write-Host "Running Camoufox..." -ForegroundColor Cyan
            & make run
        }

        'clean' {
            Write-Host "Cleaning build artifacts..." -ForegroundColor Cyan
            & make clean
            Write-Host "✓ Cleaned" -ForegroundColor Green
        }

        'status' {
            Write-Host "Build Status:" -ForegroundColor Cyan
            & git status
            Write-Host ""
            Write-Host "Recent Commits:" -ForegroundColor Cyan
            & git log --oneline -5
        }
    }

    return $true
}

# Main execution
switch ($Action) {
    'help' {
        Show-Help
    }

    default {
        if (-not (Test-Prerequisites)) {
            exit 1
        }

        $success = Invoke-Action -ActionName $Action -TargetName $Target
        if (-not $success) {
            exit 1
        }
    }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
