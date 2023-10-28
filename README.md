# Metapad v 2.0

Metapad is a robust PyQt5-based text editor that aims to provide a simple yet efficient interface for reading and writing text files. It comes with features such as line numbers, basic text formatting, and an intuitive toolbar for quick actions.

## Features:
- **Line Numbers**: Clearly visualized line numbers next to your text.
- **Toolbar**: A toolbar for quick actions such as undo, redo, save, open, print, and font selection.
- **Styling**: Custom styling for the editor and the application, done via CSS styling. Icons are from Adwaita icons theme. Without icons a button with a text will be shown.
- **Font Change**: Quickly change the font of the selected text.
- **Open/Save Dialog**: Intuitive dialogs for opening and saving your files.
- **Printing**: A print preview and printing capability.
- **Protection**: Before closing or opening new files, a warning is given if there are unsaved changes.

## Dependencies:

- **PyQt5**: For the main GUI components.
- **PyQt5.QtPrintSupport**: For print preview and printing capabilities.
- **subprocess, os, sys**: Other Python libraries for various tasks.

## Copyright:

Metapad v.2.0 is Copyright (c) 2017 by JJ Posti <techtimejourney.net>. This program comes with ABSOLUTELY NO WARRANTY; for details see: http://www.gnu.org/copyleft/gpl.html. Metapad is free software, and you are welcome to redistribute it under GPL Version 2, June 1991.

## Installation:

Before you run Metapad, ensure you have the required dependencies installed.

```bash
pip install PyQt5

Debian/Ubuntu:

sudo apt-get install python3-pyqt5
sudo apt-get install adwaita-icon-theme
