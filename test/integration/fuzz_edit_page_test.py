from PySide2 import QtCore
from models.data.http_flow import HttpFlow
from support.fixtures import load_fixtures
from models.data.editor_item import EditorItem
from models.data.payload_file import PayloadFile
from widgets.editor.fuzz_edit_page import FuzzEditPage

class TestFuzzEditPage:
    def test_saving_a_fuzz_request(self, database, qtbot):
        load_fixtures()

        editor_item = EditorItem()
        editor_item.name = 'New Fuzz Request'
        editor_item.item_type = EditorItem.TYPE_FUZZ
        editor_item.save()

        widget = FuzzEditPage(editor_item)
        qtbot.addWidget(widget)
        qtbot.waitForWindowShown(widget)

        # Enter form data
        widget.ui.urlInput.setText("http://www.wonderbill.com/login.php?username=${payload:usernames}&password=${payload:passwords}")

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
        qtbot.mouseClick(button, QtCore.Qt.LeftButton, pos=button.rect().center())

        http_flows = HttpFlow.order_by('id', 'desc').get()
        http_flow = http_flows[0]

        assert http_flow.type == 'editor_fuzz'
        assert http_flow.request.form_data['url'] == 'http://www.wonderbill.com/login.php?username=${payload:usernames}&password=${payload:passwords}'
        assert http_flow.request.form_data['fuzz_data']['payload_files'] == [
            {'file_path': './test/support/usernames.txt', 'key': 'usernames', 'num_items': 4, 'description': ''},
            {'file_path': './test/support/passwords.txt', 'key': 'passwords', 'num_items': 4, 'description': ''}
        ]
        assert http_flow.request.form_data['fuzz_data']['fuzz_type'] == 'one_to_one'

        # button = widget.ui.fuzzButton
        # qtbot.mouseClick(button, QtCore.Qt.LeftButton, pos=button.rect().center())

        # with qtbot.waitSignal(widget.worker.signals.result, timeout=10000):
        #     pass

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # qtbot.wait(3000)

        # assert 1 == 1
