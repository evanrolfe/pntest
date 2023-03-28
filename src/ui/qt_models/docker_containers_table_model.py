from typing import Any, Optional, Union

from PyQt6 import QtCore

from entities.container import Container
from entities.network import Network
from repos.container_repo import ContainerRepo


class DockerContainersTableModel(QtCore.QAbstractTableModel):
    headers: list[str]
    containers: list[Container]
    network: Network

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['ID', 'Host', 'Name', 'Status', 'Gateway Configured?']
        self.containers = []

    def set_network(self, network: Network):
        self.network = network
        self.reload()

    def reload(self):
        self.containers = ContainerRepo.get_instance().find_by_ids(self.network.container_ids())
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        self.layoutChanged.emit()

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
        return len(self.containers)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        return QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled

    def data(self, index: QtCore.QModelIndex, role: int) -> Union[None, str]:
        if role in [QtCore.Qt.ItemDataRole.DisplayRole, QtCore.Qt.ItemDataRole.EditRole]:
            if not index.isValid():
                return None

            if index.row() > len(self.containers):
                return None

            container = self.containers[index.row()]

            if (index.column() == 0):
                return str(container.short_id)
            elif (index.column() == 1):
                return str(container.host_name)
            elif (index.column() == 2):
                return str(container.name)
            elif (index.column() == 3):
                return str(container.status)
            elif (index.column() == 4):
                return str('Yes')

    def roleNameArray(self) -> list[str]:
        return self.headers
