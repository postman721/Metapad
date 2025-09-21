# Metapad v4

Metapad is a lightweight text editor built with PyQt, now compatible with **PyQt6 and PyQt5** from the same codebase. It features line numbers, a clean “white-paper” UI, minimal syntax highlighting, Find/Replace, Go To Line, word wrap, and reliable printing (Preview + Direct).

<img width="899" height="667" alt="Image" src="https://github.com/user-attachments/assets/4721799c-d255-4844-b927-cb21f6b11aaf" />

---

## What’s new in version 4

- **PyQt6 / PyQt5 auto-detect**  
  Tries PyQt6 first, falls back to PyQt5 automatically—no code changes needed.

- **White-paper UI**  
  Clean light theme optimized for readability (black text on white, subtle greys for chrome).

- **Print Preview & Direct Print that always show text**  
  Temporary palette/CSS switch ensures black-on-white output so previews aren’t “blank” even if your theme changes.

- **Single-confirmation Exit**  
  Close confirmation handled once via `closeEvent`—no more “press Exit twice”.

- **Robust file dialogs**  
  Safer cross-version options for `QFileDialog` (no `Options()` AttributeError).

- **Minimal highlighter (Python)**  
  Comments & strings only. **Keywords highlighting removed** by request.

- **“New File” in File menu**  
  Quickly clear the editor to start fresh.

- **Address bar**  
  Shows the current file name at a glance.

---

## Quick start

```bash
python3 metapad.py [optional_filename]
```

Examples:
```bash
python3 metapad.py

python3 metapad.py notes.txt
```

---

## Features

- **Line Numbers** in a subtle light-grey gutter.
- **Toolbar & Menus**: New, Open, Save, Undo/Redo, Print (Preview/Direct), Font, Exit.
- **Find & Replace** (modeless): Find next, Replace one, Replace all, Case sensitivity.
- **Go To Line**: Jump directly to a line number.
- **Word Wrap**: Toggle between wrap/no-wrap.
- **Status Bar**: Live line/column indicator.
- **Address Bar**: Shows current file name.
- **Font Picker**: Apply a font to selected text.
- **Printing**:  
  - **Print Preview** and **Direct Print** via Qt Print Support.  
  - Ensures readable black-on-white output regardless of editor styling.
- **Safety prompts**: Confirmation before exiting and before replacing the current document when opening another file.

---

## Compatibility & Dependencies

Metapad runs with **either** PyQt6 **or** PyQt5.

- **Recommended (any OS via pip):**
  ```bash
  # Pick one:
  pip install PyQt6
  # or
  pip install PyQt5
  ```

- **Debian/Ubuntu (APT):**
  ```bash
  sudo apt-get install python3-pyqt6   # or: python3-pyqt5
  ```

If both PyQt6 and PyQt5 are installed, Metapad will prefer **PyQt6**.

---

## Notes

- Printing uses Qt’s print pipeline and temporarily switches the editor to a black-on-white palette so the text is always visible on paper/PDF.
- Minimal syntax highlighter targets Python: **comments & strings only** by design (keywords removed).
- Open via CLI argument or start blank and use File → Open/New.

---

## License & Copyright

Metapad © 2017–2025 JJ Posti <techtimejourney.net>  
This program comes with ABSOLUTELY NO WARRANTY; see: http://www.gnu.org/copyleft/gpl.html  
Released under **GPL Version 2, June 1991**.
