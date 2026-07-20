# -*- mode: python ; coding: utf-8 -*-
import platform
from pathlib import Path


project = Path(SPEC).resolve().parent
system = platform.system()
icon_extension = {"Windows": "ico", "Darwin": "icns"}.get(system, "png")
icon = project / "assets" / f"icon.{icon_extension}"

a = Analysis(
    [str(project / "folder_browser.py")],
    pathex=[str(project)],
    binaries=[],
    datas=[(str(project / "assets" / "icon.png"), "assets")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="GPAHelper",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon),
)

if system == "Darwin":
    app = BUNDLE(
        exe,
        name="GPA Helper.app",
        icon=str(icon),
        bundle_identifier="org.gpahelper.GPAHelper",
        info_plist={
            "CFBundleDisplayName": "GPA Helper",
            "CFBundleShortVersionString": "1.1.1",
            "NSHighResolutionCapable": True,
        },
    )
