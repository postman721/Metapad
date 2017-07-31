# -*- coding: utf-8 -*-
#Metapad v.1 Copyright (c) 2017 JJ Posti <techtimejourney.net> 
#This program comes with ABSOLUTELY NO WARRANTY; 
#for details see: http://www.gnu.org/copyleft/gpl.html. 
#This is free software, and you are welcome to redistribute it under 
#GPL Version 2, June 1991")
#!/usr/bin/env python

#Importing modules. To make it easier we use * in some occasions to speed things up.
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *  
from PyQt5.QtGui import *  
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter
import subprocess, os, sys
#Loading unicode like this may lead to potential problems. Use only if needed.
reload(sys)
sys.setdefaultencoding('utf8')
######
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):

#This section defines MainWindow properties.
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setMouseTracking(True)
        MainWindow.setStyleSheet(_fromUtf8("QMainWindow{\n"
"background-color:#1b1a1a;\n"
"color:green;\n"
"}"))
        MainWindow.setDocumentMode(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
#################################################
#We create a grid and add our objects into it.        
#Note that our objects have CSS styling in them: background-color & color values.
#We also set textEdit to become a central widget. We want textEdit to be in the center of things
#since it is the most important thing we have. 
#We instruct our main window with: self.textEdit = QTextEdit(self.centralwidget) --> we wrap textEdit inside centralwidget.
 
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setStyleSheet(_fromUtf8("QTextEdit{\n"
"background-color:#1b1a1a;\n"
"color:green;\n"
"}"))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        
#Menubar comes first and inside menubar there can be menus like "File".        
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menuBar.setStyleSheet(_fromUtf8("QMenuBar{\n"
"background-color:#1b1a1a;\n"
"color:green;}"))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QMenu(self.menuBar) #File menu is placed within menubar here.
        self.menuFile.setStyleSheet(_fromUtf8("QMenu{\n"
"color:green;\n"
"}"))

############File Menu defintions begin        
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menuBar) #Notify MainWindow about menuBar.
        
#Open File        
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpen.triggered.connect(self.openFile)

#Save file        
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave.triggered.connect(self.saveFile)
       
#Printing        
        self.actionPrint = QAction(MainWindow)
        self.actionPrint.setObjectName(_fromUtf8("actionPrint"))
        self.actionPrint.triggered.connect(self.printing)
#About        
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAbout.triggered.connect(self.about)

#Exit
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionExit.triggered.connect(self.quitting)

#Add actions to file menu        
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction()) #Add file menu actions to menubar        
#################################################
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

#Exit/Quit program. This function only binds to File->Exit. This does not work for Alt+F4 or Esc keys, which are subclassed.
    def quitting(self):
        buttonReply = QMessageBox.question(self.window, 'Quit now?', "All unsaved documents will be lost. If unsure press Cancel now.", QMessageBox.Cancel | QMessageBox.Ok  )
        
        if buttonReply == QMessageBox.Ok:
            print('Ok clicked, messagebox closed.')
            app.quit()
            print "\n"
            print "Program ends. Goodbye."
            print "\n"    
        if buttonReply == QMessageBox.Cancel:
            print "Do not quit. --> Going back to the program."
            pass
        
#About box
    def about(self):
        buttonReply = QMessageBox.question(self.window, 'Metapad Copyright (c) 2017 JJ Posti <techtimejourney.net> ', "Metapad is text-editor made with Python and QT5. The program comes with ABSOLUTELY NO WARRANTY  for details see: http://www.gnu.org/copyleft/gpl.html. This is free software, and you are welcome to redistribute it under GPL Version 2, June 1991. Additional keys: Escape key launches the quit prompt.", QMessageBox.Ok )
        if buttonReply == QMessageBox.Ok:
            print('Ok clicked, messagebox closed.')

#Open & Save dialogs. Notice with all the dialogs that we use self.window - since our dialog needs to play nicely with our main window.
    def openFile(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.window,"Open a file", "","All Files (*);;Text Files (*.txt);;Python Files (*.py);;C++ Files (*.cpp);;Bash Files (*.sh);;Javascript Files (*.js);;Odt text files (*.odt)", options=options)
        if fileName:
            f=open(fileName, 'r') #Opening in read-mode with 'r'.
            alltxt=f.read()
            self.textEdit.setText(alltxt)
            f.close() #Need to close the file.
            
    def saveFile(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self.window,"Save as","","All Files (*);;Text Files (*.txt);;Python Files (*.py);;C++ Files (*.cpp);;Bash Files (*.sh);;Javascript Files (*.js);;Odt text Files (*.odt)", options=options)
        if fileName:
            f=open(fileName, 'w') #Opening in write-mode with 'w'.
            f.write(self.textEdit.toPlainText())
            f.close() #Need to close the file.
           
#Printing the page
    def printing(self):
        preview = QPrintPreviewDialog()
# Print button is pressed within the print preview. Using Lambda here.
        preview.paintRequested.connect(lambda x: self.textEdit.print_(x))
        preview.exec_() #We need to execute the Lambda.

#Designer related  "translations".
    def retranslateUi(self, MainWindow):
        self.window=MainWindow
        MainWindow.setWindowTitle(_translate("MainWindow", "Metapad", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionPrint.setText(_translate("MainWindow", "Print", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

class Extra(QMainWindow):
#Creating a subclass for keyPressEvents and closeEvents. 
#They cannot be in the same class as the ui stuff. If
#they were they would fail to get triggered(launched).

#Keypresses go below.    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.closeEvent(event) #Esc key launches Quit program prompt.

#Exit/Quit program prompt. This catches Alt+F4 and closing via X window controller. 
#Notice the event parameter and changes resulted from it.
    def closeEvent(self, event):
        buttonReply = QMessageBox.question(self, 'Quit now?', "All unsaved documents will be lost. If unsure press Cancel now.", QMessageBox.Cancel | QMessageBox.Ok  )
        
        if buttonReply == QMessageBox.Ok:
            print('Ok clicked, messagebox closed.')
            event.accept()
            app.quit()
            print "\n"
            print "Program ends. Goodbye."
            print "\n"    
        if buttonReply == QMessageBox.Cancel:
            print "Do not quit. --> Going back to the program."
            event.ignore() #This was pass in the quitting function.

#The mainloop that gives us a visible program when binding things together.
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = Extra()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
