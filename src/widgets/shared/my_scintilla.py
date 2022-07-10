import re
from PyQt6 import QtCore, QtWidgets, Qsci, QtGui

# Regular Expression for valid individual code 'words'
RE_VALID_WORD = re.compile(r"^\w+$")

class MyScintilla(Qsci.QsciScintilla):
    def __init__(self, *args, **kwargs):
        super(MyScintilla, self).__init__(*args, **kwargs)

        self.setUtf8(True)
        self.setAutoIndent(True)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setIndentationGuides(True)
        self.setBackspaceUnindents(True)
        self.setTabWidth(4)
        self.setEdgeColumn(79)
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, 50)
        self.setBraceMatching(Qsci.QsciScintilla.BraceMatch.SloppyBraceMatch)
        # self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)


    # This is necessary for mac os x
    # More info see: https://www.scintilla.org/ScintillaDoc.html#keyDefinition
    def keyPressEvent(self, e: QtGui.QKeyEvent):
        key_name = QtGui.QKeySequence(e.keyCombination()).toString()

        if key_name == 'Home':
            self.SendScintilla(Qsci.QsciScintilla.SCI_VCHOME)

        elif key_name == 'Shift+Home':
            end_pos = self.SendScintilla(Qsci.QsciScintilla.SCI_GETCURRENTPOS)
            self.SendScintilla(Qsci.QsciScintilla.SCI_VCHOME)
            start_pos = self.SendScintilla(Qsci.QsciScintilla.SCI_GETCURRENTPOS)

            self.SendScintilla(Qsci.QsciScintilla.SCI_SETSELECTIONSTART, start_pos)
            self.SendScintilla(Qsci.QsciScintilla.SCI_SETSELECTIONEND, end_pos)

        elif key_name == 'End':
            self.SendScintilla(Qsci.QsciScintilla.SCI_LINEEND)

        elif key_name == 'Shift+End':
            start_pos = self.SendScintilla(Qsci.QsciScintilla.SCI_GETCURRENTPOS)
            self.SendScintilla(Qsci.QsciScintilla.SCI_LINEEND)
            end_pos = self.SendScintilla(Qsci.QsciScintilla.SCI_GETCURRENTPOS)

            self.SendScintilla(Qsci.QsciScintilla.SCI_SETSELECTIONSTART, start_pos)
            self.SendScintilla(Qsci.QsciScintilla.SCI_SETSELECTIONEND, end_pos)
        else:
            super().keyPressEvent(e)
