from typing import Optional
from PySide2 import QtCore
from models.data.http_flow import HttpFlow

class ExamplesTableModel(QtCore.QAbstractTableModel):
    headers: list[str]
    flows: list[HttpFlow]

    def __init__(self, flows: list[HttpFlow], parent: QtCore.QObject = None):
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

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if index.column() == 0 and index.row() > 0:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable  # type: ignore
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable  # type: ignore

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.headers)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.flows)

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Optional[str]:
        if role in [QtCore.Qt.EditRole, QtCore.Qt.DisplayRole]:
            if not index.isValid():
                return None

            if index.row() > len(self.flows):
                return None

            flow = self.flows[index.row()]

            if flow.is_example():
                if (index.column() == 0):
                    return flow.title
                elif (index.column() == 1):
                    return flow.response.status_code
                elif (index.column() == 2):
                    return str(len(flow.response.content))
            else:
                if (index.column() == 0):
                    return 'Original Request'
                else:
                    return None

    def setData(self, index: QtCore.QModelIndex, value: str, role: QtCore.Qt = QtCore.Qt.EditRole) -> bool:
        if role == QtCore.Qt.EditRole:
            if value != '':
                flow = self.flows[index.row()]
                flow.title = value
                flow.save()

            return True

        return False

    @QtCore.Slot(result="QVariantList")  # type: ignore
    def roleNameArray(self) -> list[str]:
        return self.headers
