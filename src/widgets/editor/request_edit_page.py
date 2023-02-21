from ast import For
from typing import Optional
import pyperclip

from PyQt6 import QtWidgets, QtCore, QtGui
from models.http_flow import HttpFlow
from models.http_response import HttpResponse
from repos.app_settings_repo import AppSettingsRepo
from services.editor_item_service import EditorItemService
from services.http_flow_service import HttpFlowService

from views._compiled.editor.request_edit_page import Ui_RequestEditPage
from models.http_request import FormData
from models.editor_item import EditorItem
from lib.background_worker import BackgroundWorker

class RequestEditPage(QtWidgets.QWidget):
    flow: HttpFlow
    editor_item: EditorItem
    latest_response: Optional[HttpResponse]

    form_input_changed = QtCore.pyqtSignal(bool)
    request_saved = QtCore.pyqtSignal(EditorItem)

    METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']

    def __init__(self, editor_item: EditorItem):
        super(RequestEditPage, self).__init__()

        self.editor_item = editor_item
        flow = self.editor_item.item
        if flow is None:
            raise Exception("RequestEditPage needs an editor item with a flow!")
        self.flow = flow

        self.ui = Ui_RequestEditPage()
        self.ui.setupUi(self)

        self.ui.urlInput.setText(self.editor_item.name)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.ui.examplesTable.setVisible(False)
        self.ui.toggleExamplesButton.setText("Saved Examples >>")
        self.restore_layout_state()

        self.ui.toggleExamplesButton.clicked.connect(self.toggle_examples_table)
        self.ui.sendButton.clicked.connect(self.ui.flowView.show_loader)
        self.ui.sendButton.clicked.connect(self.send_request_async)
        self.ui.saveButton.clicked.connect(self.save_request)
        self.ui.methodInput.insertItems(0, self.METHODS)

        self.ui.flowView.set_show_rendered(False)
        self.ui.flowView.set_request_editable(True)
        self.ui.flowView.set_save_as_example_enabled(False)
        self.ui.flowView.save_example_button.clicked.connect(self.save_example)

        self.show_request()
        self.show_examples()
        self.request_is_modified = False

        # save_response_button = QtWidgets.QPushButton('Save Response')
        # save_response_button.setContentsMargins(10, 10, 10, 10)
        # self.ui.responseTabs.setCornerWidget(save_response_button)

        # Form inputs:
        self.ui.urlInput.centre_text_vertically()
        self.ui.urlInput.enter_pressed.connect(self.send_request_async)
        self.ui.urlInput.text_changed.connect(self.form_field_changed)
        self.ui.methodInput.currentIndexChanged.connect(self.form_field_changed)

        self.threadpool = QtCore.QThreadPool()
        # self.ui.loaderWidget.ui.cancelButton.clicked.connect(self.cancel_request)

        # Keyboard shortcuts:
        keyseq_ctrl_s = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+S'), self)
        keyseq_ctrl_s.activated.connect(self.save_request)

        # keyseq_ctrl_enter = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+Enter'), self)
        # keyseq_ctrl_enter.activated.connect(self.send_request_async)

        self.ui.examplesTable.example_selected.connect(self.example_selected)
        self.ui.examplesTable.delete_examples.connect(self.delete_examples)

        # Request Actions Dropdown Button
        self.actions_menu = QtWidgets.QMenu(self.ui.actionsButton)
        action1 = QtGui.QAction("Copy as curl", self.actions_menu)
        action1.triggered.connect(self.action_copy_as_curl)
        self.actions_menu.addAction(action1)
        self.ui.actionsButton.setMenu(self.actions_menu)

    def action_copy_as_curl(self):
        print("Copy as curl...")
        self.update_request_with_values_from_form()
        pyperclip.copy(self.flow.request.get_curl_command())

    # TODO: This logic is spread all over the place here and in self.ui.flowView, it needs to be
    # cleaned up and encapsulated (probably most of the logic should go in FlowView)
    def show_request(self):
        self.set_send_save_buttons_enabled(True)

        form_data = self.flow.request.form_data
        self.ui.urlInput.setText(form_data['url'])
        self.set_method_on_form(form_data['method'])
        self.ui.flowView.set_flow(self.flow)

    def show_request_example(self):
        self.set_send_save_buttons_enabled(False)
        self.ui.flowView.set_flow(self.flow)

        self.ui.urlInput.setText(self.flow.request.get_url())
        self.ui.flowView.show_real_request()

    # When an example is selected it can either be the original request or an example
    def example_selected(self, flow):
        self.flow = flow

        if self.flow.is_example():
            self.show_request_example()
        else:
            self.show_request()

    def show_examples(self):
        self.ui.examplesTable.set_flow(self.flow)

    def set_send_save_buttons_enabled(self, enabled):
        self.ui.sendButton.setVisible(enabled)
        self.ui.saveButton.setVisible(enabled)

    def delete_examples(self, flows):
        example_flows = [f for f in flows if f.is_example()]

        if len(example_flows) == 0:
            return

        for flow in example_flows:
            flow.delete()

        self.ui.examplesTable.refresh()

    def save_request(self):
        self.update_request_with_values_from_form()

        EditorItemService().save(self.editor_item)
        HttpFlowService().save(self.flow)

        self.form_input_changed.emit(False)
        self.request_saved.emit(self.editor_item)

    def save_example(self):
        # 1. Save the HttpResponse (without a flow)
       #  self.save_request()

        # 3. Create the example HttpFlow
        if self.latest_response is None:
            return

        self.update_request_with_values_from_form()
        example_flow = self.flow.build_example(self.latest_response)
        HttpFlowService().save(example_flow)

        # 4. Update GUI
        self.ui.examplesTable.refresh()
        self.ui.flowView.set_save_as_example_enabled(False)

        if not self.ui.examplesTable.isVisible():
            self.toggle_examples_table()

    def response_received(self, http_response: HttpResponse):
        self.latest_response = http_response
        self.ui.flowView.set_response_from_editor(self.latest_response)
        self.ui.flowView.set_save_as_example_enabled(True)

    def request_error(self, error):
        exctype, value, traceback = error

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('Error')
        message_box.setText(str(value))
        message_box.exec()

    # TODO: Close the request:
    # https://stackoverflow.com/questions/10115126/python-requests-close-http-connection
    def send_request_async(self):
        print('Sending the request!')
        self.ui.flowView.show_loader()

        self.update_request_with_values_from_form()

        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        self.worker = BackgroundWorker(self.flow.make_request)
        self.worker.signals.result.connect(self.response_received)
        self.worker.signals.error.connect(self.request_error)
        self.worker.signals.finished.connect(self.ui.flowView.hide_loader)

        self.threadpool.start(self.worker) # type:ignore

    # Get the request values (method, url, header, content) from the form and set them on the
    # HttpRequest object, but dont save it
    def update_request_with_values_from_form(self):
        method = self.ui.methodInput.currentText()
        url = self.ui.urlInput.text()
        headers = self.ui.flowView.get_request_headers()
        content = self.ui.flowView.get_request_payload()
        form_data: FormData = {
            'method': method,
            'url': url,
            'headers': headers,
            'content': content,
            'fuzz_data': None
        }
        self.flow.request.set_form_data(form_data)
        self.ui.flowView.refresh_header_line()

    def cancel_request(self):
        self.worker.kill()
        self.ui.flowView.hide_loader()

    def form_field_changed(self):
        request_on_form = {
            'method': self.ui.methodInput.currentText(),
            'url': self.ui.urlInput.text()
        }
        original_request = {
            'method': self.flow.request.method or self.METHODS[0],
            'url': self.flow.request.get_url() or ''
        }

        self.request_is_modified = (request_on_form != original_request)
        self.form_input_changed.emit(self.request_is_modified)

    def toggle_examples_table(self):
        visible = not self.ui.examplesTable.isVisible()
        self.ui.examplesTable.setVisible(visible)

        if visible:
            self.restore_layout_state()

        if (visible):
            self.ui.toggleExamplesButton.setText("<< Saved Examples")
        else:
            self.ui.toggleExamplesButton.setText("Saved Examples >>")

    def restore_layout_state(self):
        settings = AppSettingsRepo().get()
        splitter_state = settings["request_edit_page_splitter_state"]

        if splitter_state is not None:
            self.ui.requestEditSplitter.restoreState(splitter_state)

    # TODO: This doesnt get called so never actually does anything
    def save_layout_state(self):
        settings = AppSettingsRepo().get()
        splitter_state = self.ui.requestEditSplitter.saveState()
        settings['request_edit_page_splitter_state'] = splitter_state
        AppSettingsRepo().save(settings)


    def set_method_on_form(self, method):
        if method is None:
            index = 0
        else:
            index = self.METHODS.index(method)

        self.ui.methodInput.setCurrentIndex(index)
