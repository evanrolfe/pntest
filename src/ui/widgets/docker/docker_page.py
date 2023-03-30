import time
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets

from entities.container import Container
from entities.http_flow import HttpFlow
from entities.network import Network
from repos.container_repo import ContainerRepo
from repos.http_flow_repo import HttpFlowRepo
from repos.network_repo import NetworkRepo
from repos.ws_message_repo import WsMessageRepo
from services.docker_service import DockerService
from services.intercept_queue import InterceptQueue
from ui.qt_models.docker_containers_table_model import \
    DockerContainersTableModel
from ui.views._compiled.docker.docker_page import Ui_DockerPage
from ui.widgets.docker.console_proc import NUM_LINES, ConsoleProc


class ContainerRowStyleDelegate(QtWidgets.QStyledItemDelegate):
    HOVER_COLOUR = "#252526"

    hovered_index: QtCore.QModelIndex
    prev_hovered_index: QtCore.QModelIndex
    hover_background: QtGui.QBrush

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super(ContainerRowStyleDelegate, self).__init__(parent=None)
        self.parent = parent # type:ignore
        self.hovered_index = QtCore.QModelIndex()

    def highlight_index(self, index: QtCore.QModelIndex):
        self.hovered_index = index
        self.parent.viewport().update()

    # https://stackoverflow.com/questions/20565930/qtableview-how-can-i-highlight-the-entire-row-for-mouse-hover
    def initStyleOption(self, options: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        super().initStyleOption(options, index)
        # options.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter
        if self.hovered_index.row() == index.row():
            options.backgroundBrush = QtGui.QBrush(QtGui.QColor(self.HOVER_COLOUR))

    def paint(self, painter: QtGui.QPainter, options: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        super().paint(painter, options, index)

        model: DockerContainersTableModel = index.model()  # type: ignore
        container = model.get_container(index)

        # Response status column
        if index.column() == 4:
            if container is None:
                return

            if container.interception_active:
                label_text = "Active"
                bg_color = "#3B6118"
            else:
                label_text = "Inactive"
                bg_color = "#7A4C15"

            label = QtWidgets.QLabel(label_text)
            label.setAutoFillBackground(True)
            label.setObjectName("responseStatusLabelTable")
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setMinimumWidth(30)
            label.setStyleSheet(f"background-color: {bg_color};")
            # painter.fillRect(options.rect, QtGui.QColor("#C3E88D"))
            x_offest = 9
            y_offset = 0
            painter.drawPixmap(options.rect.x()+x_offest, options.rect.y()+y_offset, label.grab())

class DockerPage(QtWidgets.QWidget):
    networks: list[Network]
    network: Network

    def __init__(self, *args, **kwargs):
        super(DockerPage, self).__init__(*args, **kwargs)
        self.ui = Ui_DockerPage()
        self.ui.setupUi(self)

        self.ui.refreshButton.setIcon(QtGui.QIcon('assets:icons/dark/icons8-refresh-64.png'))

        # Setup Table
        horizontalHeader = self.ui.containerTable.horizontalHeader()
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
        horizontalHeader.setSortIndicator(0, QtCore.Qt.SortOrder.DescendingOrder)
        horizontalHeader.setHighlightSections(False)

        verticalHeader = self.ui.containerTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        verticalHeader.setVisible(False)
        verticalHeader.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # NOTE: I've disabled sorting for now because it needs more work to get it with fetchMore() from containerTableModel
        self.ui.containerTable.setSortingEnabled(False)
        self.ui.containerTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.ui.containerTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Enable row hover styling:
        delegate = ContainerRowStyleDelegate(self.ui.containerTable)
        self.ui.containerTable.setMouseTracking(True)
        self.ui.containerTable.setItemDelegate(delegate)
        self.ui.containerTable.hover_index_changed.connect(delegate.highlight_index)

        # Set row selection behaviour:
        self.ui.containerTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.containerTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        # Load table model
        self.table_model = DockerContainersTableModel()
        self.ui.containerTable.setModel(self.table_model)

        self.load_networks()

        # Request Selected Signal:
        self.ui.containerTable.selectionModel().selectionChanged.connect(self.container_selected)

        # TODO: Save the column widths to AppSettings
        self.ui.containerTable.setColumnWidth(0, 100)
        self.ui.containerTable.setColumnWidth(1, 150)
        self.ui.containerTable.setColumnWidth(2, 159)
        self.ui.containerTable.setColumnWidth(3, 80)
        self.ui.containerTable.setColumnWidth(4, 120)

        horizontalHeader = self.ui.containerTable.horizontalHeader()
        horizontalHeader.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Fixed)
        horizontalHeader.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Interactive)
        horizontalHeader.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        horizontalHeader.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Interactive)
        horizontalHeader.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Fixed)

        self.ui.dockerNetworkDropdown.currentIndexChanged.connect(self.network_selected)

    def load_networks(self):
        self.networks = NetworkRepo().get_all()

        for network in self.networks:
            self.ui.dockerNetworkDropdown.addItem(network.name)

        if len(self.networks) > 0:
            self.network_selected(0)

    def network_selected(self, index: int):
        self.network = self.networks[index]
        DockerService().load_containers_to_network(self.network)
        print("GATEWAY CONTAINER: ", self.network.gateway_container())

        self.table_model.set_network(self.network)

        # self.ui.dockerTab.ui.networkText.setPlainText(network.human_readable_desc())

    def container_selected(self, selected, deselected):
        selected_q_indexes = self.ui.containerTable.selectionModel().selectedRows()
        # TODO: Make this a method on the table model
        selected_containers = [self.table_model.containers[i.row()] for i in selected_q_indexes]

        if len(selected_containers) == 0:
            return

        container = selected_containers[0]
        print("CONTAINER HAS TOOLS? ", container.has_tools_installed())
        # self.ui.dockerTab.ui.containerText.setPlainText(container.human_readable_desc())
        self.ui.tabs.open_tab(self.network, container)
        # self.setup_console(container)

    def kill_console(self):
        self.ui.tabs.kill_consoles()
