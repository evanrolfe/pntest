from PySide2 import QtWidgets, QtCore

from views._compiled.intercept.ui_intercept_page import Ui_InterceptPage
from lib.intercept_queue import InterceptQueue

class InterceptPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(InterceptPage, self).__init__(*args, **kwargs)
        self.ui = Ui_InterceptPage()
        self.ui.setupUi(self)

        self.__set_buttons_enabled(False)

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

        # self.intercepted_flow = HttpFlow.find(93)
        # self.decision_required(self.intercepted_flow)

    @QtCore.Slot()
    def decision_required(self, flow):
        self.intercepted_flow = flow
        self.__set_buttons_enabled(True)

        if self.intercepted_flow.has_response():
            self.ui.interceptTitle.setText(f"Intercepted Response: {flow.request.method} {flow.request.get_url()}")
            self.ui.headers.set_headers(flow.response.get_headers())
            self.ui.headers.set_header_line(flow.response.get_header_line_no_http_version())
            self.ui.bodyText.setPlainText(flow.response.content)
        else:
            self.ui.interceptTitle.setText(f"Intercepted Request: {flow.request.method} {flow.request.get_url()}")
            self.ui.headers.set_headers(flow.request.get_headers())
            self.ui.headers.set_header_line(flow.request.get_method_path())
            self.ui.bodyText.setPlainText(flow.request.content)

    @QtCore.Slot()
    def forward_button_clicked(self):
        header_line_arr = self.ui.headers.get_header_line().split(' ')
        modified_headers = self.ui.headers.get_headers()
        modified_content = self.ui.bodyText.toPlainText()

        if self.intercepted_flow.has_response():
            modified_status_code = int(header_line_arr[0])
            self.intercepted_flow.modify_response(modified_status_code, modified_headers, modified_content)
        else:
            modified_method = header_line_arr[0]
            modified_path = header_line_arr[1]
            self.intercepted_flow.modify_request(modified_method, modified_path, modified_headers, modified_content)

        # NOTE: Its important __clear_request comes before forward_flow, otherwise a race condition will occur
        self.__clear_request()

        reloaded_flow = self.intercepted_flow.reload()
        self.intercept_queue.forward_flow(reloaded_flow)

    def __clear_request(self):
        self.intercepted_request = None
        self.ui.interceptTitle.setText("Intercepted Request:")
        self.ui.headers.set_headers(None)
        self.ui.headers.set_header_line('')
        self.ui.bodyText.setPlainText("")
        self.__set_buttons_enabled(False)

    def __set_buttons_enabled(self, enabled):
        self.ui.forwardButton.setEnabled(enabled)
        self.ui.forwardInterceptButton.setEnabled(enabled)
        self.ui.dropButton.setEnabled(enabled)

    def set_enabled(self, intercept_enabled):
        self.intercept_enabled = intercept_enabled

        if intercept_enabled is True:
            self.ui.enabledButton.setText('Disable Intercept')
        else:
            self.ui.enabledButton.setText('Enable Intercept')
            self.__clear_request()

    # ===========================================================================
    # TODO:
    # ===========================================================================
    @QtCore.Slot()
    def forward_intercept_button_clicked(self):
        # TODO
        self.__clear_request()

    @QtCore.Slot()
    def enabled_button_clicked(self):
        new_value = not self.intercept_enabled
        print(new_value)
        # TODO
