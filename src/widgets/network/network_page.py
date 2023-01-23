from PyQt6 import QtCore, QtWidgets

from widgets.network.http_page import HttpPage
from widgets.network.ws_page import WsPage

class NetworkPage(QtWidgets.QWidget):
    send_flow_to_editor = QtCore.pyqtSignal(object)
    send_flow_to_fuzzer = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(NetworkPage, self).__init__(*args, **kwargs)

        self.http_page = HttpPage()
        self.ws_page = WsPage()

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(self.http_page)
        self.stacked_widget.addWidget(self.ws_page)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)

        # Connect signals
        self.http_page.send_flow_to_editor.connect(self.send_flow_to_editor)
        self.http_page.send_flow_to_fuzzer.connect(self.send_flow_to_fuzzer)
        self.ws_page.toggle_page.connect(self.set_page_http)
        self.http_page.toggle_page.connect(self.set_page_ws)

    def set_page_http(self):
        self.stacked_widget.setCurrentWidget(self.http_page)

    def set_page_ws(self):
        self.stacked_widget.setCurrentWidget(self.ws_page)

    def save_layout_state(self):
        self.http_page.save_layout_state()
        self.ws_page.save_layout_state()

    def reload(self):
        self.http_page.reload()
        self.ws_page.reload()

    def layout_changed(self, layout: str):
        self.http_page.layout_changed(layout)
