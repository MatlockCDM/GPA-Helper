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
cp dist/GPAHelper packaging/flatpak/GPAHelper
cp assets/icon-128.png packaging/flatpak/icon-128.png
cp assets/icon-256.png packaging/flatpak/icon-256.png

flatpak-builder --disable-rofiles-fuse --force-clean --repo=flatpak-repo flatpak-build packaging/flatpak/org.gpahelper.GPAHelper.yml
flatpak build-bundle flatpak-repo dist/GPAHelper.flatpak org.gpahelper.GPAHelper

echo "Built: dist/GPAHelper.flatpak"
