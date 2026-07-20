#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

python3 -m venv .build-venv
build_python="$project_root/.build-venv/bin/python"
"$build_python" -m pip install --upgrade pip
"$build_python" -m pip install -r requirements-build.txt
"$build_python" scripts/generate_icons.py
"$build_python" -m PyInstaller --noconfirm --clean folder_browser.spec

signing_identity="${MACOS_SIGN_IDENTITY:--}"
codesign --force --deep --options runtime --sign "$signing_identity" "dist/GPA Helper.app"
hdiutil create -volname "GPA Helper" -srcfolder "dist/GPA Helper.app" -ov -format UDZO "dist/GPAHelper-macOS.dmg"

echo "Built: dist/GPAHelper-macOS.dmg"
