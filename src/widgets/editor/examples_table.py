from PyQt6 import QtCore, QtWidgets, QtGui

from views._compiled.editor.examples_table import Ui_ExamplesTable
from qt_models.examples_table_model import ExamplesTableModel
from entities.http_flow import HttpFlow

class ExamplesTable(QtWidgets.QWidget):
    example_selected = QtCore.pyqtSignal(HttpFlow)
    delete_examples = QtCore.pyqtSignal(list)
    # open_client_clicked = QtCore.pyqtSignal(Client)
    # close_client_clicked = QtCore.pyqtSignal(Client)
    # bring_to_front_client_clicked = QtCore.pyqtSignal(Client)

    def __init__(self, *args, **kwargs):
        super(ExamplesTable, self).__init__(*args, **kwargs)
        self.ui = Ui_ExamplesTable()
        self.ui.setupUi(self)

        horizontalHeader = self.ui.table.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
        horizontalHeader.setSortIndicator(0, QtCore.Qt.SortOrder.DescendingOrder)
        # self.ui.table.setSortingEnabled(True)

        # self.ui.table.setColumnWidth(2, 250)
        # self.ui.table.setColumnWidth(1, 50)
        # self.ui.table.setColumnWidth(2, 50)

        verticalHeader = self.ui.table.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        # Set row selection behaviour:
        self.ui.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        # # Set right-click behaviour:
        self.ui.table.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.table.customContextMenuRequested.connect(self.right_clicked)
        self.selected_flows = []

    def set_flow(self, flow: HttpFlow):
        self.flow = flow
        self.table_model = ExamplesTableModel([self.flow] + list(self.flow.examples))
        self.ui.table.setModel(self.table_model)
        self.ui.table.selectionModel().selectionChanged.connect(self.selection_changed)
        self.ui.table.selectionModel().selectionChanged.connect(self.set_selected_flows)

    def selection_changed(self, selected, deselected):
        try:
            selected_index = selected.indexes()[0]
            flow = self.table_model.flow_for_index(selected_index)
            self.example_selected.emit(flow)
        except IndexError:
            return

    def refresh(self):
        self.set_flow(self.flow)

    def set_selected_flows(self, selected, deselected):
        selected_q_indexes = self.ui.table.selectionModel().selectedRows()
        selected_flows = [self.table_model.flows[i.row()] for i in selected_q_indexes]
        self.selected_flows = selected_flows

    def right_clicked(self, position):
        index = self.ui.table.indexAt(position)
        index_col0 = index.siblingAtColumn(0)
        flow = self.table_model.flows[index.row()]
        menu = QtWidgets.QMenu()

        if (len(self.selected_flows) > 1):
            action = QtGui.QAction(f"Delete {len(self.selected_flows)} selected examples")
            menu.addAction(action)
            action.triggered.connect(lambda: self.delete_examples.emit(self.selected_flows))
        else:
            send_action = QtGui.QAction("Rename")
            menu.addAction(send_action)
            send_action.triggered.connect(lambda: self.ui.table.edit(index_col0))

            del_action = QtGui.QAction("Delete example")
            menu.addAction(del_action)
            del_action.triggered.connect(lambda: self.delete_examples.emit([flow]))

            if not flow.is_example():
                send_action.setEnabled(False)
                del_action.setEnabled(False)

        # NOTE: The generated types seem to be in correct, QObject does indeed have mapToGlobal() as a method
        position = self.sender().mapToGlobal(position) # type: ignore
        menu.exec(position)
