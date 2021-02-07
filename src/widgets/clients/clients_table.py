from PySide2 import QtCore, QtWidgets

from views._compiled.clients.ui_clients_table import Ui_ClientsTable
from lib.backend import Backend

class ClientsTable(QtWidgets.QWidget):
    client_selected = QtCore.Signal(QtCore.QItemSelection, QtCore.QItemSelection)

    def __init__(self, *args, **kwargs):
        super(ClientsTable, self).__init__(*args, **kwargs)
        self.ui = Ui_ClientsTable()
        self.ui.setupUi(self)

        horizontalHeader = self.ui.clientsTable.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        horizontalHeader.setSortIndicator(0, QtCore.Qt.DescendingOrder)
        self.ui.clientsTable.setSortingEnabled(True)

        self.ui.clientsTable.setColumnWidth(0, 50)
        self.ui.clientsTable.setColumnWidth(1, 80)
        self.ui.clientsTable.setColumnWidth(2, 400)
        self.ui.clientsTable.setColumnWidth(3, 60)

        verticalHeader = self.ui.clientsTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        # Set row selection behaviour:
        self.ui.clientsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Set right-click behaviour:
        self.ui.clientsTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.clientsTable.customContextMenuRequested.connect(
            self.right_clicked)

        self.backend = Backend.get_instance()

    def setTableModel(self, model):
        self.table_model = model
        self.ui.clientsTable.setModel(model)

        # Client Selected Signal:
        self.ui.clientsTable.selectionModel().selectionChanged.connect(self.client_selected)

    @QtCore.Slot()
    def right_clicked(self, position):
        index = self.ui.clientsTable.indexAt(position)
        client = self.table_model.clients[index.row()]

        menu = QtWidgets.QMenu()

        if client.open is True:
            bring_front_action = QtWidgets.QAction("Bring to Front")
            bring_front_action.triggered.connect(
                lambda: self.bring_to_front_client_clicked(client))

            close_action = QtWidgets.QAction("Close Client")
            close_action.triggered.connect(
                lambda: self.close_client_clicked(client))

            menu.addAction(bring_front_action)
            menu.addAction(close_action)
        else:
            action = QtWidgets.QAction("Open Client")
            menu.addAction(action)
            action.triggered.connect(lambda: self.open_client_clicked(client))

        menu.exec_(self.mapToGlobal(position))

    @QtCore.Slot()
    def open_client_clicked(self, client):
        self.backend.open_client(client.id)

    @QtCore.Slot()
    def close_client_clicked(self, client):
        self.backend.close_client(client.id)

    @QtCore.Slot()
    def bring_to_front_client_clicked(self, client):
        self.backend.bring_to_front_client(client.id)
