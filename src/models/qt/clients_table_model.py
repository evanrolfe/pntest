from typing import Optional, Union
from PySide2 import QtCore
from models.data.client import Client

class ClientsTableModel(QtCore.QAbstractTableModel):
    dataChanged: QtCore.SignalInstance
    layoutChanged: QtCore.SignalInstance
    headers: list[str]
    clients: list[Client]

    def __init__(self, clients: list[Client], parent: Optional[QtCore.QObject] = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['ID', 'Type', 'Name',
                        'Status', 'Proxy Port', 'Browser Port']
        self.clients = clients

    def set_clients(self, clients: list[Client]) -> None:
        self.clients = clients
        self.dataChanged.emit(QtCore.QModelIndex, QtCore.QModelIndex)
        self.layoutChanged.emit()

    # def roleNames(self):
    #     roles = {}
    #     for i, header in enumerate(self.headers):
    #         roles[QtCore.Qt.UserRole + i + 1] = header.encode()
    #     return roles

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int) -> Union[None, str]:
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.headers)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.clients)

    def data(self, index: QtCore.QModelIndex, role: int) -> Union[None, str]:
        if role == QtCore.Qt.DisplayRole:
            if not index.isValid():
                return None

            if index.row() > len(self.clients):
                return None

            client = self.clients[index.row()]

            if (index.column() == 0):
                return str(client.id)
            elif (index.column() == 1):
                return str(client.type)
            elif (index.column() == 2):
                return str(client.title)
            elif (index.column() == 3):
                return str(client.open_text())
            elif (index.column() == 4):
                return str(client.proxy_port)
            elif (index.column() == 5):
                return str(client.browser_port)

    @QtCore.Slot(result="QVariantList")  # type: ignore
    def roleNameArray(self) -> list[str]:
        return self.headers
