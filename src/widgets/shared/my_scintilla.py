import re
from PyQt6 import QtCore, QtWidgets, Qsci, QtGui

from widgets.shared.code_themes import DarkTheme

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

        self.search_indicators = {"selection": {"id": 21, "positions": []}}
        self.previous_selection = {
            "line_start": 0,
            "col_start": 0,
            "line_end": 0,
            "col_end": 0,
        }
        self.selectionChanged.connect(self.selection_changed)
        self.setIndicatorDrawUnder(True)

        self.theme = DarkTheme
        self.apply_theme()

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

    def selection_changed(self):
        # Get the current selection, exit if it has not changed
        line_from, index_from, line_to, index_to = self.getSelection()
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
        selected_range = line0, col0, line1, col1 = self.getSelection()

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
        selected_text = self.selectedText()
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
        pos0 = self.positionFromLineIndex(line0, col0)
        word_start_pos = self.SendScintilla(
            Qsci.QsciScintilla.SCI_WORDSTARTPOSITION, pos0, 1
        )
        _, start_offset = self.lineIndexFromPosition(word_start_pos)
        if col0 != start_offset:
            return

        pos1 = self.positionFromLineIndex(line1, col1)
        word_end_pos = self.SendScintilla(
            Qsci.QsciScintilla.SCI_WORDENDPOSITION, pos1, 1
        )
        _, end_offset = self.lineIndexFromPosition(word_end_pos)
        if col1 != end_offset:
            return

        #
        # For each matching word within the editor text, add it to
        # the list of highlighted indicators and fill it according
        # to the current theme.
        #
        indicators = self.search_indicators["selection"]
        encoding = "utf8" if self.isUtf8() else "latin1"
        text_bytes = self.text().encode(encoding)
        selected_text_bytes = selected_text.encode(encoding)

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

            self.fillIndicatorRange(
                line_start, col_start, line_end, col_end, indicators["id"]
            )

    def range_from_positions(self, start_position, end_position):
        """Given a start-end pair, such as are provided by a regex match,
        return the corresponding Scintilla line-offset pairs which are
        used for searches, indicators etc.

        NOTE: Arguments must be byte offsets into the underlying text bytes.
        """
        start_line, start_offset = self.lineIndexFromPosition(start_position)
        end_line, end_offset = self.lineIndexFromPosition(end_position)
        return start_line, start_offset, end_line, end_offset

    def reset_search_indicators(self):
        """
        Clears all the text indicators from the search functionality.
        """
        for indicator in self.search_indicators:
            for position in self.search_indicators[indicator]["positions"]:
                self.clearIndicatorRange(
                    position["line_start"],
                    position["col_start"],
                    position["line_end"],
                    position["col_end"],
                    self.search_indicators[indicator]["id"],
                )
            self.search_indicators[indicator]["positions"] = []

    def set_format(self, format: str):
        if format == 'JSON':
            lexer = self.theme.new_json_lexer()
            self.setLexer(lexer)
        elif format in ['XML', 'HTML']:
            lexer = self.theme.new_html_lexer()
            self.setLexer(lexer)
        elif format == 'Javascript':
            lexer = self.theme.new_js_lexer()
            self.setLexer(lexer)

    def apply_theme(self):
        self.setPaper(QtGui.QColor(self.theme.default_bg))
        self.setColor(QtGui.QColor(self.theme.default_color))
        self.setCaretForegroundColor(QtGui.QColor(self.theme.default_color))

        self.setMarginsBackgroundColor(QtGui.QColor(self.theme.default_bg))
        self.setMarginsForegroundColor(QtGui.QColor(self.theme.darker_color))

        self.setIndentationGuidesBackgroundColor(QtGui.QColor(self.theme.darker_color))

        for type_ in self.search_indicators:
            self.setMatchedBraceForegroundColor(QtGui.QColor(self.theme.default_color))
            self.setMatchedBraceBackgroundColor(QtGui.QColor(self.theme.selected_secondary_color))

            self.setIndicatorForegroundColor(QtGui.QColor(self.theme.selected_secondary_color), self.search_indicators[type_]["id"])
            self.setIndicatorHoverStyle(Qsci.QsciScintilla.IndicatorStyle.FullBoxIndicator, self.search_indicators[type_]["id"])

            # https://www.scintilla.org/ScintillaDoc.html#SCI_INDICSETSTYLE
            self.SendScintilla(
                Qsci.QsciScintilla.SCI_INDICSETSTYLE, self.search_indicators[type_]["id"], 16
            )
