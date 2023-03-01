from typing import Any, Optional, Union

from PyQt6 import QtCore

from entities.client import Client
from repos.client_repo import ClientRepo


class ClientsTableModel(QtCore.QAbstractTableModel):
    # dataChanged: QtCore.SignalInstance
    # layoutChanged: QtCore.SignalInstance
    headers: list[str]
    clients: list[Client]

    def __init__(self, clients: list[Client], parent: Optional[QtCore.QObject] = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['ID', 'Type', 'Name',
                        'Status', 'Proxy Port']
        self.clients = clients

    def set_clients(self, clients: list[Client]) -> None:
        self.clients = clients
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        self.layoutChanged.emit()

    def reload(self):
        clients = ClientRepo().find_all()
        self.set_clients(clients)

    # def roleNames(self):
    #     roles = {}
    #     for i, header in enumerate(self.headers):
    #         roles[QtCore.Qt.UserRole + i + 1] = header.encode()
    #     return roles

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int) -> Union[None, str]:
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.headers)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.clients)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        if index.column() == 2:
            return QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled
        else:
            return QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled

    def data(self, index: QtCore.QModelIndex, role: int) -> Union[None, str]:
        if role in [QtCore.Qt.ItemDataRole.DisplayRole, QtCore.Qt.ItemDataRole.EditRole]:
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

    def setData(self, index: QtCore.QModelIndex, value: str, role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.EditRole) -> bool:
        if role == QtCore.Qt.ItemDataRole.EditRole:
            client = self.clients[index.row()]
            client.title = value
            ClientRepo().save(client)

            return True

        return False

    def roleNameArray(self) -> list[str]:
        return self.headers
