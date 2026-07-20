<p align="center">
  <img src="assets/icon.png" alt="GPA Helper icon" width="150">
</p>

<h1 align="center">GPA Helper</h1>

<p align="center">
  A simple desktop dashboard for finding, reviewing, and searching numbered
  language-lesson folders.
</p>

<p align="center">
  <a href="https://github.com/MatlockCDM/GPA-Helper/releases/latest"><strong>Download the latest release</strong></a>
</p>

## What it does

GPA Helper turns a directory of numbered lesson folders into a spaced-review
queue. It automatically shows the newest lesson and any available lessons from
1, 3, 5, 10, 20, 40, 105, and 365 sessions ago.

- Open review folders directly from the dashboard.
- See which folders you have already opened during the session.
- Search plain text, Markdown, CSV, PDF, Word, OpenDocument, and RTF files
  without freezing the interface.
- Open a matching note by double-clicking its search result.
- Remember the last lesson directory you selected.
- Run locally without an internet connection.

## Download

Prebuilt packages are available on the
[Releases page](https://github.com/MatlockCDM/GPA-Helper/releases/latest):

| Platform | Download | Format |
| --- | --- | --- |
| Windows | `GPAHelper.exe` | Standalone 64-bit application |
| Linux | `GPAHelper.flatpak` | Flatpak bundle |
| macOS | `GPAHelper-macOS.dmg` | Disk image containing the app |

The packages are currently unsigned. Windows SmartScreen or macOS Gatekeeper
may therefore display a warning the first time the application is opened.

### Linux installation

Double-click the Flatpak bundle in a Flatpak-aware software center, or run:

```bash
flatpak install --user GPAHelper.flatpak
```

## Organize your lessons

Each lesson folder must begin with its session number. Everything after the
number is optional.

```text
Language Lessons/
├── 1 Feb 10/
├── 2 Feb 15/
├── 3 Feb 20 - Travel/
└── 4 Feb 25/
```

Names such as `English Class 1` are not detected because the number is not at
the beginning.

## Supported file formats

GPA Helper searches inside the following files:

| Category | Extensions | Notes |
| --- | --- | --- |
| Plain text | `.txt`, `.text`, `.log` | Standard UTF-8 text files; invalid characters are safely replaced |
| Markdown | `.md` | Markdown formatting is searched as text |
| Spreadsheets and lists | `.csv`, `.tsv` | Searches the text stored in every row and column |
| PDF | `.pdf` | Searches embedded text; image-only scans require OCR and are not currently supported |
| Microsoft Word | `.docx` | Searches paragraphs and table cells |
| OpenDocument | `.odt` | Searches document paragraphs |
| Rich Text Format | `.rtf` | Searches text after removing RTF formatting |
| Legacy Microsoft Word | `.doc` | Requires antiword, LibreOffice, or macOS `textutil` |

Searches are case-insensitive. Password-protected, corrupted, or otherwise
unreadable documents are skipped and included in the search status count.

## Use GPA Helper

1. Launch the application.
2. Select **Choose folder** and pick the directory containing your lessons.
3. Open lessons from the review queue on the left.
4. Enter a word or phrase on the right to search all supported notes and documents.
5. Double-click a search result to open it in your default text editor.

The application only reads lesson names and documents; it does not rename,
move, or delete lesson content.

## Run from source

GPA Helper requires Python 3 with Tkinter:

```bash
python3 folder_browser.py
```

No third-party runtime packages are required. Tkinter is included with the
Python installer from python.org; some Linux distributions package it
separately.

Run the automated tests with:

```bash
python3 -m unittest -v
```

## Build installers

Native packaging scripts and a GitHub Actions workflow are included for all
three platforms. See [BUILDING.md](BUILDING.md) for local and automated build
instructions.

## License

GPA Helper is released into the public domain under
[The Unlicense](LICENSE).
