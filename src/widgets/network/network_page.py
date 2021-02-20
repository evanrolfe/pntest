from PySide2 import QtCore, QtWidgets

from widgets.network.http_page import HttpPage

class NetworkPage(QtWidgets.QWidget):
    send_request_to_editor = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(NetworkPage, self).__init__(*args, **kwargs)

        http_page = HttpPage()

        stacked_widget = QtWidgets.QStackedWidget()
        stacked_widget.addWidget(http_page)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(stacked_widget)
