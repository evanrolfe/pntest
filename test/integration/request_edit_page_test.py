# import time
from PySide2 import QtCore
from models.data.http_flow import HttpFlow
from support.fixtures import load_fixtures

from models.data.editor_item_unsaved import EditorItemUnsaved
from widgets.editor.request_edit_page import RequestEditPage

class TestEditorPage:
    def test_editor_page_saving_a_request(self, database, qtbot):
        load_fixtures()

        editor_item = EditorItemUnsaved()
        widget = RequestEditPage(editor_item)
        qtbot.addWidget(widget)
        qtbot.waitForWindowShown(widget)

        # Enter form data
        widget.ui.urlInput.setText("http://localhost:8080/v1/accounts")

        # Click save button
        button = widget.ui.saveButton
        qtbot.mouseClick(button, QtCore.Qt.LeftButton, pos=button.rect().center())

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # time.sleep(3)
        http_flows = HttpFlow.order_by('id', 'desc').get()
        http_flow = http_flows[0]

        assert http_flow.request.http_version == 'HTTP/1.1'
        assert http_flow.request.headers == '{"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"}'
        assert http_flow.request.content == ''
        assert http_flow.request.host == 'localhost'
        assert http_flow.request.port == 8080
        assert http_flow.request.method == 'GET'
        assert http_flow.request.scheme == 'http'
        assert http_flow.request.authority is None
        assert http_flow.request.path == '/v1/accounts'

        assert http_flow.request.form_data['method'] == 'GET'
        assert http_flow.request.form_data['url'] == 'http://localhost:8080/v1/accounts'
        assert http_flow.request.form_data['headers'] == {'Content-Length': '<calculated when request is sent>', 'Host': '<calculated when request is sent>', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'User-Agent': 'pntest/0.1'}
        assert http_flow.request.form_data['body'] == ''
