from typing import Optional
from PyQt6 import QtCore
from models.http_flow import HttpFlow
from repos.http_flow_repo import HttpFlowRepo

class ExamplesTableModel(QtCore.QAbstractTableModel):
    headers: list[str]
    flows: list[HttpFlow]

    def __init__(self, flows: list[HttpFlow], parent: Optional[QtCore.QObject] = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['Title', 'Status', 'Response Length']
        self.flows = flows

    def flow_for_index(self, index: QtCore.QModelIndex) -> HttpFlow:
        row = index.row()
        return self.flows[row]

    # def roleNames(self):
    #     roles = {}
    #     for i, header in enumerate(self.headers):
    #         roles[QtCore.Qt.UserRole + i + 1] = header.encode()
    #     return roles

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        if index.column() == 0 and index.row() > 0:
            return QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
        else:
            return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.DisplayRole) -> Optional[str]:
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.headers)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.flows)

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Optional[str]:
        if role in [QtCore.Qt.ItemDataRole.EditRole, QtCore.Qt.ItemDataRole.DisplayRole]:
            if not index.isValid():
                return None

            if index.row() > len(self.flows):
                return None

            flow = self.flows[index.row()]

            if flow.is_example():
                if (index.column() == 0):
                    return flow.title
                elif (index.column() == 1):
                    response = flow.response
                    if response is None:
                        return

                    return str(response.status_code)
                elif (index.column() == 2):
                    response = flow.response
                    response = flow.response
                    if response is None:
                        return

                    content = getattr(response, 'content', None)
                    if content == None:
                        return

                    return str(len(content))
            else:
                if (index.column() == 0):
                    return 'Original Request'
                else:
                    return None

    def setData(self, index: QtCore.QModelIndex, value: str, role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.EditRole) -> bool:
        if role == QtCore.Qt.ItemDataRole.EditRole:
            if value != '':
                flow = self.flows[index.row()]
                flow.title = value
                HttpFlowRepo().save(flow)

            return True

        return False

    def roleNameArray(self) -> list[str]:
        return self.headers

    def refresh(self) -> None:
        self.layoutChanged.emit()
