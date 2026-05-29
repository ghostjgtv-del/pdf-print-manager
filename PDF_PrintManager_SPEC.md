# PDF Print Manager — Project Specification

## Overview

Desktop application for Windows that allows batch printing of PDF files with a visual interface, printer selection, print scheduling, and print history. Targets both technical and non-technical users at LFFG.

Built with **Python + CustomTkinter**, compiled to a standalone `.exe` via PyInstaller.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Language | Python 3.11+ |
| UI Framework | CustomTkinter |
| PDF Printing | `win32print` + `win32api` (pywin32) |
| Scheduling | `schedule` library (lightweight, no daemon required) |
| History Storage | SQLite via `sqlite3` (stdlib) |
| Packaging | PyInstaller → single `.exe` |

---

## Project Structure

```
pdf_print_manager/
├── main.py                  # Entry point
├── app.py                   # Main App class (CustomTkinter root)
├── ui/
│   ├── sidebar.py           # Left navigation panel
│   ├── tab_queue.py         # Print Queue tab
│   ├── tab_scheduler.py     # Scheduler tab
│   └── tab_history.py       # History tab
├── core/
│   ├── printer.py           # Printer enumeration and print logic
│   ├── scheduler.py         # Job scheduling logic
│   └── history.py           # SQLite read/write for history
├── assets/
│   └── icon.ico             # App icon
├── data/
│   └── history.db           # Auto-created SQLite database
├── requirements.txt
└── build.spec               # PyInstaller spec file
```

---

## Modules & Features

### 1. Print Queue Tab

- **File selector** — "Add Files" button opens a file dialog filtered to `.pdf` only
- **Folder selector** — "Add Folder" button adds all PDFs inside a selected folder (non-recursive by default; option to include subfolders)
- **Queue list** — Scrollable table showing: filename, full path, page count (if readable), status (`Pending` / `Printed` / `Error`)
- **Reorder** — Up/Down buttons to reorder items in queue
- **Remove** — Remove individual items or clear entire queue
- **Printer selector** — Dropdown populated with all printers installed on the Windows system (uses `win32print.EnumPrinters`)
- **Print button** — Sends all `Pending` items in queue to selected printer sequentially
- **Progress indicator** — Shows current file being printed and overall progress (e.g., `3 / 10`)

### 2. Scheduler Tab

- **Queue snapshot** — Import current queue from Print Queue tab with one click
- **Date/Time picker** — Select target date and time for the print job to execute
- **Scheduled jobs list** — Shows all pending scheduled jobs with: name, file count, printer, scheduled time, status
- **Cancel job** — Remove a scheduled job before it executes
- **Background execution** — Scheduler runs in a background thread; app must remain open for jobs to fire (displayed as a notice to the user)

### 3. History Tab

- **Log table** — Columns: Date/Time, Filename, Printer, Pages, Status (`Success` / `Error`)
- **Filter** — Filter by date range or status
- **Export** — Export history to `.csv`
- **Clear history** — Button to wipe history (with confirmation dialog)

### 4. Settings (sidebar or menu)

- Default printer (persisted between sessions)
- Default folder path for file picker
- Theme toggle: Dark / Light (CustomTkinter native)

---

## Print Logic (core/printer.py)

Uses `pywin32` to send PDFs directly to the Windows print spooler:

```python
import win32api
import win32print

def print_pdf(filepath: str, printer_name: str):
    win32api.ShellExecute(
        0,
        "print",
        filepath,
        f'/d:"{printer_name}"',
        ".",
        0
    )
```

This mirrors the logic from `Print_PDFs.ps1` — no external PDF renderer needed, uses the system's default PDF handler (Adobe, Edge, etc.).

---

## UI Design Guidelines

- **Theme:** Dark mode by default (CustomTkinter `"dark"`)
- **Accent color:** Blue (`#1f6aa5` — CustomTkinter default blue)
- **Layout:** Left sidebar for navigation tabs; main content area on the right
- **Font:** CustomTkinter default (Segoe UI on Windows)
- **Sidebar icons:** Use text labels (no icon library dependency)
- **Minimum window size:** 900 × 600 px
- **Resizable:** Yes

---

## Non-Functional Requirements

- **Single `.exe`** — No Python installation required on target machines
- **No admin rights** needed to run (standard user permissions)
- **Offline only** — No network calls, fully local
- **SQLite DB auto-created** on first run in `./data/history.db`
- **Error handling** — If a PDF fails to print, log the error to history and continue with the next file; do not crash

---

## Out of Scope (v1)

- Multi-format support (Word, Excel, images) — PDF only
- Network/shared printer advanced configuration
- Print preview
- Cloud sync
- Multi-user / server mode

---

## Dependencies (requirements.txt)

```
customtkinter
pywin32
schedule
pyinstaller
```

---

## Build Command (PyInstaller)

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico --name="PDF Print Manager" main.py
```

---

## Development Notes for Claude Code

- Start with `main.py` → `app.py` → `ui/tab_queue.py` as the first working skeleton
- Wire printer enumeration early so the dropdown is functional from the start
- Use `threading.Thread` for the scheduler loop to keep the UI responsive
- SQLite history writes should be wrapped in try/except to avoid blocking the UI
- Test print logic with `win32api.ShellExecute` before integrating into UI
