from PySide2 import QtWidgets, QtCore, QtGui

from views._compiled.editor.ui_request_edit_page import Ui_RequestEditPage
from widgets.editor.request_headers_form import RequestHeadersForm
from widgets.editor.request_body_form import RequestBodyForm

from lib.app_settings import AppSettings
from lib.background_worker import BackgroundWorker
from lib.http_request import HttpRequest

class RequestEditPage(QtWidgets.QWidget):
    form_input_changed = QtCore.Signal(bool)
    request_saved = QtCore.Signal()

    METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']

    def __init__(self, editor_item):
        super(RequestEditPage, self).__init__()

        self.editor_item = editor_item
        self.request = self.editor_item.item()
        self.ui = Ui_RequestEditPage()
        self.ui.setupUi(self)

        self.ui.urlInput.setText(self.editor_item.name)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.hide_fuzz_table()
        self.settings = AppSettings.get_instance()
        self.restore_layout_state()

        self.ui.toggleFuzzTableButton.clicked.connect(self.toggle_fuzz_table)
        self.ui.sendButton.clicked.connect(self.show_loader)
        self.ui.sendButton.clicked.connect(self.send_request_async)
        self.ui.saveButton.clicked.connect(self.save_request)
        self.ui.methodInput.insertItems(0, self.METHODS)
        self.show_request()
        self.request_is_modified = False

        save_response_button = QtWidgets.QPushButton('Save Response')
        save_response_button.setContentsMargins(10, 10, 10, 10)
        self.ui.responseTabs.setCornerWidget(save_response_button)

        # Form inputs:
        self.ui.urlInput.returnPressed.connect(self.send_request_async)
        self.ui.urlInput.textChanged.connect(self.form_field_changed)
        self.ui.methodInput.currentIndexChanged.connect(self.form_field_changed)

        # self.show_loader()
        self.threadpool = QtCore.QThreadPool()
        self.ui.loaderWidget.ui.cancelButton.clicked.connect(self.cancel_request)

        # Keyboard shortcuts:
        self.connect(
            QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S), self),
            QtCore.SIGNAL('activated()'),
            self.save_request
        )
        # TODO: self.connect(QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self),
        #  QtCore.SIGNAL('activated()'), self.send_request_async)

    @QtCore.Slot()
    def show_loader(self):
        print('showing the loader')
        self.ui.stackedWidget.setCurrentWidget(self.ui.loaderWidget)

    def hide_loader(self):
        print('hiding the loader')
        self.ui.stackedWidget.setCurrentWidget(self.ui.responseTabs)

    def show_request(self):
        self.ui.urlInput.setText(self.request.url)
        self.set_method_on_form(self.request.method)

        # Request Headers and body
        self.request_headers_form = RequestHeadersForm(self.editor_item)
        self.request_body_form = RequestBodyForm(self.editor_item)

        self.ui.requestTabs.insertTab(0, self.request_headers_form, 'Headers')
        self.ui.requestTabs.insertTab(1, self.request_body_form, 'Body')

    @QtCore.Slot()
    def save_request(self):
        method = self.ui.methodInput.currentText()
        url = self.ui.urlInput.text()
        headers = self.request_headers_form.get_headers()

        self.request.url = url
        self.request.method = method
        self.request.request_payload = self.request_body_form.get_body()
        self.request.set_request_headers(headers)
        self.request.save()

        self.form_input_changed.emit(False)
        self.request_saved.emit()
        print(f'saving {method} {url} to request {self.request.id}')

    @QtCore.Slot()
    def response_received(self, response):
        # Display response headers and body
        self.ui.responseBodyText.setPlainText(response.text)

        headers_text = ""
        for key, value in response.headers.items():
            headers_text += f"{key}: {value}\n"

        self.ui.responseHeadersText.setPlainText(headers_text)

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
        self.show_loader()

        method = self.ui.methodInput.currentText()
        url = self.ui.urlInput.text()
        headers = self.request_headers_form.get_headers()
        body = self.request_body_form.get_body()
        http_request = HttpRequest(method, url, headers, body)

        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        self.worker = BackgroundWorker(lambda: http_request.send())
        self.worker.signals.result.connect(self.response_received)
        self.worker.signals.error.connect(self.request_error)
        self.worker.signals.finished.connect(self.hide_loader)

        self.threadpool.start(self.worker)

    @QtCore.Slot()
    def cancel_request(self):
        self.worker.kill()
        self.hide_loader()

    @QtCore.Slot()
    def form_field_changed(self):
        request_on_form = {
            'method': self.ui.methodInput.currentText(),
            'url': self.ui.urlInput.text()
        }
        original_request = {
            'method': self.request.method or self.METHODS[0],
            'url': self.request.url or ''
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
        splitter_state = self.settings.get("RequestEditPage.splitter", None)
        splitter_state2 = self.settings.get("RequestEditPage.splitter2", None)

        self.ui.requestEditSplitter.restoreState(splitter_state)
        self.ui.splitter2.restoreState(splitter_state2)

    def save_layout_state(self):
        splitter_state = self.ui.requestEditSplitter.saveState()
        splitter_state2 = self.ui.splitter2.saveState()

        self.settings.save("RequestEditPage.splitter", splitter_state)
        self.settings.save("RequestEditPage.splitter2", splitter_state2)

    def set_method_on_form(self, method):
        if method is None:
            index = 0
        else:
            index = self.METHODS.index(method)

        self.ui.methodInput.setCurrentIndex(index)
