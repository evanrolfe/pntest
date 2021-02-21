from PySide2 import QtCore, QtWidgets

from views._compiled.network.ws.ui_messages_table import Ui_MessagesTable
from widgets.network.http.display_filters import DisplayFilters
from widgets.qt.row_style_delegate import RowStyleDelegate

class MessagesTable(QtWidgets.QWidget):
    request_selected = QtCore.Signal(QtCore.QItemSelection, QtCore.QItemSelection)
    delete_requests = QtCore.Signal(list)
    search_text_changed = QtCore.Signal(str)
    send_request_to_editor = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(MessagesTable, self).__init__(*args, **kwargs)
        self.ui = Ui_MessagesTable()
        self.ui.setupUi(self)

        horizontalHeader = self.ui.messagesTable.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        horizontalHeader.setSortIndicator(0, QtCore.Qt.DescendingOrder)
        horizontalHeader.setHighlightSections(False)
        # horizontalHeader.setCursor(QtCore.Qt.PointingHandCursor)

        verticalHeader = self.ui.messagesTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        self.ui.messagesTable.setSortingEnabled(True)
        self.ui.messagesTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.ui.messagesTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        # Enable row hover styling:
        delegate = RowStyleDelegate(self.ui.messagesTable)
        self.ui.messagesTable.setMouseTracking(True)
        self.ui.messagesTable.setItemDelegate(delegate)
        # self.ui.messagesTable.viewport().update()
        self.ui.messagesTable.hover_index_changed.connect(delegate.highlight_index)

        # Search box:
        self.ui.searchBox.textEdited.connect(self.search_text_edited)

        # Display & Capture Filters:
        self.network_display_filters = DisplayFilters(self)
        self.ui.displayFiltersButton.clicked.connect(lambda: self.network_display_filters.show())

        # Set row selection behaviour:
        self.ui.messagesTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Set right-click behaviour:
        self.ui.messagesTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.messagesTable.customContextMenuRequested.connect(
            self.right_clicked)
        self.selected_request_ids = []

    def setTableModel(self, model):
        self.table_model = model
        self.ui.messagesTable.setModel(model)

        # Request Selected Signal:
        self.ui.messagesTable.selectionModel().selectionChanged.connect(self.request_selected)
        self.ui.messagesTable.selectionModel().selectionChanged.connect(self.set_selected_requests)

        self.ui.messagesTable.setColumnWidth(0, 50)
        self.ui.messagesTable.setColumnWidth(1, 80)
        self.ui.messagesTable.setColumnWidth(2, 80)
        self.ui.messagesTable.setColumnWidth(3, 80)

    @QtCore.Slot()
    def set_selected_requests(self, selected, deselected):
        selected_q_indexes = self.ui.messagesTable.selectionModel().selectedRows()
        self.selected_request_ids = list(map(lambda index: index.data(), selected_q_indexes))

    @QtCore.Slot()
    def right_clicked(self, position):
        index = self.ui.messagesTable.indexAt(position)
        request = self.table_model.requests[index.row()]

        menu = QtWidgets.QMenu()

        if (len(self.selected_request_ids) > 1):
            action = QtWidgets.QAction(f"Delete {len(self.selected_request_ids)} selected requests")
            menu.addAction(action)
            action.triggered.connect(lambda: self.delete_requests.emit(self.selected_request_ids))
        else:
            # if request.is_editable():
            #     send_action = QtWidgets.QAction("Send to editor")
            #     menu.addAction(send_action)
            #     send_action.triggered.connect(lambda: self.send_request_to_editor.emit(request))

            action = QtWidgets.QAction("Delete request")
            menu.addAction(action)
            action.triggered.connect(lambda: self.delete_requests.emit([request.id]))

        menu.exec_(self.sender().mapToGlobal(position))

    @QtCore.Slot()
    def display_filters_clicked(self):
        print("You clicked me!")

    @QtCore.Slot()
    def search_text_edited(self, new_text):
        self.search_text_changed.emit(new_text)
