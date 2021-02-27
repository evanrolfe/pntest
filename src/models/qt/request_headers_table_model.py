from PySide2 import QtCore

class RequestHeadersTableModel(QtCore.QAbstractTableModel):
    BLANK_ROW = [False, '', '']

    def __init__(self, headers, parent=None):
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

    def set_headers(self, headers):
        self.headers = headers
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        self.layoutChanged.emit()

    def get_headers(self):
        header_arrays = [h[1:3] for h in self.headers if h[0] is True]
        headers = {}
        for header_arr in header_arrays:
            headers[header_arr[0]] = header_arr[1]
        return headers

    def flags(self, index):
        if index.column() == 0:
            return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        else:
            if index.row() < 2:
                return QtCore.Qt.ItemIsEnabled
            else:
                return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled

    def roleNames(self):
        roles = {}
        for i, header in enumerate(self.row_headers):
            roles[QtCore.Qt.UserRole + i + 1] = header.encode()
        return roles

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.row_headers[section]

        return None

    def columnCount(self, parent):
        return len(self.row_headers)

    def rowCount(self, index):
        return len(self.headers)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            self.headers[index.row()][0] = (value == QtCore.Qt.Checked)
            return True

        if role == QtCore.Qt.EditRole:
            if self.is_item_blank(index) and value != '':
                self.headers[index.row()][0] = True
                self.insert_blank_row()

            self.headers[index.row()][index.column()] = value
            return True

        return False

    def data(self, index, role):
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

    @QtCore.Slot(result="QVariantList")
    def roleNameArray(self):
        return self.row_headers

    def is_item_blank(self, index):
        return self.headers[index.row()] == self.BLANK_ROW
