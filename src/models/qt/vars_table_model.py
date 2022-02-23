from typing import Dict, Optional, cast, Any
from PySide2 import QtCore
from models.data.variable import Variable

class VarsTableModel(QtCore.QAbstractTableModel):
    dataChanged: QtCore.SignalInstance
    layoutChanged: QtCore.SignalInstance

    headers: list[str]
    variables: list[Variable]

    def __init__(self, variables, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['Key', 'Value', 'Description']
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

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled  # type: ignore

    def setData(self, index: QtCore.QModelIndex, value: Any, role: QtCore.Qt = QtCore.Qt.EditRole) -> bool:
        if role == QtCore.Qt.EditRole:
            var = self.variables[index.row()]
            columns = ['key', 'value', 'description']
            field = columns[index.column()]
            setattr(var, field, value)
            return True

        return False

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if not index.isValid():
                return None

            if index.row() > len(self.variables):
                return None

            var = self.variables[index.row()]
            row_values = [var.key, var.value, var.description]
            return row_values[index.column()]

    @QtCore.Slot(result="QVariantList")  # type: ignore
    def roleNameArray(self) -> list[str]:
        return self.headers
