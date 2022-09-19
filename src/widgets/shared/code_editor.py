import json
import re
from typing import Optional
from PyQt6 import QtCore, QtWidgets, Qsci, QtGui
from bs4 import BeautifulSoup
from models.data.http_flow import HttpFlow

from views._compiled.shared.code_editor import Ui_CodeEditor

# TODO: This class should be merged into MyScintilla
class CodeEditor(QtWidgets.QWidget):
    find_in_progress: Optional[str]
    selected_format: Optional[str]
    auto_format_enabled: bool

    set_code = QtCore.pyqtSignal(str, str)

    FORMATS = ['JSON', 'XML', 'HTML', 'Javascript', 'Unformatted']

    def __init__(self, *args, **kwargs):
        super(CodeEditor, self).__init__(*args, **kwargs)
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)

        self.ui.code.setMarginType(0, Qsci.QsciScintilla.MarginType.NumberMargin)
        self.ui.code.setMarginWidth(0, "0000")

        self.hide_find_replace()
        self.ui.findButton.clicked.connect(self.find)
        self.ui.findPrevButton.setVisible(False)
        self.ui.replaceButton.clicked.connect(self.replace)
        self.ui.replaceAllButton.clicked.connect(self.replace_all)

        keyseq_ctrl_f = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+F'), self)
        keyseq_ctrl_f.setContext(QtCore.Qt.ShortcutContext.WidgetWithChildrenShortcut)
        keyseq_ctrl_f.activated.connect(self.show_find_replace)

        keyseq_esc = QtGui.QShortcut(QtGui.QKeySequence('Escape'), self)
        keyseq_esc.setContext(QtCore.Qt.ShortcutContext.WidgetWithChildrenShortcut)
        keyseq_esc.activated.connect(self.hide_find_replace)
        self.ui.code.escape_pressed.connect(self.hide_find_replace)

        keyseq_enter = QtGui.QShortcut(QtGui.QKeySequence('Return'), self)
        keyseq_enter.setContext(QtCore.Qt.ShortcutContext.WidgetWithChildrenShortcut)
        keyseq_enter.activated.connect(self.find)

        self.selected_format = None
        self.auto_format_enabled = False
        self.find_in_progress = None

    def show_find_replace(self):
        self.ui.findReplace.setVisible(True)
        self.ui.findText.setFocus()

    def hide_find_replace(self):
        self.ui.code.cancelFind()
        self.find_in_progress = None
        self.ui.findReplace.setVisible(False)

    def find(self) -> bool:
        find_text = self.ui.findText.text()

        if self.find_in_progress == find_text:
            return self.ui.code.findNext()
        else:
            self.find_in_progress = find_text
            return self.ui.code.findFirst(
                find_text,  # Text to find,
                False,  # Treat as regular expression
                False,  # Case sensitive search
                True,  # Whole word matches only
                True,  # Wrap search
                True,  # Forward search
                line=-1,  # From line: -1 starts at current position
                index=-1,  # From col: -1 starts at current position
                show=False,  # Unfolds found text
                posix=False,
            )

    def replace(self):
        replace_text = self.ui.replaceText.text()
        found = self.find()
        if found:
            self.ui.code.replaceSelectedText(replace_text)

    def replace_all(self):
        replace_text = self.ui.replaceText.text()

        found = True
        while found == True:
            found = self.find()
            if found:
                self.ui.code.replaceSelectedText(replace_text)

    def set_format(self, format: str):
        if format not in self.FORMATS:
            raise Exception(f'Unknown format {format}')

        self.selected_format = format

    def set_flow(self, flow: HttpFlow):
        self.ui.code.set_flow(flow)

    def clear_formatting(self):
        self.selected_format = None

    def set_auto_format_enabled(self, value: bool):
        self.auto_format_enabled = value

    def set_value(self, value: str):
        if self.selected_format != None:
            self.ui.code.set_format(self.selected_format)

        if self.auto_format_enabled:
            try:
                value = self.format_text(value)
            except Exception as ex:
                print("[CodeEditor] formatting error: ", ex)

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

    def format_text(self, text: str) -> str:
        # TODO: Format javascript
        if self.selected_format == 'JSON':
            try:
                formatted_content = json.dumps(json.loads(text), indent=2)
            except json.decoder.JSONDecodeError:
                formatted_content = text
        elif self.selected_format == 'XML':
            formatted_content = BeautifulSoup(text, 'xml.parser').prettify()
        elif self.selected_format == 'HTML':
            formatted_content = BeautifulSoup(text, 'html.parser').prettify()
        else:
            formatted_content = text

        return formatted_content
