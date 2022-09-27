from PyQt6 import QtCore, QtWidgets, QtGui
from models.qt.requests_table_model import RequestsTableModel

from views._compiled.network.http.requests_table import Ui_RequestsTable
from widgets.network.http.display_filters import DisplayFilters
from widgets.network.http.capture_filters import CaptureFilters
from widgets.qt.row_style_delegate import RowStyleDelegate
from models.data.http_flow import HttpFlow

class RequestsTable(QtWidgets.QWidget):
    request_selected = QtCore.pyqtSignal(QtCore.QItemSelection, QtCore.QItemSelection)
    delete_requests = QtCore.pyqtSignal(list)
    search_text_changed = QtCore.pyqtSignal(str)
    send_flow_to_editor = QtCore.pyqtSignal(HttpFlow)
    display_filters_saved = QtCore.pyqtSignal()

    table_model: RequestsTableModel

    def __init__(self, *args, **kwargs):
        super(RequestsTable, self).__init__(*args, **kwargs)
        self.ui = Ui_RequestsTable()
        self.ui.setupUi(self)

        horizontalHeader = self.ui.requestsTable.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
        horizontalHeader.setSortIndicator(0, QtCore.Qt.SortOrder.DescendingOrder)
        horizontalHeader.setHighlightSections(False)
        # horizontalHeader.setCursor(QtCore.Qt.PointingHandCursor)

        verticalHeader = self.ui.requestsTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        self.ui.requestsTable.setSortingEnabled(True)
        self.ui.requestsTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.ui.requestsTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Enable row hover styling:
        delegate = RowStyleDelegate(self.ui.requestsTable)
        self.ui.requestsTable.setMouseTracking(True)
        self.ui.requestsTable.setItemDelegate(delegate)
        # self.ui.requestsTable.viewport().update()
        self.ui.requestsTable.hover_index_changed.connect(delegate.highlight_index)

        # Search box:
        self.ui.searchBox.returnPressed.connect(self.search_text_edited)

        # Display & Capture Filters:
        self.network_display_filters = DisplayFilters(self)
        self.network_display_filters.display_filters_saved.connect(self.display_filters_saved)
        self.ui.displayFiltersButton.clicked.connect(lambda: self.network_display_filters.show())

        self.network_capture_filters = CaptureFilters(self)
        self.ui.captureFiltersButton.clicked.connect(lambda: self.network_capture_filters.show())

        # Set row selection behaviour:
        self.ui.requestsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        # Set right-click behaviour:
        self.ui.requestsTable.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.requestsTable.customContextMenuRequested.connect(self.right_clicked)
        self.selected_request_ids = []

        # SiteMap button
        icon = QtGui.QIcon("assets:icons/dark/icons8-sitemap-32.png")
        self.ui.siteMapButton.setIcon(icon)
        self.ui.siteMapButton.setIconSize(QtCore.QSize(25, 25))
        self.ui.siteMapButton.setText(">>")

    def setTableModel(self, model: RequestsTableModel):
        self.table_model = model
        self.ui.requestsTable.setModel(model)

        # Request Selected Signal:
        self.ui.requestsTable.selectionModel().selectionChanged.connect(self.request_selected)
        self.ui.requestsTable.selectionModel().selectionChanged.connect(self.set_selected_requests)

        self.ui.requestsTable.setColumnWidth(0, 50)
        self.ui.requestsTable.setColumnWidth(1, 50)
        self.ui.requestsTable.setColumnWidth(2, 50)
        self.ui.requestsTable.setColumnWidth(3, 60)
        self.ui.requestsTable.setColumnWidth(4, 150)
        self.ui.requestsTable.setColumnWidth(5, 250)
        self.ui.requestsTable.setColumnWidth(6, 50)
        self.ui.requestsTable.setColumnWidth(7, 70)

    def set_selected_requests(self, selected, deselected):
        selected_q_indexes = self.ui.requestsTable.selectionModel().selectedRows()
        self.selected_request_ids = list(map(lambda index: index.data(), selected_q_indexes))

    def right_clicked(self, position: QtCore.QPoint):
        index = self.ui.requestsTable.indexAt(position)
        flow = self.table_model.flows[index.row()]

        menu = QtWidgets.QMenu()

        if (len(self.selected_request_ids) > 1):
            action = QtGui.QAction(f"Delete {len(self.selected_request_ids)} selected requests")
            menu.addAction(action)
            action.triggered.connect(lambda: self.delete_requests.emit(self.selected_request_ids))
        else:
            if flow.is_editable():
                send_action = QtGui.QAction("Send to editor")
                menu.addAction(send_action)
                send_action.triggered.connect(lambda: self.send_flow_to_editor.emit(flow))

            action = QtGui.QAction("Delete request")
            menu.addAction(action)
            action.triggered.connect(lambda: self.delete_requests.emit([flow.id]))

        # NOTE: The generated types seem to be in correct, QObject does indeed have mapToGlobal() as a method
        position = self.sender().mapToGlobal(position) # type: ignore
        menu.exec(position)

    def display_filters_clicked(self):
        print("You clicked me!")

    def search_text_edited(self):
        self.search_text_changed.emit(self.ui.searchBox.text())
