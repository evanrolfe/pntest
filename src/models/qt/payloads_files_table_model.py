from typing import Dict, Optional, cast, Any
from PyQt6 import QtCore
from models.payload_file import PayloadFile

class PayloadFilesTableModel(QtCore.QAbstractTableModel):
    payloads_changed = QtCore.pyqtSignal()

    headers: list[str]
    payloads: list[PayloadFile]

    def __init__(self, payloads, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['Key', 'File', '# Items', 'Description']
        self.payloads = list(payloads)

    def insert_payload(self, payload: PayloadFile):
        count = len(self.payloads)
        self.beginInsertRows(QtCore.QModelIndex(), count, count)
        self.payloads.append(payload)
        self.endInsertRows()
        self.payloads_changed.emit()

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
        return len(self.payloads)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        if index.column() in [0, 3]:
            return QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsEnabled

        return QtCore.Qt.ItemFlag.NoItemFlags

    def setData(self, index: QtCore.QModelIndex, value: Any, role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.EditRole) -> bool:
        col = index.column()

        if role == QtCore.Qt.ItemDataRole.EditRole and col in [0, 3]:
            payload = self.payloads[index.row()]

            if col == 0:
                payload.key = value
            elif col == 3:
                payload.description = value

            self.payloads_changed.emit()
            return True

        return False

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
            if not index.isValid():
                return None

            if index.row() > len(self.payloads):
                return None

            payload = self.payloads[index.row()]
            row_values = [
                payload.key,
                payload.file_path,
                payload.num_items,
                payload.description,
            ]
            return row_values[index.column()]

    def roleNameArray(self) -> list[str]:
        return self.headers
