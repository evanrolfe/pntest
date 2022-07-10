import re
from PyQt6 import QtCore, QtWidgets, Qsci, QtGui

from views._compiled.shared.code_editor import Ui_CodeEditor

start_text = """{
    "student": [
        {
            "id":"01",
            "name": "Tom",
            "lastname": "Price"
        },
        {
        "id":"02",
        "name": "Nick",
        "lastname": "Thameson"
        }
    ]
}"""

# Regular Expression for valid individual code 'words'
RE_VALID_WORD = re.compile(r"^\w+$")

class CodeEditor(QtWidgets.QWidget):
    set_code = QtCore.pyqtSignal(str, str)

    def __init__(self, *args, **kwargs):
        super(CodeEditor, self).__init__(*args, **kwargs)
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)

        self.ui.code.setMarginType(0, Qsci.QsciScintilla.MarginType.NumberMargin)
        self.ui.code.setMarginWidth(0, "0000")

        keyseq_ctrl_f = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+F'), self)
        keyseq_ctrl_f.activated.connect(self.show_finder)

        self.search_indicators = {"selection": {"id": 21, "positions": []}}
        self.previous_selection = {
            "line_start": 0,
            "col_start": 0,
            "line_end": 0,
            "col_end": 0,
        }
        self.ui.code.selectionChanged.connect(self.selection_changed)
        self.ui.code.setIndicatorDrawUnder(True)

        self.set_value(start_text)
        self.set_colours()

    def set_value(self, value, format=''):
        self.ui.code.setText(value)

    def get_value(self) -> str:
        return '' # self.ui.code.toPlainText()

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

    def selection_changed(self):
        # Get the current selection, exit if it has not changed
        line_from, index_from, line_to, index_to = self.ui.code.getSelection()
        if (
            self.previous_selection["col_end"] != index_to
            or self.previous_selection["col_start"] != index_from
            or self.previous_selection["line_start"] != line_from
            or self.previous_selection["line_end"] != line_to
        ):
            self.previous_selection["line_start"] = line_from
            self.previous_selection["col_start"] = index_from
            self.previous_selection["line_end"] = line_to
            self.previous_selection["col_end"] = index_to
            # Highlight matches
            self.reset_search_indicators()
            self.highlight_selected_matches()

    def highlight_selected_matches(self):
        """
        Checks the current selection, if it is a single word it then searches
        and highlights all matches.

        Since we're interested in exactly one word:
        * Ignore an empty selection
        * Ignore anything which spans more than one line
        * Ignore more than one word
        * Ignore anything less than one word
        """
        selected_range = line0, col0, line1, col1 = self.ui.code.getSelection()
        print(f'Selection changed {col0} {col1}')
        #
        # If there's no selection, do nothing
        #
        if selected_range == (-1, -1, -1, -1):
            return

        #
        # Ignore anything which spans two or more lines
        #
        if line0 != line1:
            return

        #
        # Ignore if no text is selected or the selected text is not at most one
        # valid identifier-type word.
        #
        selected_text = self.ui.code.selectedText()
        if not RE_VALID_WORD.match(selected_text):
            return

        #
        # Ignore anything which is not a whole word.
        # NB Although Scintilla defines a SCI_ISRANGEWORD message,
        # it's not exposed by QSciScintilla. Instead, we
        # ask Scintilla for the start end end position of
        # the word we're in and test whether our range end points match
        # those or not.
        #
        pos0 = self.ui.code.positionFromLineIndex(line0, col0)
        word_start_pos = self.ui.code.SendScintilla(
            Qsci.QsciScintilla.SCI_WORDSTARTPOSITION, pos0, 1
        )
        _, start_offset = self.ui.code.lineIndexFromPosition(word_start_pos)
        if col0 != start_offset:
            return

        pos1 = self.ui.code.positionFromLineIndex(line1, col1)
        word_end_pos = self.ui.code.SendScintilla(
            Qsci.QsciScintilla.SCI_WORDENDPOSITION, pos1, 1
        )
        _, end_offset = self.ui.code.lineIndexFromPosition(word_end_pos)
        if col1 != end_offset:
            return

        #
        # For each matching word within the editor text, add it to
        # the list of highlighted indicators and fill it according
        # to the current theme.
        #
        indicators = self.search_indicators["selection"]
        encoding = "utf8" if self.ui.code.isUtf8() else "latin1"
        text_bytes = self.ui.code.text().encode(encoding)
        selected_text_bytes = selected_text.encode(encoding)
        print(f'Selection changed --')
        for match in re.finditer(selected_text_bytes, text_bytes):
            range = self.range_from_positions(*match.span())

            #
            # Don't highlight the text we've selected
            #
            if range == selected_range:
                continue

            line_start, col_start, line_end, col_end = range
            indicators["positions"].append(
                {
                    "line_start": line_start,
                    "col_start": col_start,
                    "line_end": line_end,
                    "col_end": col_end,
                }
            )
            print(f'Calling fillIndicatorRange line_start: {line_start}, line_end: {line_end}, col_start: {col_start}, col_end: {col_end}, id: {indicators["id"]}')
            self.ui.code.fillIndicatorRange(
                line_start, col_start, line_end, col_end, indicators["id"]
            )

    def range_from_positions(self, start_position, end_position):
        """Given a start-end pair, such as are provided by a regex match,
        return the corresponding Scintilla line-offset pairs which are
        used for searches, indicators etc.

        NOTE: Arguments must be byte offsets into the underlying text bytes.
        """
        start_line, start_offset = self.ui.code.lineIndexFromPosition(start_position)
        end_line, end_offset = self.ui.code.lineIndexFromPosition(end_position)
        return start_line, start_offset, end_line, end_offset

    def reset_search_indicators(self):
        """
        Clears all the text indicators from the search functionality.
        """
        for indicator in self.search_indicators:
            for position in self.search_indicators[indicator]["positions"]:
                self.ui.code.clearIndicatorRange(
                    position["line_start"],
                    position["col_start"],
                    position["line_end"],
                    position["col_end"],
                    self.search_indicators[indicator]["id"],
                )
            self.search_indicators[indicator]["positions"] = []

    def set_colours(self):
        # fonts = QtGui.QFontDatabase.families()
        # TODO: Search through the fonts and find one that matches
        font = QtGui.QFontDatabase.font('Menlo', 'Regular', 12)

        default_bg = "#1E1E1E"
        default_color = "#D4D4D4"
        key_color = "#823FF1"
        operator_color = "#569CD6"
        invalid_color = "#f14721"
        selected_secondary_color = "#4E5256"

        self.ui.code.setMarginsBackgroundColor(QtGui.QColor(default_bg))
        self.ui.code.setMarginsForegroundColor(QtGui.QColor(default_color))
        self.ui.code.setCaretForegroundColor(QtGui.QColor(default_color))

        for type_ in self.search_indicators:
            self.ui.code.setIndicatorForegroundColor(QtGui.QColor(selected_secondary_color), self.search_indicators[type_]["id"])
            self.ui.code.setIndicatorHoverStyle(Qsci.QsciScintilla.IndicatorStyle.FullBoxIndicator, self.search_indicators[type_]["id"])

            # https://www.scintilla.org/ScintillaDoc.html#SCI_INDICSETSTYLE
            self.ui.code.SendScintilla(
                Qsci.QsciScintilla.SCI_INDICSETSTYLE, self.search_indicators[type_]["id"], 16
            )

        self.lexer = Qsci.QsciLexerJSON()

        self.lexer.setHighlightEscapeSequences(False)

        self.lexer.setDefaultPaper(QtGui.QColor(default_bg))
        self.lexer.setDefaultColor(QtGui.QColor(default_color))

        self.lexer.setPaper(QtGui.QColor(default_bg), Qsci.QsciLexerJSON.Error)
        self.lexer.setColor(QtGui.QColor(invalid_color), Qsci.QsciLexerJSON.Error)
        self.lexer.setPaper(QtGui.QColor(default_bg), Qsci.QsciLexerJSON.UnclosedString)
        self.lexer.setColor(QtGui.QColor(invalid_color), Qsci.QsciLexerJSON.UnclosedString)

        self.lexer.setColor(QtGui.QColor(key_color), Qsci.QsciLexerJSON.Property)
        self.lexer.setColor(QtGui.QColor(default_color), Qsci.QsciLexerJSON.String)
        self.lexer.setColor(QtGui.QColor(operator_color), Qsci.QsciLexerJSON.Operator)

        self.lexer.setColor(QtGui.QColor(invalid_color), Qsci.QsciLexerJSON.UnclosedString)

        self.lexer.setFont(font)
        self.ui.code.setLexer(self.lexer)
