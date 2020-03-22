# Metapad
Metapad is a text-editor written with Python and QT5. 

The text-editor contains about 204 lines of heavily commented code. Metapad is the default text-editor of PostX Gnu/Linux.

![metapad13](https://user-images.githubusercontent.com/29865797/61999894-dcc50c00-b0d3-11e9-98d7-78a558a01ca4.png)

#Metapad v.1.3 Copyright (c) 2017 JJ Posti <techtimejourney.net>
#This program comes with ABSOLUTELY NO WARRANTY;
#for details see: http://www.gnu.org/copyleft/gpl.html.
#This is free software, and you are welcome to redistribute it under
#GPL Version 2, June 1991″).

<b>Features</b>

Note.Metapad v.1.1 fixes Utf-8 support. In other words: there is only one version now.

-Open file. Filters include: All files, Text files, Python files, C++ files, Bash files, Javascript files, Odt text files.

-Save file, a.k.a. the save as functionality. Filters include: All files, Python files, C++ files, Bash files, Javascript files, Odt text files.

-Print functionality. Print also gives you an option to create a PDF out of your work with a print to a PDF file functionality.

-About window: Contains info.

-Exit functionalities with “Are you sure you want to quit?” dialog. Exit functionalities appear with: Pressing the escape key, with Alt+F4 combination or pressing the quit (x) button next to maximize.

Since 1.4: Zoom in and zoom out functionalities added to the menu.
____________________


<b>Dependencies</b>

python-pyqt5 or python3-pyqt5 or similar.

python or python3.

Usually you need to install only something pointing towards python-pyqt5 or python3-pyqt5. By default python/python3 should already be installed within your Linux system.

__________________________

<b>Notes</b>

Filters do not limit the file types you can use. Instead they give you a more filtered overview of your files. Filters do not add file type automatically. If you want to save as a txt file then do: somefile.txt as a file name. The default file type is plain text without an extension – unless the extension is specified.

Odt files can be opened and you can save to odt – if the file in question contains only text. At its current state Metapad does not support image loading/saving. I might add image functionalities in the future.

The style of Metapad is black and green oriented. The styling choices are CSS and as such they do not change the way the actual text appears on a paper or in a file. For example, if you save something it is going to be black, regular text in a white paper.

__________________________


<b>Executing</b>

If needed make python files executable: chmod +x filename.py

Run with: python filename_location.py

____
Original post is at: http://www.techtimejourney.net/metapad-text-editor-arrives/


