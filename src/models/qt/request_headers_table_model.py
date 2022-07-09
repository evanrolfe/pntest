from typing import Any, Optional, Union, cast
from PyQt6 import QtCore

HeaderTuple = tuple[bool, str, str]

class RequestHeadersTableModel(QtCore.QAbstractTableModel):
    # dataChanged: QtCore.pyqtSignalInstance
    # layoutChanged: QtCore.pyqtSignalInstance

    row_headers: list[str]
    headers: list[HeaderTuple]

    BLANK_ROW = (False, '', '')

    def __init__(self, headers: list[HeaderTuple], parent: Optional[QtCore.QObject] = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.row_headers = ['', 'Header', 'Value']
        self.headers = headers
        self.insert_blank_row()

    def insert_blank_row(self):
        count = len(self.headers)
        self.beginInsertRows(QtCore.QModelIndex(), count, count)
        # Pass array by value
        self.headers.append(self.BLANK_ROW[:])
        self.endInsertRows()

    def set_headers(self, headers: list[HeaderTuple]):
        self.headers = headers
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        self.layoutChanged.emit()

    def get_headers(self):
        header_arrays = [h[1:3] for h in self.headers if h[0] is True]
        headers = {}
        for header_arr in header_arrays:
            headers[header_arr[0]] = header_arr[1]
        return headers

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        if index.column() == 0:
            return QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled
        else:
            # TODO: Only set this on the Editor page
            # if index.row() < 2:
            #     return QtCore.Qt.ItemIsEnabled
            # else:
            return QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsEnabled

    # def roleNames(self):
    #     roles = {}
    #     for i, header in enumerate(self.row_headers):
    #         roles[QtCore.Qt.UserRole + i + 1] = header.encode()
    #     return roles

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.DisplayRole) -> Optional[str]:
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return self.row_headers[section]

        return None

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.row_headers)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.headers)

    def setData(self, index: QtCore.QModelIndex, value: Any, role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.EditRole) -> bool:
        if role == QtCore.Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            header = self.headers[index.row()]
            checked = (value == QtCore.Qt.CheckState.Checked)
            self.headers[index.row()] = (checked, header[1], header[2])
            return True

        if role == QtCore.Qt.ItemDataRole.EditRole:
            if self.is_item_blank(index) and value != '':
                self.modify_header(index.row(), 0, True)
                self.insert_blank_row()

            self.modify_header(index.row(), index.column(), value)
            return True

        return False

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if role == QtCore.Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            checked = self.headers[index.row()][0]
            if checked:
                return QtCore.Qt.CheckState.Checked
            else:
                return QtCore.Qt.CheckState.Unchecked

        if role in [QtCore.Qt.ItemDataRole.DisplayRole, QtCore.Qt.ItemDataRole.EditRole]:
            if not index.isValid():
                return None

            if index.row() >= len(self.headers) or index.column() == 0:
                return None

            return self.headers[index.row()][index.column()]

    def roleNameArray(self) -> list[str]:
        return self.row_headers

    def is_item_blank(self, index) -> bool:
        return self.headers[index.row()] == self.BLANK_ROW

    # Note: this is necessary because tuples are immutable
    def modify_header(self, row: int, col: int, value: Union[str, bool]) -> None:
        header = self.headers[row]

        if col == 0:
            new_header = (cast(bool, value), header[1], header[2])
        elif col == 1:
            new_header = (header[0], cast(str, value), header[2])
        elif col == 2:
            new_header = (header[0], header[1], cast(str, value))
        else:
            return

        self.headers[row] = new_header
