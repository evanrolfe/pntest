from typing import Optional
from PyQt6 import QtWidgets, QtCore, QtGui

class Sidebar(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(Sidebar, self).__init__(parent)
        self.setup()

    def setup(self):
        print("Setting up sidebar!")
        self.itemSelectionChanged.connect(self.selection_changed)

        self.setObjectName('sideBar')
        #self.setSelectionBehavior()
        self.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.setFlow(QtWidgets.QListView.Flow.TopToBottom)
        self.setMovement(QtWidgets.QListView.Movement.Static)
        self.setUniformItemSizes(True)
        # icon_size = QSize(52, 35)

        # Network Item
        network_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-cloud-backup-restore-50.png"), "Network", None)
        network_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'network')
        network_item.setToolTip("Network")
        self.addItem(network_item)

        # Intercept Item
        intercept_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-rich-text-converter-50.png"), "Intercept", None)
        intercept_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'intercept')
        intercept_item.setToolTip("Intercept")
        self.addItem(intercept_item)

        # Clients Item
        clients_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-browse-page-50.png"), "Clients", None)
        clients_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'clients')
        clients_item.setToolTip("Clients")
        self.addItem(clients_item)

        # Requests Item
        requests_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-compose-50.png"), "Requests", None)
        requests_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'requests')
        requests_item.setToolTip("Request Editor")
        self.addItem(requests_item)

        # Extensions Item
        # extensions_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-plus-math-50.png"), None)
        # extensions_item.setData(QtCore.Qt.UserRole, 'extensions')
        # self.addItem(extensions_item)
        self.setCurrentRow(0)

    # DO not let the user de-select from the sidebar
    def selection_changed(self):
        row = self.currentRow()
        items = self.selectedItems()

        if len(items) == 0:
            self.setCurrentRow(row)
