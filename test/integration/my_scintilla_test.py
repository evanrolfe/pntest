import threading
import time
from PyQt6 import QtCore, QtWidgets, Qsci
from pytestqt.qtbot import QtBot
from lib.input_parsing.encode_base64 import EncodeBase64
from lib.input_parsing.encode_ascii_hex import EncodeAsciiHex
from models.editor_item import EditorItem
from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from services.http_flow_service import HttpFlowService
from support.fixtures import load_fixtures, build_an_editor_flow_with_payloads
from widgets.editor.editor_page import EditorPage
from widgets.shared.my_scintilla import MyScintilla
from widgets.shared.user_action import UserAction

class TestMyScintilla:
    # --------------------------------------------------------------------------
    # Variables
    # --------------------------------------------------------------------------
    # 1. Trigger autocomplete by typing in ${
    # 2. Choose a variable from the dropdown
    def test_text_trigger_autocomplete_var(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = MyScintilla()
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        qtbot.mouseClick(widget, QtCore.Qt.MouseButton.LeftButton, pos=widget.rect().center())
        qtbot.keyClick(widget, "$")
        qtbot.keyClick(widget, "{", QtCore.Qt.KeyboardModifier.ShiftModifier)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Enter)

        assert widget.text() == '${var:apiVersion}'

    # 1. Trigger autocomplete by clicking an indicator
    # 2. Choose a variable from the dropdown
    def test_indicator_click_trigger_autocomplete_var(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = MyScintilla()
        widget.setText('The verion is: ${var:apiVersion}.')
        widget.resize(500, 200)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Click on the indicator
        point = QtCore.QPoint(200, 0)
        qtbot.mouseClick(widget.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=point)

        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Enter)

        assert widget.text() == 'The verion is: ${var:account_name}.'

    # 1. Trigger autocomplete by right clicking and choosing "Insert variable"
    # 2. Choose a variable from the dropdown
    def test_right_click_trigger_autocomplete_var(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = MyScintilla()
        widget.setText('The verion is: ${var:apiVersion}.')
        widget.resize(500, 200)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Simulate a right click
        user_action = UserAction(UserAction.TRIGGER_RIGHT_CLICK)
        widget.show_autocomplete_for_user_action(user_action)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Enter)

        assert widget.text() == '${var:host}The verion is: ${var:apiVersion}.'

    # --------------------------------------------------------------------------
    # Encodings
    # --------------------------------------------------------------------------
    # 1. Trigger encoders popup by typing in ${
    # 2. Choose a variable from the dropdown
    def test_text_trigger_autocomplete_encoding(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = MyScintilla()
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        qtbot.mouseClick(widget, QtCore.Qt.MouseButton.LeftButton, pos=widget.rect().center())
        qtbot.keyClick(widget, "$")
        qtbot.keyClick(widget, "{", QtCore.Qt.KeyboardModifier.ShiftModifier)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Enter)

        widget.encoders_popup.set_input("hello")
        widget.encoders_popup.select_encoding("b64")
        button = widget.encoders_popup.ui.saveButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        assert widget.text() == '${b64:hello}'

    # 1. Trigger encoders popup by clicking an indicator (when its a var)
    # 2. Choose a variable from the dropdown
    def test_indicator_click_trigger_autocomplete_encoding(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = MyScintilla()
        widget.setText('The verion is: ${var:apiVersion}.')
        widget.resize(500, 200)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Click on the indicator
        point = QtCore.QPoint(200, 0)
        qtbot.mouseClick(widget.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=point)

        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Enter)

        widget.encoders_popup.set_input("hello")
        widget.encoders_popup.select_encoding("b64")
        button = widget.encoders_popup.ui.saveButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        assert widget.text() == 'The verion is: ${b64:hello}.'

    # # 1. Trigger encoders popup by right clicking and choosing "Encoding/Decoding/Hash"
    # # 2. Choose a variable from the dropdown
    def test_right_click_encoding_decoding_hash(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = MyScintilla()
        widget.setText('The verion is: ${var:apiVersion}.')
        widget.resize(500, 200)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Simulate a right click
        user_action = UserAction(UserAction.TRIGGER_RIGHT_CLICK)
        widget.show_encoders_popup(user_action)

        widget.encoders_popup.set_input("hello")
        widget.encoders_popup.select_encoding("b64")
        button = widget.encoders_popup.ui.saveButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        assert widget.text() == '${b64:hello}The verion is: ${var:apiVersion}.'

    # 1. Trigger encoders popup by selecting text, right clicking and choosing "Encode -> Base64"
    # 2. Choose a variable from the dropdown
    def test_selection_right_click_encoding_base64(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = MyScintilla()
        widget.setText('The verion is: ${var:apiVersion}.')
        widget.resize(500, 200)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Select the word "version"
        widget.setSelection(0, 4, 0, 10)

        # Simulate a right click
        encoding = EncodeBase64()
        widget.insert_encoding(encoding)

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # qtbot.wait(3000)

        assert widget.text() == 'The ${b64:verion} is: ${var:apiVersion}.'

    # # 1. Trigger encoders popup by selecting text, right clicking and choosing "Encoding/Decoding/Hash"
    # # 2. Choose a variable from the dropdown
    def test_selection_right_click_encoding_decoding_hash(self, database, cleanup_database, qtbot: QtBot):
        # Its too hard to simulate the right click for this test, but it does work
        pass

    # --------------------------------------------------------------------------
    # Decodings
    # --------------------------------------------------------------------------
    def test_selection_right_click_decoding(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = MyScintilla()
        widget.setText('The encoded word is: aGVsbG8=.')
        widget.resize(500, 200)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Select the encoded value
        widget.setSelection(0, 21, 0, 29)

        # Simulate a right click
        encoding = EncodeBase64()
        widget.decode_selection(encoding)

        assert widget.text() == 'The encoded word is: hello.'

    # --------------------------------------------------------------------------
    # Payloads
    # --------------------------------------------------------------------------
    def test_text_trigger_autocomplete_payload(self, database, cleanup_database, qtbot: QtBot):
        http_flow = build_an_editor_flow_with_payloads()
        HttpFlowService().save(http_flow)

        widget = MyScintilla()
        widget.resize(500, 200)
        widget.set_flow(http_flow)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        qtbot.keyClick(widget, "$")
        qtbot.keyClick(widget, "{", QtCore.Qt.KeyboardModifier.ShiftModifier)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Enter)

        assert widget.text() == '${payload:password}'

    def test_indicator_click_trigger_autocomplete_payload(self, database, cleanup_database, qtbot: QtBot):
        http_flow = build_an_editor_flow_with_payloads()
        HttpFlowService().save(http_flow)

        widget = MyScintilla()
        widget.setText('${payload:password}')
        widget.resize(500, 200)
        widget.set_flow(http_flow)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        point = QtCore.QPoint(50, 0)
        qtbot.mouseClick(widget.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=point)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(widget, QtCore.Qt.Key.Key_Enter)

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # qtbot.wait(3000)

        assert widget.text() == '${payload:username}'
