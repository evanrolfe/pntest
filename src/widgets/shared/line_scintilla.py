import re
from PyQt6 import QtCore, QtWidgets, Qsci, QtGui

from widgets.shared.code_themes import DarkTheme
from widgets.shared.my_scintilla import MyScintilla

# Regular Expression for valid individual code 'words'
RE_VALID_WORD = re.compile(r"^\w+$")

class LineScintilla(MyScintilla):
    # TODO: Implement these signals
    enter_pressed = QtCore.pyqtSignal()
    text_changed = QtCore.pyqtSignal()

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
        self.apply_theme()

        self.focused = False

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
            self.enter_pressed.emit()
            # Disabled because we dont handle multiple lines here
            return
        else:
            old_text = self.text()
            super().keyPressEvent(e)
            new_text = self.text()

            if new_text != old_text:
                self.text_changed.emit()

    def apply_theme(self):
        self.bg_default = QtGui.QColor(self.theme.bg_input)
        self.bg_hover = QtGui.QColor(self.theme.bg_input_hover)
        self.bg_focus = QtGui.QColor(self.theme.bg_dark)

        self.setPaper(self.bg_default)
        self.setColor(QtGui.QColor(self.theme.default_color))
        self.setCaretForegroundColor(QtGui.QColor(self.theme.default_color))

        font = self.theme.get_font()
        self.setFont(font)

    # Hover
    def enterEvent(self, event):
        if not self.focused:
            self.setPaper(self.bg_hover)
        super(LineScintilla, self).enterEvent(event)

    # Un-Hover
    def leaveEvent(self, event):
        if not self.focused:
            self.setPaper(self.bg_default)
        super(LineScintilla, self).leaveEvent(event)

    def focusInEvent(self, event):
        self.focused = True
        self.setPaper(self.bg_focus)
        # Show the cursor:
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETCARETSTYLE, Qsci.QsciScintilla.CARETSTYLE_LINE)
        super(LineScintilla, self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.focused = False
        self.setPaper(self.bg_default)
        # Hide the cursor:
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETCARETSTYLE, Qsci.QsciScintilla.CARETSTYLE_INVISIBLE)
        super(LineScintilla, self).focusInEvent(event)

    # This is used by the URL input because its too big
    def centre_text_vertically(self):
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETEXTRAASCENT, 10)
