from typing import Dict, Optional, cast, Any
from PyQt6 import QtCore
from entities.variable import Variable

class VarsTableModel(QtCore.QAbstractTableModel):
    # dataChanged: QtCore.pyqtSignalInstance
    # layoutChanged: QtCore.pyqtSignalInstance

    headers: list[str]
    variables: list[Variable]

    def __init__(self, variables: list[Variable], parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['Key', 'Value', 'Description']
        self.variables = list(variables)
        self.insert_blank_row()

    def insert_blank_row(self):
        count = len(self.variables)
        self.beginInsertRows(QtCore.QModelIndex(), count, count)
        # Pass array by value
        blank_var = Variable.build_blank_global()
        self.variables.append(blank_var)
        self.endInsertRows()

    def roleNames(self) -> Dict[int, str]:
        roles = {}
        for i, header in enumerate(self.headers):
            user_role_int = cast(int, QtCore.Qt.ItemDataRole.UserRole)
            roles[user_role_int + i + 1] = str(header.encode())
        return roles

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.DisplayRole) -> Optional[str]:
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.headers)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.variables)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        return QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsEnabled

    def setData(self, index: QtCore.QModelIndex, value: Any, role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.EditRole) -> bool:
        if role == QtCore.Qt.ItemDataRole.EditRole:
            var = self.variables[index.row()]

            if var.is_blank() and value != '':
                self.insert_blank_row()

            columns = ['key', 'value', 'description']
            field = columns[index.column()]
            setattr(var, field, value)

            return True

        return False

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
            if not index.isValid():
                return None

            if index.row() > len(self.variables):
                return None

            var = self.variables[index.row()]
            row_values = [
                getattr(var, 'key', ''),
                getattr(var, 'value', ''),
                getattr(var, 'description', '')
            ]
            return row_values[index.column()]

    def roleNameArray(self) -> list[str]:
        return self.headers

    def is_item_blank(self, index) -> bool:
        return self.variables[index.row()].is_blank()
