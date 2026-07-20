# Building GPA Helper installers

The project produces three native downloads:

- `GPAHelper.exe` for Windows
- `GPAHelper.flatpak` for Linux
- `GPAHelper-macOS.dmg` containing the Mac application

PyInstaller packages are operating-system specific, so each one must be built
on its target operating system. The GitHub Actions workflow does this
automatically on native Windows, Ubuntu, and macOS runners.

## Automated builds

1. Put this project in a GitHub repository.
2. Open **Actions → Build installers → Run workflow**.
3. Download the three artifacts from the completed workflow run.

Pushing a tag such as `v1.0.0` starts the workflow and creates a GitHub Release
with all three installers attached as direct downloads.

## Local Windows build

Install Python 3 with Tkinter, open PowerShell in the project directory, and
run:

```powershell
.\scripts\build_windows.ps1
```

The one-file executable is written to `dist\GPAHelper.exe`.

## Local Linux Flatpak build

Install Python 3, Tkinter, Flatpak, and Flatpak Builder. Add Flathub and install
the 24.08 Freedesktop Platform and SDK, then run:

```bash
./scripts/build_linux.sh
```

Install the resulting bundle by double-clicking `dist/GPAHelper.flatpak` in a
Flatpak-aware software center, or with:

```bash
flatpak install --user dist/GPAHelper.flatpak
```

The Flatpak can access lesson folders under the user's home directory.

## Local macOS build

Install Python 3 with Tkinter and run:

```bash
./scripts/build_macos.sh
```

This creates `dist/GPAHelper-macOS.dmg`. By default the app is ad-hoc signed,
which is suitable for testing. For distribution without Gatekeeper warnings,
set `MACOS_SIGN_IDENTITY` to an Apple Developer ID Application certificate
before building, then notarize the DMG with Apple's `notarytool`. Apple requires
a paid Developer Program identity for that final signing and notarization step.

## Current local build status

The Linux standalone executable has been built at `dist/GPAHelper`. The final
Flatpak bundle needs Flatpak Builder and the Freedesktop runtime; if those are
not installed locally, the automated Ubuntu build creates it instead. Windows
and macOS packages are intentionally produced on their native workflow runners.
