from typing import Dict, Optional, cast, Any
from PySide2 import QtCore

class VarsTableModel(QtCore.QAbstractTableModel):
    dataChanged: QtCore.SignalInstance
    layoutChanged: QtCore.SignalInstance

    headers: list[str]
    variables: list[str]

    def __init__(self, variables, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['Key', 'Value']
        self.variables = list(variables)

    def roleNames(self) -> Dict[int, str]:
        roles = {}
        for i, header in enumerate(self.headers):
            user_role_int = cast(int, QtCore.Qt.UserRole)
            roles[user_role_int + i + 1] = str(header.encode())
        return roles

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt = QtCore.Qt.DisplayRole) -> Optional[str]:
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.headers)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.variables)

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if role == QtCore.Qt.DisplayRole:
            if not index.isValid():
                return None

            if index.row() > len(self.variables):
                return None

            # flow = self.flows[index.row()]
            # row_values = flow.values_for_table()
            # return row_values[index.column()]
            return 'ok'

    @QtCore.Slot(result="QVariantList")  # type: ignore
    def roleNameArray(self) -> list[str]:
        return self.headers
