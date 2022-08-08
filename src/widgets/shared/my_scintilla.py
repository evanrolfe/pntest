from optparse import Option
import re
from typing import Optional, TypedDict
from PyQt6 import QtCore, QtWidgets, Qsci, QtGui
from lib.input_parsing.text_wrapper import get_matches_for_indicators

from widgets.shared.code_themes import DarkTheme
from widgets.shared.encoders_popup import EncodersPopup
from lib.input_parsing.parse import get_available_encoders
from lib.input_parsing.encoder import Encoder

# Regular Expression for valid individual code 'words'
RE_VALID_WORD = re.compile(r"^\w+$")

class IndicatorRange(TypedDict):
    line_start: int
    col_start: int
    line_end: int
    col_end: int

class IndicatorRecord(TypedDict):
    ranges: list[IndicatorRange]

class MyScintilla(Qsci.QsciScintilla):
    INDICATOR_ENCODING_ID = 1
    INDICATOR_SEARCH_ID = 2

    previous_selection: IndicatorRange
    indicators: dict[int, IndicatorRecord]

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

        # Right click behaviour
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_clicked)

        self.indicators = {}
        self.indicators[self.INDICATOR_ENCODING_ID] = { "ranges": [] }
        self.indicators[self.INDICATOR_SEARCH_ID] = { "ranges": [] }

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

        self.encoders_popup = EncodersPopup(self)
        self.encoders_popup.encode.connect(self.encode_selection)
        self.encoders_popup.decode.connect(self.decode_selection)

        self.indicatorReleased.connect(self.indicator_clicked)
        self.textChanged.connect(self.apply_encoding_indicators)

    def apply_encoding_indicators(self):
        self.reset_encoding_indicators()

        text = self.text()
        for match in get_matches_for_indicators(text):
            # Subtract 2 from start and add 1 to end because of the "${" and "}" chars
            range = self.range_from_positions(match.start_index - 2, match.end_index + 1)
            self.highlight_with_indicator(range, self.INDICATOR_ENCODING_ID)

    def indicator_clicked(self, line: int, index: int, keys: QtCore.Qt.KeyboardModifier):
        print("line: ", line, ", index: ", index, ", keys: ", keys)
        # TODO: Get the value of the encoding and set it on the EncoderPopup
        self.encoders_popup.show()

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

    # Checks the current selection, if it is a single word it then searches and highlights all matches.
    # Since we're interested in exactly one word:
    # * Ignore an empty selection
    # * Ignore anything which spans more than one line
    # * Ignore more than one word
    # * Ignore anything less than one word
    def highlight_selected_matches(self):
        selected_range = line0, col0, line1, col1 = self.getSelection()

        if selected_range == (-1, -1, -1, -1): # If there's no selection, do nothing
            return

        if line0 != line1: # Ignore anything which spans two or more lines
            return

        # Ignore if no text is selected or the selected text is not at most one valid identifier-type word.
        selected_text = self.selectedText()
        if not RE_VALID_WORD.match(selected_text):
            return

        # Ignore anything which is not a whole word.
        pos0 = self.positionFromLineIndex(line0, col0)
        word_start_pos = self.SendScintilla(Qsci.QsciScintilla.SCI_WORDSTARTPOSITION, pos0, 1)
        _, start_offset = self.lineIndexFromPosition(word_start_pos)
        if col0 != start_offset:
            return

        pos1 = self.positionFromLineIndex(line1, col1)
        word_end_pos = self.SendScintilla(Qsci.QsciScintilla.SCI_WORDENDPOSITION, pos1, 1)
        _, end_offset = self.lineIndexFromPosition(word_end_pos)
        if col1 != end_offset:
            return

        # Add each matching word to the list of highlighted indicators and highlight it
        encoding = "utf8" if self.isUtf8() else "latin1"
        text_bytes = self.text().encode(encoding)
        selected_text_bytes = selected_text.encode(encoding)

        for match in re.finditer(selected_text_bytes, text_bytes):
            range = self.range_from_positions(*match.span())

            # Don't highlight the text we've selected
            if range == selected_range:
                continue

            self.highlight_with_indicator(range, self.INDICATOR_SEARCH_ID)

    def highlight_with_indicator(self, range: IndicatorRange, indicator_id: int):
        indicator = self.indicators[indicator_id]
        indicator["ranges"].append(range)
        self.fillIndicatorRange(
            range["line_start"],
            range["col_start"],
            range["line_end"],
            range["col_end"],
            indicator_id
        )

    # Given a start-end pair, such as are provided by a regex match,
    # return the corresponding Scintilla line-offset pairs which are
    # used for searches, indicators etc.
    # NOTE: Arguments must be byte offsets into the underlying text bytes.
    def range_from_positions(self, start_position: int, end_position: int) -> IndicatorRange:
        start_line, start_offset = self.lineIndexFromPosition(start_position)
        end_line, end_offset = self.lineIndexFromPosition(end_position)
        return {
            "line_start": start_line,
            "col_start": start_offset,
            "line_end": end_line,
            "col_end": end_offset,
        }

    def reset_search_indicators(self):
        for range in self.indicators[self.INDICATOR_SEARCH_ID]["ranges"]:
            self.clearIndicatorRange(
                range["line_start"],
                range["col_start"],
                range["line_end"],
                range["col_end"],
                self.INDICATOR_SEARCH_ID,
            )
        self.indicators[self.INDICATOR_SEARCH_ID]["ranges"] = []

    def reset_encoding_indicators(self):
        for range in self.indicators[self.INDICATOR_ENCODING_ID]["ranges"]:
            self.clearIndicatorRange(
                range["line_start"],
                range["col_start"],
                range["line_end"],
                range["col_end"],
                self.INDICATOR_ENCODING_ID,
            )
        self.indicators[self.INDICATOR_ENCODING_ID]["ranges"] = []

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

        # Set Search Indicator Style
        self.setMatchedBraceForegroundColor(QtGui.QColor(self.theme.default_color))
        self.setMatchedBraceBackgroundColor(QtGui.QColor(self.theme.selected_secondary_color))

        self.setIndicatorForegroundColor(QtGui.QColor(self.theme.selected_secondary_color), self.INDICATOR_SEARCH_ID)
        self.setIndicatorHoverStyle(Qsci.QsciScintilla.IndicatorStyle.FullBoxIndicator, self.INDICATOR_SEARCH_ID)

        # https://www.scintilla.org/ScintillaDoc.html#SCI_INDICSETSTYLE
        self.SendScintilla(Qsci.QsciScintilla.SCI_INDICSETSTYLE, self.INDICATOR_SEARCH_ID, 16)

        font = self.theme.get_font()
        self.setFont(font)

        self.setIndicatorForegroundColor(QtGui.QColor("#1c90b4"), self.INDICATOR_ENCODING_ID)
        self.SendScintilla(Qsci.QsciScintilla.SCI_INDICSETSTYLE, self.INDICATOR_ENCODING_ID, 15)

        self.setIndicatorHoverForegroundColor(QtGui.QColor("#404040"), self.INDICATOR_ENCODING_ID)
        self.setIndicatorHoverStyle(Qsci.QsciScintilla.IndicatorStyle.FullBoxIndicator, self.INDICATOR_ENCODING_ID)

    def right_clicked(self, position: QtCore.QPoint):
        menu = self.createStandardContextMenu()

        # Add Encode sub-menu
        if self.hasSelectedText():
            encoding_menu = menu.addMenu("Encode")
            for encoder in get_available_encoders():
                encoding_menu.addAction(encoder.name, lambda encoder=encoder: self.encode_selection(encoder))

        # Add Decode sub-menu
        if self.hasSelectedText():
            decoding_menu = menu.addMenu("Decode")
            for encoder in get_available_encoders():
                decoding_menu.addAction(encoder.name, lambda encoder=encoder: self.decode_selection(encoder))

        menu.addAction("Encode/Decode/Hash", self.show_encoders_popup)

        position = self.sender().mapToGlobal(position) # type: ignore
        menu.exec(position)

    def encode_selection(self, encoder: Encoder, text_to_encode: Optional[str] = None):
        if text_to_encode is None:
            text_to_encode = self.selectedText()

        # TODO: Move this syntax to a function in lib.input_parsing.parse
        encoded_text = "${" + encoder.key + ":" + text_to_encode + "}"
        self.replaceSelectedText(encoded_text)

    def decode_selection(self, encoder: Encoder, text_to_decode: Optional[str] = None):
        if text_to_decode is None:
            text_to_decode = self.selectedText()

        self.replaceSelectedText(encoder.decode(text_to_decode))

    def show_encoders_popup(self):
        self.encoders_popup.set_input(self.selectedText())
        self.encoders_popup.show()
