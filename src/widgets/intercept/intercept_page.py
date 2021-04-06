from PySide2 import QtWidgets, QtCore

from views._compiled.intercept.ui_intercept_page import Ui_InterceptPage
from lib.intercept_queue import InterceptQueue
# from models.data.setting import Setting

class InterceptPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(InterceptPage, self).__init__(*args, **kwargs)
        self.ui = Ui_InterceptPage()
        self.ui.setupUi(self)

        self.__set_buttons_enabled(False)

        # Register callback with the backend:
        # self.backend = Backend.get_instance()
        # self.backend.register_callback('requestIntercepted', self.request_intercepted)
        # self.backend.register_callback('responseIntercepted', self.response_intercepted)

        # Connect buttons:
        self.ui.forwardButton.clicked.connect(self.forward_button_clicked)
        self.ui.forwardInterceptButton.clicked.connect(self.forward_intercept_button_clicked)
        self.ui.enabledButton.clicked.connect(self.enabled_button_clicked)

        # Set enabled/disabled:
        # self.ui.enabledButton.setCheckable(True)
        # intercept_enabled = Setting.intercept_enabled()
        self.set_enabled(True)
        self.__set_buttons_enabled(True)
        # self.ui.enabledButton.setDown(intercept_enabled)

        self.intercept_queue = InterceptQueue()
        self.intercept_queue.decision_required.connect(self.decision_required)

    @QtCore.Slot()
    def decision_required(self, flow):
        print(f'[InterceptPage] flow id {flow.id} intercepted!')
        self.ui.interceptTitle.setText(f"Intercepted Request: {flow.request.method} {flow.request.get_url()}")
        self.ui.headersText.setPlainText(flow.request.headers)
        self.__set_buttons_enabled(True)
        self.intercepted_flow = flow

    @QtCore.Slot()
    def forward_button_clicked(self):
        print(f'Forwarding flow {self.intercepted_flow.uuid} and client_id={self.intercepted_flow.client_id}')
        self.intercept_queue.forward_flow(self.intercepted_flow)
        self.__clear_request()

    def response_intercepted(self, request):
        self.intercepted_request = request

        self.ui.interceptTitle.setText(
            f"Intercepted Response: {request['method']} {request['path']}")

        self.ui.headersText.setPlainText(request['rawResponse'])
        self.ui.bodyText.setPlainText(request['responseBody'])

        self.__set_buttons_enabled(True)
        self.ui.forwardInterceptButton.setEnabled(False)

    def __clear_request(self):
        self.intercepted_request = None
        self.ui.interceptTitle.setText("Intercepted Request:")
        self.ui.headersText.setPlainText("")
        self.ui.bodyText.setPlainText("")
        self.__set_buttons_enabled(False)

    def __set_buttons_enabled(self, enabled):
        self.ui.forwardButton.setEnabled(enabled)
        self.ui.forwardInterceptButton.setEnabled(enabled)
        self.ui.dropButton.setEnabled(enabled)

    @QtCore.Slot()
    def forward_intercept_button_clicked(self):
        self.get_data_from_form()

        self.backend.forward_intercept_request(self.intercepted_request)
        self.__clear_request()

    @QtCore.Slot()
    def enabled_button_clicked(self):
        new_value = not self.intercept_enabled
        self.backend.change_setting('interceptEnabled', new_value)
        self.set_enabled(new_value)

    def get_data_from_form(self):
        # If intercepted_request is a response:
        if self.intercepted_request.get('rawResponse') is not None:
            self.intercepted_request['rawResponse'] = self.ui.headersText.toPlainText()
            self.intercepted_request['rawResponseBody'] = self.ui.bodyText.toPlainText()
        else:
            self.intercepted_request['rawRequest'] = self.ui.headersText.toPlainText()

    def set_enabled(self, intercept_enabled):
        self.intercept_enabled = intercept_enabled

        if intercept_enabled is True:
            self.ui.enabledButton.setText('Disable Intercept')
        else:
            self.ui.enabledButton.setText('Enable Intercept')
            self.__clear_request()
