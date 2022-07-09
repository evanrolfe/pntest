from PyQt6 import QtWidgets, QtCore

from views._compiled.intercept.intercept_page import Ui_InterceptPage
from lib.intercept_queue import InterceptQueue

class InterceptPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(InterceptPage, self).__init__(*args, **kwargs)
        self.ui = Ui_InterceptPage()
        self.ui.setupUi(self)

        # Connect buttons:
        self.ui.forwardButton.clicked.connect(self.forward_button_clicked)
        self.ui.forwardInterceptButton.clicked.connect(self.forward_intercept_button_clicked)
        self.ui.enabledButton.clicked.connect(self.enabled_button_clicked)
        self.ui.dropButton.clicked.connect(self.drop_button_clicked)

        # Set enabled/disabled:
        # self.ui.enabledButton.setCheckable(True)
        self.__set_enabled(False)
        self.__set_buttons_enabled(False)
        # self.ui.enabledButton.setDown(intercept_enabled)

        self.intercept_queue = InterceptQueue()
        self.intercept_queue.decision_required.connect(self.decision_required)

    def decision_required(self, flow):
        self.intercepted_flow = flow
        self.__set_buttons_enabled(True)

        if hasattr(self.intercepted_flow, 'intercept_websocket_message'):
            self.ui.interceptTitle.setText(
                f"Intercepted Websocket Message: {flow.request.method} {flow.request.get_url()}"
            )
            self.ui.headers.set_headers(None)
            self.ui.headers.set_header_line('')
            self.ui.bodyText.setPlainText(flow.websocket_messages[-1].content)

        elif self.intercepted_flow.has_response():
            self.ui.interceptTitle.setText(f"Intercepted HTTP Response: {flow.request.method} {flow.request.get_url()}")
            self.ui.headers.set_headers(flow.response.get_headers())
            self.ui.headers.set_header_line(flow.response.get_header_line_no_http_version())
            self.ui.bodyText.setPlainText(flow.response.content)

            self.ui.forwardInterceptButton.setEnabled(False)

        else:
            self.ui.interceptTitle.setText(f"Intercepted HTTP Request: {flow.request.method} {flow.request.get_url()}")
            self.ui.headers.set_headers(flow.request.get_headers())
            self.ui.headers.set_header_line(flow.request.get_header_line_no_http_version())
            self.ui.bodyText.setPlainText(flow.request.content)

    def forward_button_clicked(self):
        self.__forward_flow(False)

    def forward_intercept_button_clicked(self):
        self.__forward_flow(True)

    def drop_button_clicked(self):
        self.__clear_request()
        self.intercept_queue.drop_flow(self.intercepted_flow)

    def enabled_button_clicked(self):
        if self.intercept_enabled:
            self.__clear_request()
            self.intercept_queue.forward_all()

        self.intercept_queue.set_enabled(not self.intercept_enabled)
        self.__set_enabled(not self.intercept_enabled)

    # Private methods

    def __forward_flow(self, intercept_response):
        header_line_arr = self.ui.headers.get_header_line().split(' ')
        modified_headers = self.ui.headers.get_headers()
        modified_content = self.ui.bodyText.toPlainText()

        if hasattr(self.intercepted_flow, 'intercept_websocket_message'):
            print('Forwarding websocket!')
            self.intercepted_flow.modify_latest_websocket_message(modified_content)

        elif self.intercepted_flow.has_response():
            modified_status_code = int(header_line_arr[0])
            self.intercepted_flow.modify_response(modified_status_code, modified_headers, modified_content)

        else:
            modified_method = header_line_arr[0]
            modified_path = header_line_arr[1]
            self.intercepted_flow.modify_request(modified_method, modified_path, modified_headers, modified_content)

        # NOTE: Its important __clear_request comes before forward_flow, otherwise a race condition will occur
        self.__clear_request()

        reloaded_flow = self.intercepted_flow.reload()
        self.intercept_queue.forward_flow(reloaded_flow, intercept_response)

    def __clear_request(self):
        self.intercepted_request = None
        self.ui.interceptTitle.setText("Intercepted Request:")
        self.ui.headers.set_headers(None)
        self.ui.headers.set_header_line('')
        self.ui.bodyText.setPlainText("")
        self.__set_buttons_enabled(False)

    def __set_enabled(self, intercept_enabled):
        self.intercept_enabled = intercept_enabled

        if intercept_enabled is True:
            self.ui.enabledButton.setText('Disable Intercept')
        else:
            self.ui.enabledButton.setText('Enable Intercept')
            self.__clear_request()

    def __set_buttons_enabled(self, enabled):
        self.ui.forwardButton.setEnabled(enabled)
        self.ui.forwardInterceptButton.setEnabled(enabled)
        self.ui.dropButton.setEnabled(enabled)
