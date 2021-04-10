from PySide2 import QtWidgets, QtCore, QtGui
from urllib.parse import urlsplit

from views._compiled.editor.ui_request_edit_page import Ui_RequestEditPage

from lib.app_settings import AppSettings
from lib.background_worker import BackgroundWorker
from lib.http_request import HttpRequest as HttpRequestLib
from models.data.http_response import HttpResponse

class RequestEditPage(QtWidgets.QWidget):
    form_input_changed = QtCore.Signal(bool)
    request_saved = QtCore.Signal()

    METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']

    def __init__(self, editor_item):
        super(RequestEditPage, self).__init__()

        self.editor_item = editor_item
        self.flow = self.editor_item.item()
        self.request = self.flow.request

        self.ui = Ui_RequestEditPage()
        self.ui.setupUi(self)

        self.ui.urlInput.setText(self.editor_item.name)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.hide_fuzz_table()
        self.settings = AppSettings.get_instance()
        self.restore_layout_state()

        self.ui.toggleFuzzTableButton.clicked.connect(self.toggle_fuzz_table)
        self.ui.sendButton.clicked.connect(self.ui.flowView.show_loader)
        self.ui.sendButton.clicked.connect(self.send_request_async)
        self.ui.saveButton.clicked.connect(self.save_request)
        self.ui.methodInput.insertItems(0, self.METHODS)

        self.ui.flowView.set_show_rendered(False)
        self.ui.flowView.show_save_as_example_button()
        self.ui.flowView.save_example_button.clicked.connect(self.save_example)

        self.show_request()
        self.request_is_modified = False

        # save_response_button = QtWidgets.QPushButton('Save Response')
        # save_response_button.setContentsMargins(10, 10, 10, 10)
        # self.ui.responseTabs.setCornerWidget(save_response_button)

        # Form inputs:
        self.ui.urlInput.returnPressed.connect(self.send_request_async)
        self.ui.urlInput.textChanged.connect(self.form_field_changed)
        self.ui.methodInput.currentIndexChanged.connect(self.form_field_changed)

        self.threadpool = QtCore.QThreadPool()
        # self.ui.loaderWidget.ui.cancelButton.clicked.connect(self.cancel_request)

        # Keyboard shortcuts:
        self.connect(
            QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S), self),
            QtCore.SIGNAL('activated()'),
            self.save_request
        )
        # TODO: self.connect(QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self),
        #  QtCore.SIGNAL('activated()'), self.send_request_async)

    def show_request(self):
        self.ui.urlInput.setText(self.flow.request.get_url())
        self.set_method_on_form(self.flow.request.method)

        self.ui.flowView.set_flow(self.flow)

    @QtCore.Slot()
    def save_request(self):
        self.update_request_with_values_from_form()
        self.flow.request.save()
        self.form_input_changed.emit(False)
        self.request_saved.emit()

    @QtCore.Slot()
    def save_example(self):
        print('Saving an example!')
        self.update_request_with_values_from_form()
        self.latest_response.save()
        example_flow = self.flow.duplicate_for_example(self.latest_response)
        print(f'Saved example flow: {example_flow.id}')

    @QtCore.Slot()
    def response_received(self, requests_response):
        self.latest_response = HttpResponse.from_requests_response(requests_response)
        self.ui.flowView.set_response_from_editor(self.flow, self.latest_response)

    @QtCore.Slot()
    def request_error(self, error):
        exctype, value, traceback = error

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('Error')
        message_box.setText(str(value))
        message_box.exec_()

    # TODO: Close the request:
    # https://stackoverflow.com/questions/10115126/python-requests-close-http-connection
    @QtCore.Slot()
    def send_request_async(self):
        print('Sending the request!')
        self.ui.flowView.show_loader()

        method = self.ui.methodInput.currentText()
        url = self.ui.urlInput.text()
        headers = self.ui.flowView.get_request_headers()
        payload = self.ui.flowView.get_request_payload()
        http_request = HttpRequestLib(method, url, headers, payload)

        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        self.worker = BackgroundWorker(lambda: http_request.send())
        self.worker.signals.result.connect(self.response_received)
        self.worker.signals.error.connect(self.request_error)
        self.worker.signals.finished.connect(self.ui.flowView.hide_loader)

        self.threadpool.start(self.worker)

    # Get the request values (method, url, header, content) from the form and set them on the
    # HttpRequest object, but dont save it
    def update_request_with_values_from_form(self):
        method = self.ui.methodInput.currentText()
        url = self.ui.urlInput.text()
        headers = self.ui.flowView.get_request_headers()
        url_data = urlsplit(url)

        self.flow.request.method = method
        self.flow.request.host = url_data.hostname
        if url_data.port:
            self.flow.request.port = url_data.port

        if url_data.query == '':
            self.flow.request.path = url_data.path
        else:
            self.flow.request.path = url_data.path + '?' + url_data.query

        self.flow.request.content = self.ui.flowView.get_request_payload()
        self.flow.request.set_headers(headers)

    @QtCore.Slot()
    def cancel_request(self):
        self.worker.kill()
        self.ui.flowView.hide_loader()

    @QtCore.Slot()
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

    def hide_fuzz_table(self):
        self.ui.fuzzRequestsTable.setVisible(False)
        self.ui.toggleFuzzTableButton.setText("9 Saved Examples [+]")

    @QtCore.Slot()
    def toggle_fuzz_table(self):
        visible = not self.ui.fuzzRequestsTable.isVisible()
        self.ui.fuzzRequestsTable.setVisible(visible)

        if visible:
            self.restore_layout_state()

        if (visible):
            self.ui.toggleFuzzTableButton.setText("9 Saved Examples [-]")
        else:
            self.ui.toggleFuzzTableButton.setText("9 Saved Examples [+]")

    def restore_layout_state(self):
        return None
        # splitter_state = self.settings.get("RequestEditPage.splitter", None)
        # splitter_state2 = self.settings.get("RequestEditPage.splitter2", None)

        # self.ui.requestEditSplitter.restoreState(splitter_state)
        # self.ui.splitter2.restoreState(splitter_state2)

    def save_layout_state(self):
        return None
        # splitter_state = self.ui.requestEditSplitter.saveState()
        # splitter_state2 = self.ui.splitter2.saveState()

        # self.settings.save("RequestEditPage.splitter", splitter_state)
        # self.settings.save("RequestEditPage.splitter2", splitter_state2)

    def set_method_on_form(self, method):
        if method is None:
            index = 0
        else:
            index = self.METHODS.index(method)

        self.ui.methodInput.setCurrentIndex(index)
