from PyQt6 import QtCore
from pytestqt.qtbot import QtBot
from entities.http_flow import HttpFlow
from repos.editor_item_repo import EditorItemRepo
from services.http_flow_service import HttpFlowService
from support.fixtures import load_fixtures
from entities.editor_item import EditorItem
from entities.payload_file import PayloadFile
from widgets.editor.fuzz_edit_page import FuzzEditPage

class TestFuzzEditPage:
    def test_saving_a_fuzz_request(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        editor_item = EditorItem(name = 'New Fuzz Request', item_type = EditorItem.TYPE_FUZZ)
        editor_item.build_blank_http_flow()
        EditorItemRepo().save(editor_item)

        widget = FuzzEditPage(editor_item)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Enter form data
        widget.ui.urlInput.setText("http://www.synack.com/login.php?username=${payload:usernames}&password=${payload:passwords}")

        # Set the payloads via the table model because QtBot is rubbish
        payload_usernames = PayloadFile('./test/support/usernames.txt', 'usernames')
        payload_passwords = PayloadFile('./test/support/passwords.txt', 'passwords')

        payload_usernames.verify_file()
        payload_passwords.verify_file()

        model = widget.ui.fuzzView.table_model
        model.insert_payload(payload_usernames)
        model.insert_payload(payload_passwords)

        # Click save button
        button = widget.ui.saveButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        assert editor_item.item is not None
        http_flows = HttpFlowService().find_by_ids([editor_item.item.id])
        assert len(http_flows) == 1
        http_flow = http_flows[0]

        assert http_flow.type == 'editor_fuzz'
        assert http_flow.request is not None
        assert http_flow.request.form_data['fuzz_data'] is not None
        assert http_flow.request.form_data['url'] == 'http://www.synack.com/login.php?username=${payload:usernames}&password=${payload:passwords}'
        assert http_flow.request.form_data['fuzz_data']['payload_files'] == [
            {'file_path': './test/support/usernames.txt', 'key': 'usernames', 'num_items': 2, 'description': ''},
            {'file_path': './test/support/passwords.txt', 'key': 'passwords', 'num_items': 2, 'description': ''}
        ]
        assert http_flow.request.form_data['fuzz_data']['fuzz_type'] == 'one_to_one'
        assert http_flow.request.form_data['fuzz_data']['delay_type'] == 'disabled'

    def test_modifying_a_payload_in_fuzz_request(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        editor_item = EditorItem(name = 'New Fuzz Request', item_type = EditorItem.TYPE_FUZZ)
        editor_item.build_blank_http_flow()
        EditorItemRepo().save(editor_item)

        widget = FuzzEditPage(editor_item)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Enter form data
        widget.ui.urlInput.setText("http://www.synack.com/login.php?username=${payload:usernames}&password=${payload:passwords}")

        # Set the payloads via the table model because QtBot is rubbish
        payload_usernames = PayloadFile('./test/support/usernames.txt', 'usernames')
        payload_passwords = PayloadFile('./test/support/passwords.txt', 'passwords')

        payload_usernames.verify_file()
        payload_passwords.verify_file()

        model = widget.ui.fuzzView.table_model
        model.insert_payload(payload_usernames)
        model.insert_payload(payload_passwords)

        # 1. First try inserting the payloads that were just added
        my_scintilla = widget.ui.fuzzView.ui.requestBody.ui.code
        qtbot.keyClick(my_scintilla, "$")
        qtbot.keyClick(my_scintilla, "{", QtCore.Qt.KeyboardModifier.ShiftModifier)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Enter)

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # qtbot.wait(3000)

        assert my_scintilla.text() == '${payload:usernames}'

        # Clear the text:
        my_scintilla.setText("")

        # 2. Modfiy the key of one of the payloads and try inserting again
        # Click the fuzz payloads tab
        tabs = widget.ui.fuzzView.ui.requestTabs
        tabs.setCurrentIndex(2)

        # Change the key of the first payload via the payloads table:
        table = widget.ui.fuzzView.ui.payloadsTable
        self.set_data_at(table, 0, 0, "newUsernames")

        # Go back to request body tab and start typing to insert a payload
        tabs.setCurrentIndex(1)
        qtbot.keyClick(my_scintilla, "$")
        qtbot.keyClick(my_scintilla, "{", QtCore.Qt.KeyboardModifier.ShiftModifier)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Down)
        qtbot.keyClick(my_scintilla, QtCore.Qt.Key.Key_Enter)

        assert my_scintilla.text() == '${payload:newUsernames}'

    def set_data_at(self, table, row: int, column: int, value: str):
        index = table.model().index(row, column)
        return table.model().setData(index, value, QtCore.Qt.ItemDataRole.EditRole)
