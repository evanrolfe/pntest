from typing import Optional, cast

from PyQt6 import QtCore, QtGui, QtWidgets

from entities.container import Container
from entities.network import Network
from ui.widgets.docker.docker_tab import DockerTab


class DockerTabs(QtWidgets.QTabWidget):
    blank_item_has_been_opened = False

    def __init__(self, *args, **kwargs):
        super(DockerTabs, self).__init__(*args, **kwargs)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setIconSize(QtCore.QSize(20, 12))

    def open_tab(self, network: Network, container: Container):
        tab = DockerTab(self)
        tab.set_container(network, container)
        self.addTab(tab, container.host_name)
        self.setCurrentIndex(self.count() - 1)

    def kill_consoles(self):
        for i in range(0, self.count()):
            tab = self.get_page_for_tab(i)
            tab.kill_console()

    def get_page_for_tab(self, index: int) -> DockerTab:
        return cast(DockerTab, self.widget(index))

