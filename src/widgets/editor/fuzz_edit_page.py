from PyQt6 import QtWidgets, QtCore, QtGui
from lib.fuzz_http_requests import FuzzHttpRequests
from models.data.http_flow import HttpFlow

from views._compiled.editor.fuzz_edit_page import Ui_FuzzEditPage

from lib.app_settings import AppSettings
from lib.background_worker import BackgroundWorker
from models.data.http_request import FormData

class FuzzEditPage(QtWidgets.QWidget):
    flow: HttpFlow
    fuzzer: FuzzHttpRequests

    form_input_changed = QtCore.pyqtSignal(bool)
    request_saved = QtCore.pyqtSignal()

    METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']

    def __init__(self, editor_item):
        super(FuzzEditPage, self).__init__()

        self.editor_item = editor_item
        self.flow = self.editor_item.item()
        self.request = self.flow.request
        self.original_flow = self.flow

        self.ui = Ui_FuzzEditPage()
        self.ui.setupUi(self)

        self.ui.urlInput.setText(self.editor_item.name)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.ui.examplesTable.setVisible(False)
        self.ui.toggleExamplesButton.setText("Saved Examples >>")
        self.settings = AppSettings.get_instance()
        self.restore_layout_state()

        self.ui.toggleExamplesButton.clicked.connect(self.toggle_examples_table)
        self.ui.fuzzButton.clicked.connect(self.ui.fuzzView.show_loader)
        self.ui.fuzzButton.clicked.connect(self.start_fuzzing_async)

        self.ui.saveButton.clicked.connect(self.save_request)
        self.ui.methodInput.insertItems(0, self.METHODS)

        self.ui.fuzzView.cancel_clicked.connect(self.loader_cancel_clicked)

        self.show_request()
        self.show_examples()
        self.request_is_modified = False

        # save_response_button = QtWidgets.QPushButton('Save Response')
        # save_response_button.setContentsMargins(10, 10, 10, 10)
        # self.ui.responseTabs.setCornerWidget(save_response_button)

        # Form inputs:
        self.ui.urlInput.centre_text_vertically()
        self.ui.urlInput.textChanged.connect(self.form_field_changed)
        self.ui.methodInput.currentIndexChanged.connect(self.form_field_changed)

        self.threadpool = QtCore.QThreadPool()
        # self.ui.loaderWidget.ui.cancelButton.clicked.connect(self.cancel_request)

        # Keyboard shortcuts:
        # TODO:
        # self.connect(
        #     QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S), self),
        #     QtCore.SIGNAL('activated()'),
        #     self.save_request
        # )
        # TODO: self.connect(QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self),
        #  QtCore.SIGNAL('activated()'), self.send_request_async)

        self.ui.examplesTable.example_selected.connect(self.show_example)
        self.ui.examplesTable.delete_examples.connect(self.delete_examples)

    def show_request(self):
        form_data = self.flow.request.form_data
        self.ui.urlInput.setText(form_data['url'])
        self.set_method_on_form(form_data['method'])
        self.ui.fuzzView.set_flow(self.flow)

    def start_fuzzing_async(self):
        print('Fuzzing...')
        self.save_request()
        self.fuzzer = FuzzHttpRequests(self.flow)
        self.worker = BackgroundWorker(self.fuzzer.start)
        self.worker.signals.result.connect(self.fuzz_finished)
        self.worker.signals.error.connect(self.request_error)
        self.worker.signals.response_received.connect(self.example_response_received)
        self.worker.signals.finished.connect(self.ui.fuzzView.hide_loader)

        self.threadpool.start(self.worker)

    def example_response_received(self, example_flow: HttpFlow):
        if not self.ui.examplesTable.isVisible():
            self.toggle_examples_table()

        # TODO: Find a more effecient way of doing this:
        self.flow = self.flow.reload()
        self.show_examples()
        print(f'Got response for example: {example_flow.request.get_url()}')

    def fuzz_finished(self):
        print('Finished!')

    def loader_cancel_clicked(self):
        self.fuzzer.cancel()

    def show_examples(self):
        self.ui.examplesTable.set_flow(self.flow)

    def set_send_save_buttons_enabled(self, enabled):
        self.ui.fuzzButton.setVisible(enabled)
        self.ui.saveButton.setVisible(enabled)

    def show_example(self, flow):
        self.flow = flow
        self.show_request()
        self.set_send_save_buttons_enabled(not self.flow.is_example())

    def delete_examples(self, flows):
        example_flows = [f for f in flows if f.is_example()]

        if len(example_flows) == 0:
            return

        for flow in example_flows:
            flow.delete()

        self.ui.examplesTable.reload()

    def save_request(self):
        self.update_request_with_values_from_form()
        if hasattr(self.flow, 'id'):
            self.flow.request.save()
        else:
            saved_editor_item = self.editor_item.save()
            self.editor_item = saved_editor_item
            self.flow = self.editor_item.item()
            self.request = self.flow.request
            self.original_flow = self.flow

        self.form_input_changed.emit(False)
        self.request_saved.emit()

    def request_error(self, error):
        exctype, value, traceback = error

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('Error')
        message_box.setText(str(value))
        message_box.exec()

    # Get the request values (method, url, header, content) from the form and set them on the
    # HttpRequest object, but dont save it
    def update_request_with_values_from_form(self):
        method = self.ui.methodInput.currentText()
        url = self.ui.urlInput.text()
        headers = self.ui.fuzzView.get_request_headers()
        content = self.ui.fuzzView.get_request_body()
        payload_files = self.ui.fuzzView.get_request_payload_files()
        payload_files_serialised = [p.serialise() for p in payload_files]
        fuzz_type = self.ui.fuzzView.get_fuzz_type()
        delay_type = self.ui.fuzzView.get_delay_type()

        form_data: FormData = {
            'method': method,
            'url': url,
            'headers': headers,
            'content': content,
            'fuzz_data': {
                'payload_files': payload_files_serialised,
                'fuzz_type': fuzz_type,
                'delay_type': delay_type
            }
        }
        self.flow.request.set_form_data(form_data)

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
        return None
        # splitter_state = self.settings.get("FuzzEditPage.splitter", None)
        # splitter_state2 = self.settings.get("FuzzEditPage.splitter2", None)

        # self.ui.requestEditSplitter.restoreState(splitter_state)
        # if splitter_state2 is not None:
        #   self.ui.splitter2.restoreState(splitter_state2)

    def save_layout_state(self):
        return None
        # splitter_state = self.ui.requestEditSplitter.saveState()
        # splitter_state2 = self.ui.splitter2.saveState()

        # self.settings.save("FuzzEditPage.splitter", splitter_state)
        # self.settings.save("FuzzEditPage.splitter2", splitter_state2)

    def set_method_on_form(self, method):
        if method is None:
            index = 0
        else:
            index = self.METHODS.index(method)

        self.ui.methodInput.setCurrentIndex(index)
