import time
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets

from entities.container import Container
from entities.http_flow import HttpFlow
from entities.network import Network
from ui.views._compiled.docker.docker_tab import Ui_DockerTab
from ui.widgets.docker.console_proc import NUM_LINES, ConsoleProc


class DockerTab(QtWidgets.QWidget):
    container: Container
    console_proc: Optional[ConsoleProc]
    threadpool: QtCore.QThreadPool

    def __init__(self, *args, **kwargs):
        super(DockerTab, self).__init__(*args, **kwargs)
        self.ui = Ui_DockerTab()
        self.ui.setupUi(self)
        self.console_proc = None
        self.threadpool = QtCore.QThreadPool()

    def set_container(self, network: Network, container: Container):
        self.container = container
        self.ui.networkText.setPlainText(network.human_readable_desc())
        self.ui.containerText.setPlainText(container.human_readable_desc())
        self.setup_console()

    def setup_console(self):
        # Setup console
        console_args = ['docker', 'exec', '-it', self.container.short_id, 'bash']
        self.console_proc = ConsoleProc(console_args, NUM_LINES, 80)
        self.threadpool.start(self.console_proc)

        # Connect the signals:
        self.console_proc.signals.result.connect(self.ui.consoleText.output_received)
        self.ui.consoleText.key_pressed.connect(self.console_proc.key_pressed)

    def kill_console(self):
        if self.console_proc:
            self.console_proc.kill()
