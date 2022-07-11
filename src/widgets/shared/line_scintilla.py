import re
from PyQt6 import QtCore, QtWidgets, Qsci, QtGui

# Regular Expression for valid individual code 'words'
RE_VALID_WORD = re.compile(r"^\w+$")

class DarkTheme:
    default_bg = "#1E1E1E"
    default_color = "#D4D4D4"
    key_color = "#823FF1"
    operator_color = "#569CD6"
    invalid_color = "#f14721"
    selected_secondary_color = "#4E5256"

    bg_dark = "#252526"
    border_color = "#404040"

class LineScintilla(Qsci.QsciScintilla):
    def __init__(self, *args, **kwargs):
        super(LineScintilla, self).__init__(*args, **kwargs)

        self.setUtf8(True)
        self.setAutoIndent(False)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setIndentationGuides(False)
        self.setBackspaceUnindents(True)
        self.setTabWidth(4)
        self.setEdgeColumn(79)
        self.setMarginLineNumbers(0, False)

        # Hide all margins:
        for i in range(5):
            self.setMarginWidth(i, 0)

        self.setBraceMatching(Qsci.QsciScintilla.BraceMatch.SloppyBraceMatch)

        self.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETVSCROLLBAR, 0)

        self.setIndicatorDrawUnder(True)

        self.theme = DarkTheme
        self.set_colours()

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
        elif 'Return' in key_name:
            # Disabled because we dont handle multiple lines here
            return
        else:
            super().keyPressEvent(e)

    def get_font(self) -> QtGui.QFont:
        # fonts = QtGui.QFontDatabase.families()
        # TODO: Search through the fonts and find one that matches
        font = QtGui.QFontDatabase.font('Menlo', 'Regular', 12)
        return font

    def set_colours(self):
        self.setPaper(QtGui.QColor(self.theme.bg_dark))
        self.setColor(QtGui.QColor(self.theme.default_color))
        self.setCaretForegroundColor(QtGui.QColor(self.theme.default_color))
