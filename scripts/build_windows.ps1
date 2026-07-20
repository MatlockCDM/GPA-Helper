$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

python -m venv .build-venv
$Python = Join-Path $ProjectRoot ".build-venv\Scripts\python.exe"
& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements-build.txt
& $Python scripts/generate_icons.py
& $Python -m PyInstaller --noconfirm --clean folder_browser.spec

Write-Host "Built: dist/GPAHelper.exe"
