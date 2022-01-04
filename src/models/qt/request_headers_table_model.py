from typing import Any, Optional
from PySide2 import QtCore

Header = tuple[bool, str, str]

class RequestHeadersTableModel(QtCore.QAbstractTableModel):
    dataChanged: QtCore.SignalInstance
    layoutChanged: QtCore.SignalInstance

    row_headers: list[str]
    headers: list[Header]

    BLANK_ROW = (False, '', '')

    def __init__(self, headers: list[Header], parent: QtCore.QObject = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.row_headers = ['', 'Header', 'Value']
        self.headers = headers
        self.insert_blank_row()

    def insert_blank_row(self):
        count = len(self.headers)
        self.beginInsertRows(QtCore.QModelIndex(), count, count)  # type: ignore
        # Pass array by value
        self.headers.append(self.BLANK_ROW[:])
        self.endInsertRows()

    def set_headers(self, headers: list[Header]):
        self.headers = headers
        self.dataChanged.emit(QtCore.QModelIndex, QtCore.QModelIndex)
        self.layoutChanged.emit()

    def get_headers(self):
        header_arrays = [h[1:3] for h in self.headers if h[0] is True]
        headers = {}
        for header_arr in header_arrays:
            headers[header_arr[0]] = header_arr[1]
        return headers

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if index.column() == 0:
            return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled  # type: ignore
        else:
            # TODO: Only set this on the Editor page
            # if index.row() < 2:
            #     return QtCore.Qt.ItemIsEnabled
            # else:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled  # type: ignore

    # def roleNames(self):
    #     roles = {}
    #     for i, header in enumerate(self.row_headers):
    #         roles[QtCore.Qt.UserRole + i + 1] = header.encode()
    #     return roles

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt = QtCore.Qt.DisplayRole) -> Optional[str]:
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.row_headers[section]

        return None

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.row_headers)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.headers)

    def setData(self, index: QtCore.QModelIndex, value: Any, role: QtCore.Qt = QtCore.Qt.EditRole) -> bool:
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            header = self.headers[index.row()]
            checked = (value == QtCore.Qt.Checked)
            self.headers[index.row()] = (checked, header[1], header[2])
            return True

        if role == QtCore.Qt.EditRole:
            if self.is_item_blank(index) and value != '':
                self.headers[index.row()][0] = True  # type: ignore
                self.insert_blank_row()

            self.headers[index.row()][index.column()] = value  # type: ignore
            return True

        return False

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            checked = self.headers[index.row()][0]
            if checked:
                return QtCore.Qt.Checked
            else:
                return QtCore.Qt.Unchecked

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if not index.isValid():
                return None

            if index.row() > len(self.headers) or index.column() == 0:
                return None

            return self.headers[index.row()][index.column()]

    @QtCore.Slot(result="QVariantList")  # type: ignore
    def roleNameArray(self) -> list[str]:
        return self.row_headers

    def is_item_blank(self, index) -> bool:
        return self.headers[index.row()] == self.BLANK_ROW
