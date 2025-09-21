#!/usr/bin/env python3
# Metapad (PyQt6 / PyQt5 compatible)
# White-paper UI
# GPL v2

import sys, os

# --- Try PyQt6 first, fallback to PyQt5 ---
try:
    from PyQt6.QtCore import (Qt, QRegularExpression, QRect, QUrl, QSize, pyqtSignal)
    from PyQt6.QtGui import (QFont, QPainter, QTextCharFormat, QSyntaxHighlighter,
                             QTextCursor, QColor, QAction, QPalette, QTextDocument)
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPlainTextEdit,
                                 QToolBar, QLabel, QFileDialog, QMessageBox,
                                 QFontDialog, QInputDialog, QDialog, QVBoxLayout,
                                 QHBoxLayout, QPushButton, QLineEdit, QCheckBox)
    from PyQt6.QtPrintSupport import QPrintPreviewDialog, QPrinter, QPrintDialog
    USING_QT6 = True
    print("Using PyQt6")
except ImportError:
    from PyQt5.QtCore import (Qt, QRegExp, QRect, QUrl, QSize, pyqtSignal)
    from PyQt5.QtGui import (QFont, QPainter, QTextCharFormat, QSyntaxHighlighter,
                             QTextCursor, QColor, QPalette, QTextDocument)
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPlainTextEdit,
                                 QToolBar, QLabel, QFileDialog, QMessageBox,
                                 QFontDialog, QInputDialog, QDialog, QVBoxLayout,
                                 QHBoxLayout, QPushButton, QLineEdit, QCheckBox, QAction)
    from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter, QPrintDialog
    USING_QT6 = False
    print("Using PyQt5")

# --- Cross-version QMessageBox buttons ---
if USING_QT6:
    MB_OK = QMessageBox.StandardButton.Ok
    MB_CANCEL = QMessageBox.StandardButton.Cancel
    MB_YES = QMessageBox.StandardButton.Yes
    MB_NO = QMessageBox.StandardButton.No
else:
    MB_OK = QMessageBox.Ok
    MB_CANCEL = QMessageBox.Cancel
    MB_YES = QMessageBox.Yes
    MB_NO = QMessageBox.No

# --- Safe file dialog options helper ---
def file_dialog_options():
    """
    Return a safe 'options' value for QFileDialog across PyQt5/6.
    Avoids crashes on builds missing Options/Option attributes.
    """
    Option = getattr(QFileDialog, "Option", None)
    if Option is not None:
        try:
            opts = Option(0)
            dont = getattr(Option, "DontUseNativeDialog", None)
            if dont is not None:
                opts |= dont
            return opts
        except Exception:
            pass
    Options = getattr(QFileDialog, "Options", None)
    if Options is not None:
        try:
            opts = Options()
            if hasattr(QFileDialog, "DontUseNativeDialog"):
                opts |= QFileDialog.DontUseNativeDialog
            return opts
        except Exception:
            pass
    return getattr(QFileDialog, "DontUseNativeDialog", 0) or 0


# ---- Syntax Highlighter (comments + strings only; keywords removed) ----
class PythonHighlighter(QSyntaxHighlighter):
    """Minimal Python syntax highlighter (comments & strings)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_highlighting_rules()

    def init_highlighting_rules(self):
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6a737d"))  # grey

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#d14"))      # red-ish

        self.highlighting_rules = []
        self.highlighting_rules.append((r'#[^\n]*', comment_format))
        self.highlighting_rules.append((r"'[^']*'", string_format))
        self.highlighting_rules.append((r'"[^"]*"', string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            if USING_QT6:
                regex = QRegularExpression(pattern)
                match = regex.globalMatch(text)
                while match.hasNext():
                    m = match.next()
                    self.setFormat(m.capturedStart(), m.capturedLength(), fmt)
            else:
                regex = QRegExp(pattern)
                index = regex.indexIn(text)
                while index >= 0:
                    length = regex.matchedLength()
                    self.setFormat(index, length, fmt)
                    index = regex.indexIn(text, index + length)


# ---- Line Number Area ----
class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.metapad = editor

    def sizeHint(self):
        return QSize(self.metapad.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.metapad.lineNumberAreaPaintEvent(event)


# ---- Find & Replace Dialog ----
class FindReplaceDialog(QDialog):
    def __init__(self, parent=None, editor=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("Find & Replace")
        self.setModal(False)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        # Find input
        find_layout = QHBoxLayout()
        find_label = QLabel("Find:")
        self.find_input = QLineEdit()
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)

        # Replace input
        replace_layout = QHBoxLayout()
        replace_label = QLabel("Replace:")
        self.replace_input = QLineEdit()
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)

        # Match case checkbox
        self.match_case_checkbox = QCheckBox("Match case")
        layout.addWidget(self.match_case_checkbox)

        # Buttons
        button_layout = QHBoxLayout()
        self.find_button = QPushButton("Find Next")
        self.replace_button = QPushButton("Replace")
        self.replace_all_button = QPushButton("Replace All")
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.replace_button)
        button_layout.addWidget(self.replace_all_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setFixedSize(400, 160)

        # Signals
        self.find_button.clicked.connect(self.find_next)
        self.replace_button.clicked.connect(self.replace_one)
        self.replace_all_button.clicked.connect(self.replace_all)

    def find_flags(self):
        """Return flags for QPlainTextEdit.find, cross-version safe."""
        if USING_QT6:
            flags = QTextDocument.FindFlag(0)
            if self.match_case_checkbox.isChecked():
                flags |= QTextDocument.FindFlag.FindCaseSensitively
            return flags
        else:
            flags = QTextDocument.FindFlags()
            if self.match_case_checkbox.isChecked():
                flags |= QTextDocument.FindCaseSensitively
            return flags

    def find_next(self):
        text = self.find_input.text()
        if text:
            if not self.editor.find(text, self.find_flags()):
                cursor = self.editor.textCursor()
                if USING_QT6:
                    cursor.movePosition(QTextCursor.MoveOperation.Start)
                else:
                    cursor.movePosition(QTextCursor.Start)
                self.editor.setTextCursor(cursor)
                self.editor.find(text, self.find_flags())

    def replace_one(self):
        text_find = self.find_input.text()
        text_replace = self.replace_input.text()
        cursor = self.editor.textCursor()

        if not cursor.hasSelection():
            self.find_next()
            return

        selected = cursor.selectedText()
        if (selected == text_find or
            (not self.match_case_checkbox.isChecked() and selected.lower() == text_find.lower())):
            cursor.insertText(text_replace)
        self.find_next()

    def replace_all(self):
        text_find = self.find_input.text()
        text_replace = self.replace_input.text()
        if not text_find:
            return

        cursor = self.editor.textCursor()
        if USING_QT6:
            cursor.movePosition(QTextCursor.MoveOperation.Start)
        else:
            cursor.movePosition(QTextCursor.Start)
        self.editor.setTextCursor(cursor)

        count = 0
        while self.editor.find(text_find, self.find_flags()):
            cursor = self.editor.textCursor()
            cursor.insertText(text_replace)
            count += 1

        QMessageBox.information(self, "Replace All",
                                f"Replaced {count} occurrence(s).", MB_OK)


# ---- Main Editor (Metapad) ----
class Metapad(QPlainTextEdit):
    cursorPositionChangedSignal = pyqtSignal(int, int)  # line, col

    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
        self.cursorPositionChanged.connect(self.onCursorPositionChanged)

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        if USING_QT6:
            space = 6 + self.fontMetrics().horizontalAdvance('9') * digits
        else:
            space = 6 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(),
                                       self.lineNumberArea.size().width(),
                                       rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                                              self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#f5f5f5"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()

        while block.isValid() and (top <= event.rect().bottom()):
            number = str(blockNumber + 1)
            painter.setPen(QColor("#888"))
            align = (Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                     if USING_QT6 else Qt.AlignRight | Qt.AlignVCenter)
            painter.drawText(0, top, self.lineNumberArea.width() - 4, height, align, number)
            block = block.next()
            top = int(bottom)
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def onCursorPositionChanged(self):
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.position() - cursor.block().position() + 1
        self.cursorPositionChangedSignal.emit(line, col)


# ---- Main Window ----
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metapad")
        self.resize(900, 640)

        # Editor
        self.metapad = Metapad(self)
        self.setCentralWidget(self.metapad)

        # Syntax highlighting (no keywords)
        self.highlighter = PythonHighlighter(self.metapad.document())

        # Status bar
        self.status = self.statusBar()
        self.status.showMessage("Ready")
        self.metapad.cursorPositionChangedSignal.connect(self.updateStatusBar)

        # Address toolbar (file info)
        self.address_toolbar = QToolBar("File")
        self.addToolBar(self.address_toolbar)
        self.address = QLabel('')
        self.address_toolbar.addWidget(self.address)

        # Toolbars & Menus
        self.createToolbarsAndMenus()

        # Styling (white-paper)
        self.applyStyles()

        # Default font
        font = QFont()
        font.setPointSize(13)
        self.setFont(font)

        # Keep reference to modeless Find/Replace dialog
        self.find_replace_dialog = None

        # Center on screen after sizing
        self.centerOnScreen()

        # Open file from CLI
        if len(sys.argv) > 1:
            self.openFileFromCommandLine(sys.argv[1])

    # ---- UI builders ----
    def createToolbarsAndMenus(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)


        self.open_action = QAction('Open', self)
        self.open_action.triggered.connect(self.openFile)

        self.new_action = QAction('New', self)
        self.new_action.triggered.connect(self.newFile)

        self.undo_action = QAction('Undo', self)
        self.undo_action.triggered.connect(self.metapad.undo)

        self.redo_action = QAction('Redo', self)
        self.redo_action.triggered.connect(self.metapad.redo)

        self.save_action = QAction('Save', self)
        self.save_action.triggered.connect(self.saveFile)

        self.print_action = QAction('Print (Preview)', self)
        self.print_action.triggered.connect(self.printPreview)

        self.print_direct_action = QAction('Print (Direct)', self)
        self.print_direct_action.triggered.connect(self.printDirect)

        self.font_action = QAction('Font', self)
        self.font_action.triggered.connect(self.changeFont)

        self.exit_action = QAction('Exit', self)
        self.exit_action.triggered.connect(self.close)   # call the *base* close(), no custom override

        for act in (self.open_action, self.new_action, self.undo_action, self.redo_action,
                    self.save_action, self.print_action, self.font_action, self.exit_action,
                    self.print_direct_action):
            self.toolbar.addAction(act)

        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.print_action)
        file_menu.addAction(self.print_direct_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = menubar.addMenu("Edit")

        find_replace_action = QAction("Find & Replace", self)
        find_replace_action.triggered.connect(self.openFindReplaceDialog)
        edit_menu.addAction(find_replace_action)

        goto_line_action = QAction("Go to Line", self)
        goto_line_action.triggered.connect(self.gotoLine)
        edit_menu.addAction(goto_line_action)

        self.word_wrap_action = QAction("Word Wrap", self, checkable=True)
        self.word_wrap_action.setChecked(True)
        self.word_wrap_action.triggered.connect(self.toggleWordWrap)
        edit_menu.addAction(self.word_wrap_action)

        edit_menu.addSeparator()
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)

        self.toggleWordWrap()

    def applyStyles(self):
        # White-paper / native-light feel
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
                color: #222222;
            }
            QToolBar {
                background: #f7f7f7;
                border-bottom: 1px solid #dddddd;
                spacing: 6px;
            }
            QToolBar QToolButton {
                background: #ffffff;
                color: #222222;
                border: 1px solid #dcdcdc;
                padding: 4px 8px;
                margin: 4px 3px;
                border-radius: 4px;
            }
            QToolBar QToolButton:hover {
                background: #f0f0f0;
                border: 1px solid #d0d0d0;
            }
            QMenuBar {
                background: #ffffff;
                color: #222222;
                border-bottom: 1px solid #e6e6e6;
            }
            QMenuBar::item:selected {
                background: #e9f2ff;
            }
            QMenu {
                background: #ffffff;
                color: #222222;
                border: 1px solid #e6e6e6;
            }
            QMenu::item:selected {
                background: #e9f2ff;
            }
            QStatusBar {
                background: #ffffff;
                color: #555555;
                border-top: 1px solid #e6e6e6;
            }
        """)
        self.metapad.setStyleSheet("""
            QPlainTextEdit {
                background-color: #ffffff;
                color: #111111;
                border: 1px solid #dddddd;
                border-radius: 6px;
                font-size: 14px;
                selection-background-color: #cfe8ff;
                selection-color: #000000;
                padding: 10px;
            }
        """)

    def centerOnScreen(self):
        if USING_QT6:
            screen_geo = QApplication.primaryScreen().availableGeometry()
            self.move(screen_geo.center() - self.rect().center())
        else:
            self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

    # ---- Feature methods ----
    def updateStatusBar(self, line, col):
        self.status.showMessage(f"Line: {line}, Col: {col}")

    def toggleWordWrap(self):
        if self.word_wrap_action.isChecked():
            if USING_QT6:
                self.metapad.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
            else:
                self.metapad.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            if USING_QT6:
                self.metapad.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
            else:
                self.metapad.setLineWrapMode(QPlainTextEdit.NoWrap)

    def gotoLine(self):
        line, ok = QInputDialog.getInt(self, "Go to Line", "Line number:", 1, 1)
        if ok and line > 0:
            block_count = self.metapad.blockCount()
            if line <= block_count:
                cursor = self.metapad.textCursor()
                if USING_QT6:
                    cursor.movePosition(QTextCursor.MoveOperation.Start)
                    cursor.movePosition(QTextCursor.MoveOperation.Down,
                                        QTextCursor.MoveMode.MoveAnchor, line - 1)
                else:
                    cursor.movePosition(QTextCursor.Start)
                    cursor.movePosition(QTextCursor.Down,
                                        QTextCursor.MoveAnchor, line - 1)
                self.metapad.setTextCursor(cursor)

    def openFindReplaceDialog(self):
        if not self.find_replace_dialog:
            self.find_replace_dialog = FindReplaceDialog(self, self.metapad)
        self.find_replace_dialog.show()
        self.find_replace_dialog.raise_()
        self.find_replace_dialog.activateWindow()

    def openFileFromCommandLine(self, filepath):
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    self.metapad.setPlainText(file.read())
                self.address.setText(f'Now viewing: {os.path.basename(filepath)}')
            except Exception as e:
                QMessageBox.warning(self, "File Open Error", f"Failed to open file:\n{e}", MB_OK)
        else:
            QMessageBox.warning(self, "File Not Found", f"Cannot find file: {filepath}", MB_OK)

    def changeFont(self):
        font, ok = QFontDialog.getFont(self.metapad.font(), self,
                                       'Select a font (applies to selected text if present).')
        if ok:
            cursor = self.metapad.textCursor()
            fmt = QTextCharFormat()
            fmt.setFont(font)
            cursor.mergeCharFormat(fmt)
            self.metapad.setTextCursor(cursor)

    def newFile(self):
        reply = QMessageBox.question(self, 'New File',
                                     'Do you want to discard changes and start a new file?',
                                     MB_YES | MB_NO)
        if reply == MB_YES:
            self.metapad.clear()
            self.address.setText('New File')

    def openFile(self):
        try:
            options = file_dialog_options()
            fileName, _ = QFileDialog.getOpenFileName(
                self.metapad, "Open a file", "",
                "All Files (*);;Text Files (*.txt);;"
                "Python Files (*.py);;C++ Files (*.cpp);;"
                "Bash Files (*.sh);;Javascript Files (*.js);;"
                "Odt text files (*.odt)",
                options=options
            )
            if fileName:
                buttonReply = QMessageBox.question(
                    self.metapad, 'Open new file?',
                    "All unsaved documents will be lost. If unsure press Cancel now.",
                    MB_CANCEL | MB_OK
                )
                if buttonReply == MB_OK:
                    with open(fileName, 'r', encoding='utf-8', errors='ignore') as f:
                        alltxt = f.read()
                        self.metapad.setPlainText(alltxt)
                    filename = os.path.basename(fileName)
                    self.address.setText('Now viewing: ' + filename)
        except Exception as e:
            print("Cannot handle, Will not continue. Error:", e)

    def saveFile(self):
        try:
            options = file_dialog_options()
            fileName, _ = QFileDialog.getSaveFileName(
                self.metapad, "Save as", "",
                "All Files (*);;Text Files (*.txt);;"
                "Python Files (*.py);;C++ Files (*.cpp);;"
                "Bash Files (*.sh);;Javascript Files (*.js);;"
                "Odt text Files (*.odt)",
                options=options
            )
            if fileName:
                with open(fileName, 'w', encoding='utf-8') as f:
                    f.write(self.metapad.toPlainText())
                filename = os.path.basename(fileName)
                self.address.setText('Now viewing: ' + filename)
        except Exception as e:
            print("Cannot handle, Will not continue. Error:", e)

    # --- Printing helpers (CSS/palette safety — on white theme this is mostly a no-op) ---
    def _print_to_printer(self, printer):
        """
        Ensure black text on white during print/preview.
        """
        old_style = self.metapad.styleSheet()
        old_pal = self.metapad.palette()

        try:
            pal = QPalette(old_pal)
            if USING_QT6:
                pal.setColor(QPalette.ColorRole.Text, QColor("black"))
                pal.setColor(QPalette.ColorRole.Base, QColor("white"))
                pal.setColor(QPalette.ColorRole.Window, QColor("white"))
            else:
                pal.setColor(QPalette.Text, QColor("black"))
                pal.setColor(QPalette.Base, QColor("white"))
                pal.setColor(QPalette.Window, QColor("white"))
            self.metapad.setPalette(pal)
            self.metapad.setStyleSheet("QPlainTextEdit { color:#000; background:#fff; }")
            self.metapad.document().print(printer)
        finally:
            self.metapad.setStyleSheet(old_style)
            self.metapad.setPalette(old_pal)

    def printPreview(self):
        try:
            mode = getattr(QPrinter, "PrinterMode", None)
            if mode is not None:  # Qt6
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            else:  # Qt5
                printer = QPrinter(QPrinter.HighResolution)

            preview = QPrintPreviewDialog(printer, self)
            preview.paintRequested.connect(self._print_to_printer)
            if hasattr(preview, "exec"):
                preview.exec()
            else:
                preview.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Print Error", str(e), MB_OK)

    def printDirect(self):
        try:
            mode = getattr(QPrinter, "PrinterMode", None)
            if mode is not None:  # Qt6
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            else:  # Qt5
                printer = QPrinter(QPrinter.HighResolution)

            dlg = QPrintDialog(printer, self)
            accepted = dlg.exec() if hasattr(dlg, "exec") else dlg.exec_()
            if accepted:
                self._print_to_printer(printer)
        except Exception as e:
            QMessageBox.critical(self, "Print Error", str(e), MB_OK)

    # --- Single confirmation on close (fixes "must press Exit twice") ---
    def closeEvent(self, event):
        resp = QMessageBox.question(self, 'Quit now?',
                                    "All unsaved documents will be lost. If unsure press Cancel now.",
                                    MB_CANCEL | MB_OK)
        if resp == MB_OK:
            event.accept()
        else:
            event.ignore()

    def showAbout(self):
        QMessageBox.information(self, "About Metapad",
                                "Metapad v4 (white-paper UI)\n\n"
                                "Copyright (c) 2017 JJ Posti <techtimejourney.net>\n"
                                "Cross-compatible PyQt5/6 version.\n"
                                "Distributed under GPL v2.",
                                MB_OK)


# ---- Main Entry Point ----
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        window.metapad.zoomIn(1)
    except Exception:
        pass
    sys.exit(app.exec() if USING_QT6 else app.exec_())
