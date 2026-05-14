# Camoufox on Windows - Quick Start Guide

## Overview

This guide helps you build and run Camoufox (a stealth, anti-detect Firefox fork) on Windows.

## Prerequisites

Before you start, ensure you have installed:

1. **Git for Windows**
   - Download from: https://git-scm.com/download/win
   - Include Git Bash in PATH

2. **Python 3.10+**
   - Download from: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation

3. **Windows Build Tools**
   - Visual Studio Build Tools or MinGW-w64 GCC
   - For Windows: [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)

4. **Make utility**
   - Install via Windows package manager or MinGW
   - Or use Windows Subsystem for Linux (WSL2)

## Quick Start

### Option 1: Using PowerShell Script (Recommended)

```powershell
# Open PowerShell in the camoufox_tuned directory

# Show all available commands
.\patch-firefox.ps1 help

# Fetch Firefox source
.\patch-firefox.ps1 fetch

# Prepare and patch Firefox
.\patch-firefox.ps1 patch

# Build Firefox (takes 1-2 hours)
.\patch-firefox.ps1 build

# Run Camoufox
.\patch-firefox.ps1 run
```

### Option 2: Using Command Prompt (CMD)

```cmd
cd camoufox_tuned

# Check status
git status

# View available make targets
make help

# Fetch Firefox source
make fetch

# Prepare patches
make dir

# Build
make build

# Run
make run
```

### Option 3: Using WSL2 (Recommended for Full Build)

WSL2 (Windows Subsystem for Linux) provides a full Linux environment on Windows:

```bash
# Inside WSL2 terminal
cd /mnt/c/path/to/camoufox_tuned
make setup
make bootstrap
make build
```

## Common Tasks

### Build Only for Windows

```powershell
.\patch-firefox.ps1 fetch
.\patch-firefox.ps1 build windows
```

### Clean Build Artifacts

```powershell
.\patch-firefox.ps1 clean
```

### View Build Status

```powershell
.\patch-firefox.ps1 status
```

### Run Built Firefox

```powershell
.\patch-firefox.ps1 run
```

## Troubleshooting

### Issue: "Make not found"

**Solution:** Install Make through one of these methods:

1. **Windows package manager (Recommended)**:
   ```powershell
   # Using Chocolatey
   choco install make

   # Using WinGet
   winget install GNU.Make
   ```

2. **MinGW64**: Install [MinGW-w64](https://www.mingw-w64.org/) and add to PATH

3. **Windows Tools**: Install Visual Studio Build Tools

### Issue: "Python not found"

**Solution:** 
- Ensure Python is in PATH: `python --version`
- Use `python -m pip --version` to verify pip installation
- Restart PowerShell/CMD after installing Python

### Issue: Git line endings (CRLF vs LF)

**Solution:**
```powershell
# Before cloning
git config --global core.autocrlf true

# After cloning, if issues persist
git config core.autocrlf false
```

### Issue: Build fails with GCC/compiler errors

**Solution:**
1. Ensure you have the correct compiler installed
2. For Windows: Install Visual Studio Build Tools
3. For MinGW: Ensure MinGW is in PATH
4. Try building with `make clean` first, then `make build`

## Build System Overview

The Camoufox build system consists of:

- **Makefile**: Main build orchestration
- **multibuild.py**: Cross-platform build script
- **patches/**: Firefox patches (fingerprint spoofing, stealth, debloat)
- **additions/**: Custom Firefox additions (UI, config)
- **pythonlib/**: Python interface for Camoufox

## Windows-Specific Patching

To use Camoufox for web scraping on Windows:

```python
from camoufox.sync_api import Camoufox

# Create browser with spoofed fingerprint
with Camoufox(config={
    "navigator.userAgent": "Mozilla/5.0...",
    "navigator.platform": "Win32",
    "screen.width": 1920,
    "screen.height": 1080,
}) as browser:
    page = browser.new_page()
    page.goto("https://example.com")
    # Your automation here
```

## Additional Resources

- **Main README**: See `README.md` for full documentation
- **Project Plan**: See `plan.md` for known issues and roadmap
- **Python Library**: See `pythonlib/README.md` for Python integration
- **Issues**: Open an issue on GitHub for bug reports

## Support

For issues and questions:
1. Check existing GitHub issues
2. Review the plan.md file for known issues
3. Open a new GitHub issue with details about your environment

---

**Last Updated**: 2026-05-14  
**Tested on**: Windows 11 Home (Build 26200)
