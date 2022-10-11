from optparse import Option
import re
from typing import Optional, TypedDict
from PyQt6 import QtCore, QtWidgets, Qsci, QtGui
from lib.input_parsing.transform_payload import TransformPayload
from models.http_flow import HttpFlow

from widgets.shared.code_themes import DarkTheme
from widgets.shared.encoders_popup import EncodersPopup
from widgets.shared.user_action import UserAction
from lib.input_parsing.parse import get_available_encoders
from lib.input_parsing.transformer import Transformer
from lib.input_parsing.text_tree import TreeNode
from lib.input_parsing.text_wrapper import TextWrapper, get_matches_for_indicators

from models.data.variable import Variable

# Regular Expression for valid individual code 'words'
RE_VALID_WORD = re.compile(r"^\w+$")

class Position(TypedDict):
    line: int
    col: int

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
    previous_cursor_position: Position
    user_action_in_progress: Optional[UserAction]

    flow: Optional[HttpFlow]

    escape_pressed = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MyScintilla, self).__init__(*args, **kwargs)

        self.setUtf8(True)
        self.setAutoIndent(True)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setIndentationGuides(True)
        self.setBackspaceUnindents(True)
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

        self.previous_cursor_position = { "line": 0, "col": 0 }
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
        self.encoders_popup.user_action_selected.connect(self.user_action_selected)
        self.encoders_popup.decode_selection.connect(self.decode_selection)

        self.indicatorReleased.connect(self.indicator_clicked)
        self.textChanged.connect(self.apply_encoding_indicators)

        # Set up auto-completion
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionCaseSensitivity(True)
        self.setAutoCompletionReplaceWord(True)
        self.setAutoCompletionSource(Qsci.QsciScintilla.AutoCompletionSource.AcsAPIs)

        # self.setAutoCompletionUseSingle(Qsci.QsciScintilla.AutoCompletionUseSingle.AcusExplicit)
        # https://www.scintilla.org/ScintillaDoc.html#SCN_AUTOCSELECTION
        self.SCN_AUTOCSELECTION.connect(self.autocomplete_selection_chosen)
        self.SCN_AUTOCCOMPLETED.connect(self.autocomplete_selection_inserted)
        self.flow = None

    def set_flow(self, flow: HttpFlow):
        self.flow = flow

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        word = self.wordAtPoint(event.pos())
        line = self.lineAt(event.pos())

        if self.autocomplete_is_open():
            return

        if line >= 0 and word != "":
            # NOTE: This causes weird behaviour if this isn't the first occurance of the word
            # Try implementing it like this: https://stackoverflow.com/questions/39657924/how-to-show-dialogs-at-a-certain-position-inside-a-qscintilla-widget
            # https://www.scintilla.org/ScintillaDoc.html#SCI_CHARPOSITIONFROMPOINT
            index = self.text(line).find(word)
            position = self.positionFromLineIndex(line, index)
            node = self.get_tree_node(line, index)

            if node:
                if type(node.get_transformer()) is TransformPayload:
                    value = 'payload'
                else:
                    value = node.get_transformed_value() or ''

                call_tip_text = str.encode('Value: ' + value)
                self.SendScintilla(Qsci.QsciScintilla.SCI_CALLTIPSHOW, position, call_tip_text)
        else:
            self.SendScintilla(Qsci.QsciScintilla.SCI_CALLTIPCANCEL)

        super().mouseMoveEvent(event)

    # NOTE: This only works if you are already focused on the Scintilla, if you are focused somewhere
    # else, hover to get a calltip, then do alt-tab (or similar), the calltip will remain displayed
    def focusOutEvent(self, event: QtGui.QFocusEvent):
        self.SendScintilla(Qsci.QsciScintilla.SCI_CALLTIPCANCEL)
        super().focusOutEvent(event)

    def apply_encoding_indicators(self):
        self.reset_encoding_indicators()

        text = self.text()
        for match in get_matches_for_indicators(text):
            # Subtract 2 from start and add 1 to end because of the "${" and "}" chars
            range = self.range_from_positions(match.start_index - 2, match.end_index + 1)
            self.highlight_with_indicator(range, self.INDICATOR_ENCODING_ID)

    def get_tree_node(self, line: int, index: int) -> Optional[TreeNode]:
        position = self.positionFromLineIndex(line, index)

        # TODO: Memoise the tree so we dont keep calculating it everytime theres a click or cursor position change
        text_wrapper = TextWrapper(self.text(), {})
        return text_wrapper.find_node_containing_index(position)

    # def cursor_position_changed(self, line: int, index: int):
    #     prev_cur = self.previous_cursor_position

    #     if line == prev_cur["line"] and index == prev_cur["col"]:
    #         return

    #     prev_cur["line"] = line
    #     prev_cur["col"] = index

    #     position = self.positionFromLineIndex(line, index)

    #     text_wrapper = TextWrapper(self.text(), {})
    #     node = text_wrapper.find_node_containing_index(position)
    #     if node is None:
    #         return

    #     # If the cursor is right before the ${, or right after the }
    #     if position == node.start_index - 2 or position == node.end_index + 1:
    #         return

    #     print("We are here")
    #     # print("position ", position, " Node: ", node.sub_str, " Start_Index: ", node.start_index, " End_Index: ", node.end_index)
    #     self.setCursorPosition(0, 0)
    #     return

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
        elif key_name == "Shift+{":
            super().keyPressEvent(e)
            self.show_autocomplete_maybe()
        elif key_name == "Esc":
            super().keyPressEvent(e)
            self.escape_pressed.emit()
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
        lexer = None

        if format == 'JSON':
            lexer = self.theme.new_json_lexer()
            self.setLexer(lexer)
        elif format in ['XML', 'HTML']:
            lexer = self.theme.new_html_lexer()
            self.setLexer(lexer)
        elif format == 'Javascript':
            lexer = self.theme.new_js_lexer()
            self.setLexer(lexer)

        if lexer is None:
            return

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

        self.setCallTipsForegroundColor(QtGui.QColor(self.theme.default_color))
        self.setCallTipsBackgroundColor(QtGui.QColor(self.theme.bg_input))

    #===========================================================================
    # User Action triggers
    #===========================================================================
    def right_clicked(self, position: QtCore.QPoint):
        menu = self.createStandardContextMenu()

        if self.hasSelectedText():
            # Add Encode sub-menu
            encoding_menu = menu.addMenu("Encode")
            for encoder in get_available_encoders():
                encoding_menu.addAction(encoder.name, lambda encoder=encoder: self.insert_encoding(encoder))

            # Add Decode sub-menu
            decoding_menu = menu.addMenu("Decode")
            for encoder in get_available_encoders():
                # TODO: Make this work
                # TODO: This should skip the encoders popup and go straight to decoding it
                decoding_menu.addAction(encoder.name, lambda encoder=encoder: self.decode_selection(encoder))

            user_action = UserAction(UserAction.TRIGGER_RIGHT_CLICK)
            user_action.set_value_to_transform(self.selectedText())
            menu.addAction("Encode/Decode/Hash", lambda user_action=user_action: self.show_encoders_popup(user_action))
        else:
            user_action = UserAction(UserAction.TRIGGER_RIGHT_CLICK)
            menu.addAction("Insert Encoding/Decoding/Hash", lambda user_action=user_action: self.show_encoders_popup(user_action))
            menu.addAction("Insert Variable", lambda user_action=user_action: self.show_autocomplete_for_user_action(user_action))
            menu.addAction("Insert Payload", lambda: print("TODO!"))

        position = self.sender().mapToGlobal(position) # type: ignore
        menu.exec(position)

    def indicator_clicked(self, line: int, index: int, keys: QtCore.Qt.KeyboardModifier):
        node = self.get_tree_node(line, index)
        if node is None:
            return

        transformer = node.get_transformer()
        if transformer is None:
            return

        if transformer.type in [Transformer.TYPE_ENCODER, Transformer.TYPE_DECODER, Transformer.TYPE_HASHER]:
            user_action = UserAction(UserAction.TRIGGER_INDICATOR_CLICK, node)
            self.show_encoders_popup(user_action)
        else:
            user_action = UserAction(UserAction.TRIGGER_INDICATOR_CLICK, node)
            self.show_autocomplete_for_user_action(user_action)

    #===========================================================================
    # User Action options
    #===========================================================================
    def show_encoders_popup(self, user_action: UserAction):
        self.encoders_popup.clear_all()
        self.encoders_popup.set_user_action(user_action)

        # Decoding results in a raw value, so you cannot decode a node
        self.encoders_popup.set_decoders_visible(user_action.node is None)

        if user_action.node is not None:
            self.encoders_popup.set_tree_node(user_action.node)
            self.encoders_popup.set_transformer(user_action.node.get_transformer()) # type: ignore
            self.encoders_popup.set_input(user_action.node.get_value()) # type: ignore

        self.encoders_popup.show()

    def show_autocomplete(self):
        vars = Variable.all_global()
        options = ["var:"+v.key for v in vars]
        options.append("encoding")

        if self.flow is not None and self.flow.has_request():
            request = self.flow.request
            if request is not None:
                payload_options = ["payload:"+k for k in request.payload_keys()]
                options.extend(payload_options)

        self.SendScintilla(Qsci.QsciScintilla.SCI_AUTOCSHOW, str.encode(' '.join(options)))

    def show_autocomplete_for_user_action(self, user_action: UserAction):
        self.user_action_in_progress = user_action
        self.show_autocomplete()
        return

    # This is called when the { key is pressed
    def show_autocomplete_maybe(self):
        text = self.text()
        pos = self.SendScintilla(Qsci.QsciScintilla.SCI_GETCURRENTPOS)
        if text[pos-2:pos] == "${":
            user_action = UserAction(UserAction.TRIGGER_TEXT)
            self.show_autocomplete_for_user_action(user_action)

    #===========================================================================
    # User Action outcomes
    #===========================================================================
    def user_action_selected(self, user_action: UserAction):
        print("User action selected! ", user_action)
        if user_action.transformer is None:
            raise Exception("no transformer has been selected")

        # Insert
        if user_action.node is None:
            self.insert_encoding(user_action.transformer, user_action.value_to_transform)

        # Update existing node
        else:
            self.update_encoding(user_action.transformer, user_action.node, user_action.value_to_transform)

    # TODO: Maybe this should accept a UserAction instead of primitives?
    def insert_encoding(self, encoder: Transformer, text_to_encode: Optional[str] = None):
        if text_to_encode is None:
            text_to_encode = self.selectedText()

        encoded_text = "${" + encoder.key + ":" + text_to_encode + "}"

        # If this is an insert
        if self.selectedText() == "":
            # If the previous two characters are ${ then this was probably triggered by the autocomplete
            # so dont add another ${ on top of that
            line, col = self.getCursorPosition()
            position = self.positionFromLineIndex(line, col)
            last_two_chars = self.text()[position-2:position]

            if last_two_chars == "${":
                encoded_text = encoder.key + ":" + text_to_encode + "}"

        self.replaceSelectedText(encoded_text)

    def update_encoding(self, encoder: Transformer, node: TreeNode, text_to_encode: str):
        encoded_text = encoder.key + ":" + text_to_encode
        text = self.text()
        new_text = self.delete_range_from_string(text, node.start_index, node.end_index)
        self.setText(new_text)

        line_num, line_index = self.lineIndexFromPosition(node.start_index)
        self.insertAt(encoded_text, line_num, line_index)

        return

    def autocomplete_selection_chosen(self, selection: bytes, position: int, ch: int, method: int):
        selection_str = selection.decode("utf-8")

        if self.user_action_in_progress is None:
            raise Exception("autocomplete has been showed without the user_action_in_progress being set")

        # Encodings:
        if selection_str == "encoding":
            self.autocomplete_cancel()
            self.show_encoders_popup(self.user_action_in_progress)
            return

        # Variables:
        # If the autocomplete was triggered by a right click, then there will be no preceeding "${"
        # so we need to insert it
        if self.user_action_in_progress.trigger == UserAction.TRIGGER_RIGHT_CLICK and self.user_action_in_progress.node is None:
            self.autocomplete_cancel()
            selection_to_insert = "${"+selection_str + "}"

            line_num, line_index = self.lineIndexFromPosition(position)
            self.insertAt(selection_to_insert, line_num, line_index)
            self.setCursorPosition(line_num, line_index+len(selection_to_insert))
            return

        if self.user_action_in_progress.node:
            self.autocomplete_cancel()
            node = self.user_action_in_progress.node
            text = self.text()
            new_text = self.delete_range_from_string(text, node.start_index, node.end_index)
            self.setText(new_text)

            line_num, line_index = self.lineIndexFromPosition(node.start_index)
            self.insertAt(selection_str, line_num, line_index)

    #===========================================================================

    def decode_selection(self, encoder: Transformer, text_to_decode: Optional[str] = None):
        if text_to_decode is None:
            text_to_decode = self.selectedText()

        self.replaceSelectedText(encoder.decode(text_to_decode))

    def delete_range_from_string(self, value: str, start_index: int, end_index: int) -> str:
        return value[0:start_index] + value[end_index:]

    def autocomplete_selection_inserted(self, selection: bytes, position: int, ch: int, method: int):
        # Insert the closing }
        line, col = self.getCursorPosition()
        self.insertAt("}", line, col)
        self.setCursorPosition(line, col+1)

    def autocomplete_is_open(self):
        return self.SendScintilla(Qsci.QsciScintilla.SCI_AUTOCACTIVE)

    def autocomplete_cancel(self):
        self.SendScintilla(Qsci.QsciScintilla.SCI_AUTOCCANCEL)
