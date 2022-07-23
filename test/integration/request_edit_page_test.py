from PyQt6 import QtCore
import requests
from pytest_httpserver import HTTPServer
from models.data.http_flow import HttpFlow
from support.fixtures import load_fixtures

from models.data.editor_item_unsaved import EditorItemUnsaved
from widgets.editor.request_edit_page import RequestEditPage

class TestEditorPage:
    def test_editor_page_saving_a_request_with_variables(self, database, qtbot):
        load_fixtures()

        editor_item = EditorItemUnsaved()
        widget = RequestEditPage(editor_item)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Enter form data
        widget.ui.urlInput.setText("http://${var:host}:8080/${var:apiVersion}/accounts?hello=${b64url:world}")
        widget.ui.flowView.ui.requestBody.set_value('{ "account_name": "${var:account_name}" }')

        # Set the headers via the table model because QtBot is rubbish
        model = widget.ui.flowView.ui.requestHeaders.table_model
        model.headers[len(model.headers) - 1] = (True, 'X-Api-Token', '${var:apiToken}')

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # qtbot.wait(3000)

        # Click save button
        button = widget.ui.saveButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        http_flows = HttpFlow.order_by('id', 'desc').get()
        http_flow = http_flows[0]

        assert http_flow.request.http_version == 'HTTP/1.1'
        assert http_flow.request.headers == '{"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1", "X-Api-Token": "0123456789"}'
        assert http_flow.request.content == '{ "account_name": "MyAccount" }'
        assert http_flow.request.host == 'localhost'
        assert http_flow.request.port == 8080
        assert http_flow.request.method == 'GET'
        assert http_flow.request.scheme == 'http'
        assert http_flow.request.authority is None
        assert http_flow.request.path == '/v2/accounts?hello=d29ybGQ='

        assert http_flow.request.form_data['method'] == 'GET'
        assert http_flow.request.form_data['url'] == 'http://${var:host}:8080/${var:apiVersion}/accounts?hello=${b64url:world}'
        assert http_flow.request.form_data['headers'] == {
            'Content-Length': '<calculated when request is sent>',
            'Host': '<calculated when request is sent>',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'User-Agent': 'pntest/0.1',
            'X-Api-Token': '${var:apiToken}'
        }
        assert http_flow.request.form_data['content'] == '{ "account_name": "${var:account_name}" }'

    def test_editor_page_sending_a_request_and_saving_example(self, database, qtbot, httpserver: HTTPServer):
        load_fixtures()

        httpserver.expect_request("/v2/accounts/aGVsbG8gd29ybGQ=").respond_with_data("helloworld")

        editor_item = EditorItemUnsaved()
        widget = RequestEditPage(editor_item)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Enter form data
        widget.ui.urlInput.setText(httpserver.url_for("/") + "${var:apiVersion}/accounts/${b64:hello world}")

        # Click send button
        button = widget.ui.sendButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        with qtbot.waitSignal(widget.worker.signals.result, timeout=10000):
            pass

        # Click save as example button
        button2 = widget.ui.flowView.save_example_button
        qtbot.mouseClick(button2, QtCore.Qt.MouseButton.LeftButton, pos=button2.rect().center())

        example_flows = widget.ui.examplesTable.table_model.flows
        original_flow = example_flows[0]
        example_flow = example_flows[1]

        assert original_flow.id == example_flow.http_flow_id

        assert original_flow.request.id is not None
        # assert original_flow.request.get_url() == "..."
        assert not original_flow.response

        assert example_flow.request.id is not None
        assert "/v2/accounts/aGVsbG8gd29ybGQ=" in example_flow.request.get_url()

        assert example_flow.response.id is not None  # type: ignore
        assert example_flow.response.content == "helloworld"  # type: ignore
