# Metapad v 3.1

![Image](https://github.com/user-attachments/assets/f96b33de-4ebb-476b-995c-f0a86bc0d6fd)

Metapad is a robust PyQt5-based text editor that aims to provide a simple yet efficient interface for reading and writing text files. It comes with features such as line numbers, basic text formatting, and an intuitive toolbar for quick actions.


#### Metapad 3.1

        python3 metapad.py filename_to_open
Added open new empty file to menu seciton.


### Metapad 3.0

Highlights of the Improvements

    Syntax Highlighter (PythonHighlighter):
    A minimalist approach to color Python keywords, comments, and strings. If you open a non-Python file, it will still attempt to highlight based on these simple rules. You can remove or adapt this to your own language rules.

    Find & Replace Dialog (FindReplaceDialog):
    Provides basic functionality:
        Find next
        Replace one
        Replace all
        Case sensitivity checkbox

    Word Wrap Toggle:
    A simple checkable action that toggles between WidgetWidth (wrap on) and NoWrap.

    Go To Line:
    Prompts the user for a line number and moves the cursor there.

    Status Bar Updates:
    Shows current line and column. Updated via a custom signal cursorPositionChangedSignal from the text editor.




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

Running example: python3 metapad.py
