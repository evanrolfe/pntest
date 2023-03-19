from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets

from entities.http_flow import HttpFlow
from repos.http_flow_repo import HttpFlowRepo
from repos.ws_message_repo import WsMessageRepo
from services.intercept_queue import InterceptQueue
from ui.views._compiled.docker.docker_page import Ui_DockerPage


class DockerPage(QtWidgets.QWidget):
    intercepted_flow: Optional[HttpFlow]
    something_intercepted = QtCore.pyqtSignal()
    intercept_queue_empty = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(DockerPage, self).__init__(*args, **kwargs)
        self.ui = Ui_DockerPage()
        self.ui.setupUi(self)

        self.ui.refreshButton.setIcon(QtGui.QIcon('assets:icons/dark/icons8-refresh-64.png'))
