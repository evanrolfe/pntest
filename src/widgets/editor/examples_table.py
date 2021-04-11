from PySide2 import QtCore, QtWidgets

from views._compiled.editor.ui_examples_table import Ui_ExamplesTable
from models.qt.examples_table_model import ExamplesTableModel
from models.data.http_flow import HttpFlow

class ExamplesTable(QtWidgets.QWidget):
    example_selected = QtCore.Signal(HttpFlow)
    # open_client_clicked = QtCore.Signal(Client)
    # close_client_clicked = QtCore.Signal(Client)
    # bring_to_front_client_clicked = QtCore.Signal(Client)

    def __init__(self, *args, **kwargs):
        super(ExamplesTable, self).__init__(*args, **kwargs)
        self.ui = Ui_ExamplesTable()
        self.ui.setupUi(self)

        horizontalHeader = self.ui.table.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        horizontalHeader.setSortIndicator(0, QtCore.Qt.DescendingOrder)
        # self.ui.table.setSortingEnabled(True)

        self.ui.table.setColumnWidth(0, 50)
        self.ui.table.setColumnWidth(1, 150)
        self.ui.table.setColumnWidth(2, 50)

        verticalHeader = self.ui.table.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        # Set row selection behaviour:
        self.ui.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # # Set right-click behaviour:
        # self.ui.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.ui.table.customContextMenuRequested.connect(self.right_clicked)

    def set_flow(self, flow):
        self.table_model = ExamplesTableModel(flow.examples)
        self.ui.table.setModel(self.table_model)
        self.ui.table.selectionModel().selectionChanged.connect(self.selection_changed)

    @QtCore.Slot()
    def selection_changed(self, selected, deselected):
        selected_index = selected.indexes()[0]
        flow = self.table_model.flow_for_index(selected_index)
        self.example_selected.emit(flow)

    # @QtCore.Slot()
    # def right_clicked(self, position):
    #     index = self.ui.table.indexAt(position)
    #     client = self.table_model.clients[index.row()]
    #     menu = QtWidgets.QMenu()

    #     if client.open == 1:
    #         bring_front_action = QtWidgets.QAction("Bring to Front")
    #         bring_front_action.triggered.connect(lambda: self.bring_to_front_client_clicked.emit(client))

    #         close_action = QtWidgets.QAction("Close Client")
    #         close_action.triggered.connect(lambda: self.close_client_clicked.emit(client))

    #         menu.addAction(bring_front_action)
    #         menu.addAction(close_action)
    #     else:
    #         action = QtWidgets.QAction("Open Client")
    #         menu.addAction(action)
    #         action.triggered.connect(lambda: self.open_client_clicked.emit(client))

    #     menu.exec_(self.mapToGlobal(position))
