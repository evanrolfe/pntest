import time
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets

from entities.container import Container
from entities.http_flow import HttpFlow
from entities.network import Network
from ui.views._compiled.docker.docker_tab import Ui_DockerTab
from ui.widgets.docker.console_proc import NUM_LINES, ConsoleProc
from ui.widgets.docker.logs_proc import LogsProc


class DockerTab(QtWidgets.QWidget):
    container: Container
    console_proc: Optional[ConsoleProc]
    logs_proc: Optional[LogsProc]
    threadpool: QtCore.QThreadPool

    def __init__(self, *args, **kwargs):
        super(DockerTab, self).__init__(*args, **kwargs)
        self.ui = Ui_DockerTab()
        self.ui.setupUi(self)
        self.console_proc = None
        self.logs_proc = None
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.setMaxThreadCount(2)

        self.ui.dockerContainerTabs.currentChanged.connect(self.tab_changed)

        # Tabs Corner Widget
        self.activate_intercept_button = QtWidgets.QPushButton('Activate Network Interception')
        self.activate_intercept_button.setObjectName('activateInterception')

        self.response_corner_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(self.response_corner_widget)
        layout.setContentsMargins(0, 0, 3, 3)
        layout.addWidget(self.activate_intercept_button)

        self.ui.dockerContainerTabs.setCornerWidget(self.response_corner_widget)


    def set_container(self, network: Network, container: Container):
        self.container = container
        self.ui.networkText.setPlainText(network.human_readable_desc())
        self.ui.containerText.setPlainText(container.human_readable_desc())

    def tab_changed(self, i: int):
        if i == 2:
            self.setup_logs()
        elif i == 3:
            self.setup_console()

    def setup_console(self):
        if self.console_proc:
            return

        # Setup console
        console_args = ['docker', 'exec', '-it', self.container.short_id, 'bash']
        self.console_proc = ConsoleProc(console_args, NUM_LINES, 80)
        self.threadpool.start(self.console_proc)

        # Connect the signals:
        self.console_proc.signals.result.connect(self.ui.consoleText.output_received)
        self.ui.consoleText.key_pressed.connect(self.console_proc.key_pressed)

    def setup_logs(self):
        if self.logs_proc:
            return

        self.logs_proc = LogsProc(self.container, self.ui.logsText)
        self.threadpool.start(self.logs_proc, )

        # Connect the signals:
        self.logs_proc.signals.result.connect(self.new_log_line)
        print('started logs')

    def new_log_line(self, lines: list[str]):
        self.ui.logsText.appendPlainText('\n'.join(lines))

    def kill_console(self):
        if self.console_proc:
            self.console_proc.kill()

        if self.logs_proc:
            self.logs_proc.kill()
