import re
from PyQt6 import QtCore, QtWidgets, Qsci, QtGui

from views._compiled.shared.code_editor import Ui_CodeEditor

class CodeEditor(QtWidgets.QWidget):
    set_code = QtCore.pyqtSignal(str, str)

    FORMATS = ['JSON', 'XML', 'HTML', 'Javascript', 'Unformatted']

    def __init__(self, *args, **kwargs):
        super(CodeEditor, self).__init__(*args, **kwargs)
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)

        self.ui.code.setMarginType(0, Qsci.QsciScintilla.MarginType.NumberMargin)
        self.ui.code.setMarginWidth(0, "0000")

        keyseq_ctrl_f = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+F'), self)
        keyseq_ctrl_f.activated.connect(self.show_finder)

    def set_value(self, value, format = None):
        if format != None:
            if format not in self.FORMATS:
                raise Exception(f'Unknown format {format}')

            self.ui.code.set_format(format)

        self.ui.code.setText(value)

    def get_value(self) -> str:
        return self.ui.code.text()

    # NOTE: See mu/interface/main.py line 1280 (def replace_text) for an implementation of "replace all"
    def show_finder(self):
        case_sensitive = False

        self.ui.code.findFirst(
            "asdf",  # Text to find,
            False,  # Treat as regular expression
            case_sensitive,  # Case sensitive search
            True,  # Whole word matches only
            True,  # Wrap search
            forward=True,  # Forward search
            line=-1,  # From line: -1 starts at current position
            index=-1,  # From col: -1 starts at current position
            show=False,  # Unfolds found text
            posix=False,
        )  # More POSIX compatible RegEx

        self.ui.code.replaceSelectedText("somethingelse!")
