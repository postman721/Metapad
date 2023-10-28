from PyQt5.QtCore import *  ;from PyQt5.QtGui import *  ;from PyQt5.QtWidgets import *;from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter; import subprocess, os, sys

# -*- coding: utf-8 -*-
#Metapad v.2.0 Copyright (c) 2017 JJ Posti <techtimejourney.net> 
#This program comes with ABSOLUTELY NO WARRANTY; 
#for details see: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#This is free software, and you are welcome to redistribute it under 
#GPL Version 2, June 1991")

#!/usr/bin/env python3

# Custom QWidget for displaying line numbers
class QLineNumberArea(QWidget):
#This is the constructor (initializer) method of the QLineNumberArea class. It is called when an instance of the class is created. 	
    def __init__(self, editor):
#This line calls the constructor of the parent class QWidget (the superclass) and passes the editor widget as an argument. This ensures that the QWidget part of the custom widget is properly initialized.		
        super().__init__(editor)
#This line assigns the editor widget to an instance variable called metapad. Notice how we call this on the main loop at the bottom.
        self.metapad = editor

    def sizeHint(self):
        return QSize(self.metapad.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.metapad.lineNumberAreaPaintEvent(event)

class Metapad(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
    # Calculate the width needed to display line numbers
    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value //= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    # Update the width of the line number area when the block count changes
    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    # Update the line number area based on the update request
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.size().width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    # Resize the line number area when the main window is resized
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    # Paint event for the line number area
    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.yellow)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()

        # Draw line numbers for visible blocks
        while block.isValid() and (top <= event.rect().bottom()):
            number = str(blockNumber + 1)
            painter.setPen(Qt.black)
            painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)
            block = block.next()
            top = int(bottom)
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
            
#Actual MainWindow. This one will reference to metapad class by setting it as a centralWidget. We want to make sure our menus and gui materials show.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())
        # Create the text editor (Metapad instance)
        self.metapad = Metapad(self)
        self.resize(800, 600)
        QIcon.setThemeName('Adwaita')  
#####################
#Toolbar/Menu
#####################
        # Add Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Add Open Action to the toolbar
        open_icon = QIcon.fromTheme("document-open")
        open_action = QAction(open_icon, 'Open', self)
        open_action.triggered.connect(self.openFile)
        self.toolbar.addAction(open_action)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)

        # Undo Action
        undo_icon = QIcon.fromTheme("edit-undo")
        undo_action = QAction(undo_icon, 'Undo', self)
        undo_action.triggered.connect(self.undo)
        self.toolbar.addAction(undo_action)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)

        # Redo Action
        redo_icon = QIcon.fromTheme("edit-redo")
        redo_action = QAction(redo_icon, 'Redo', self)
        redo_action.triggered.connect(self.redo)
        self.toolbar.addAction(redo_action)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)

        # Save Action
        save_icon = QIcon.fromTheme("document-save")
        save_action = QAction(save_icon, 'Save', self)
        save_action.triggered.connect(self.saveFile)
        self.toolbar.addAction(save_action)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)
        
        # Print Action
        print_icon = QIcon.fromTheme("document-print")
        print_action = QAction(print_icon, 'Print', self)
        print_action.triggered.connect(self.printing)
        self.toolbar.addAction(print_action)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)

        # Add Font Action to the toolbar
        font_icon = QIcon.fromTheme("preferences-desktop-font")  # This theme icon might not be available in all systems. If it's missing, you can replace it with another appropriate one or a custom icon.
        font_action = QAction(font_icon, 'Font', self)
        font_action.triggered.connect(self.font)
        self.toolbar.addAction(font_action)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)
        
        # Add Close or Exit Action to the toolbar
        close_icon = QIcon.fromTheme("application-exit")
        close_action = QAction(close_icon, 'Exit', self)
        close_action.triggered.connect(self.close)
        self.toolbar.addAction(close_action)
        self.toolbar.addSeparator()  # Add separator (space)
        self.toolbar.addSeparator()  # Add separator (space)

#File name label
        self.address = QLabel()

#File indicator
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.address = QLabel()
        self.result2=''
        self.address.setText(self.result2)      
        self.toolbar.addWidget(self.address)
  
#Set the central widget to the text editor
        self.setCentralWidget(self.metapad)
        
#Create a QMenuBar
        menubar = self.menuBar()
#Styling
        self.setStyleSheet("background-color: #434C5E; color: #FAFAFA; border: 1px solid #393F4B; border-radius: 6px; font-size: 14px; selection-background-color: #2B3345; padding: 6px; QToolBar QToolButton { background-color: #5E6977; color: #FFFFFF; border: 1px solid #505C6C; font-weight: 500; padding: 4px; margin: 3px; min-width: 18px; min-height: 18px; border-radius: 4px; box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1); transition: all 0.3s ease-in-out; } QToolBar QToolButton:hover { background-color: #697885; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15); } QMenu::item:selected { background-color: #5E6977; } QMenu::item:hover { background-color: #6C7684; }")
        self.metapad.setStyleSheet("QPlainTextEdit{background-color: #343D4C; color: #F5F5F5; border: 1px solid #2D3643; border-radius: 6px; font-size: 15px; selection-background-color: #404A58; padding: 6px;}")
                 
#Default font
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)        
      
##############################
#Change font on selected text
##############################
    def font(self):
        font, ok = QFontDialog.getFont(self.metapad.font(), self, 'Change font: Requires text to be selected as a starting position.')
        if ok:
            cursor = self.metapad.textCursor()
            format = QTextCharFormat()
            format.setFont(font)
            cursor.mergeCharFormat(format)
            # Update the editor with the new format
            self.metapad.setTextCursor(cursor)
####################
#Undo and Redo
####################
#Undo
    def undo(self):
        self.metapad.undo()
		
#Redo
    def redo(self):
        self.metapad.redo()

#####################################################
#Modified closed event to prevent accidental closing
#####################################################
    def closeEvent(self, event):
        buttonReply = QMessageBox.question(self.metapad, 'Quit now?', "All unsaved documents will be lost. If unsure press Cancel now.", QMessageBox.Cancel | QMessageBox.Ok)
        
        if buttonReply == QMessageBox.Ok:
            print('Ok clicked, messagebox closed.')
            event.accept()  # accept the close event
            print ("\n")
            print ("Program ends. Goodbye.")
            print ("\n")    
        else:
            print ("Do not quit. --> Going back to the program.")
            event.ignore()  # ignore the close event to prevent the window from closing

########################
#Toolbar/ menu functions
########################
#Open & Save dialogs. Notice with all the dialogs that we use self.window - since our dialog needs to play nicely with our main window.
    def openFile(self):
        try:		    
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self.metapad,"Open a file", "","All Files (*);;Text Files (*.txt);;Python Files (*.py);;C++ Files (*.cpp);;Bash Files (*.sh);;Javascript Files (*.js);;Odt text files (*.odt)", options=options)
            url = QUrl.fromLocalFile(fileName)
            if fileName:
                buttonReply = QMessageBox.question(self.metapad, 'Open new file?', "All unsaved documents will be lost. If unsure press Cancel now.", QMessageBox.Cancel | QMessageBox.Ok  )
        
                if buttonReply == QMessageBox.Ok:
                    print('Ok clicked, messagebox closed. File opened.')
#Context manager way of handling files.                    
                    with open(fileName, 'r') as f: #Opening in read-mode with 'r'.
                        alltxt=f.read()
                        self.metapad.setPlainText(alltxt)                    
#Format filename location correctly.           
                    filename = QFileInfo(str(url)).fileName()
                    self.result1 = filename.replace(')', '')
                    self.result2 = self.result1	.replace("'", '')
                    print (self.result2)
                    self.address.setText('Now viewing: ' + self.result2)            
                if buttonReply == QMessageBox.Cancel:
                    print ("Will not proceed.")
                    pass 			
        except Exception as e:	 
            print("Cannot handle, Will not continue. Error.")
#Save file
    def saveFile(self):   
        try:		 
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self.metapad,"Save as","","All Files (*);;Text Files (*.txt);;Python Files (*.py);;C++ Files (*.cpp);;Bash Files (*.sh);;Javascript Files (*.js);;Odt text Files (*.odt)", options=options)
            if fileName:
                # Save the file contents to the chosen file name
                with open(fileName, 'w') as f:
                    f.write(self.metapad.toPlainText())
                # Now, update the address (filename label) to display the saved filename
                    filename = QFileInfo(fileName).fileName()
                    self.address.setText('Now viewing: ' + filename)
        except Exception as e:	 
            print("Cannot handle, Will not continue. Error.")
                         
#Printing the page
    def printing(self):
        preview = QPrintPreviewDialog()
# Print button is pressed within the print preview. Using Lambda here.
        preview.paintRequested.connect(lambda x: self.metapad.print_(x))
        preview.exec_() #We need to execute the Lambda.
        
#Exit/Quit program. This function binds to File->Exit. 
    def close(self):
        buttonReply = QMessageBox.question(self.metapad, 'Quit now?', "All unsaved documents will be lost. If unsure press Cancel now.", QMessageBox.Cancel | QMessageBox.Ok  )
        
        if buttonReply == QMessageBox.Ok:
            print('Ok clicked, messagebox closed.')
            app.quit()
            print ("\n")
            print ("Program ends. Goodbye.")
            print ("\n")    
        if buttonReply == QMessageBox.Cancel:
            print ("Do not quit. --> Going back to the program.")
            pass 
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.metapad.zoomIn(29) 
    sys.exit(app.exec_())
