from PySide2 import QtCore

from lib.backend import Backend
from models.data.network_request import NetworkRequest

class RequestsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, requests, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['ID', 'Source', 'Type', 'Method', 'Host', 'Path', 'Status', 'Modified']
        self.requests = list(requests)

        # Register callback with the backend:
        self.backend = Backend.get_instance()
        self.backend.register_callback('newRequest', self.add_request)
        self.backend.register_callback('updatedRequest', self.update_request)

    def add_request(self, request):
        rowIndex = 0
        self.beginInsertRows(QtCore.QModelIndex(), rowIndex, rowIndex)
        self.requests.insert(0, request)
        self.endInsertRows()

    def update_request(self, request):
        for i, r in enumerate(self.requests):
            if r.id == request.id:
                self.requests[i] = request

        rowIndex = self.get_index_of(request.id)
        start_index = self.index(rowIndex, 0)
        end_index = self.index(rowIndex, len(self.headers) - 1)
        self.dataChanged.emit(start_index, end_index)

    def delete_requests(self, request_ids):
        row_index = self.get_index_of(request_ids[0])
        row_index2 = self.get_index_of(request_ids[-1])

        self.beginRemoveRows(QtCore.QModelIndex(), row_index, row_index2)
        NetworkRequest.destroy(*request_ids)
        self.requests = list(filter(lambda r: r.id not in request_ids, self.requests))
        self.endRemoveRows()

    def roleNames(self):
        roles = {}
        for i, header in enumerate(self.headers):
            roles[QtCore.Qt.UserRole + i + 1] = header.encode()
        return roles

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent):
        return len(self.headers)

    def rowCount(self, index):
        return len(self.requests)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            if not index.isValid():
                return None

            if index.row() > len(self.requests):
                return None

            request = self.requests[index.row()]

            row_values = [
                request.id,
                request.client_id,
                request.request_type,
                request.method,
                request.host,
                request.path,
                request.response_status,
                request.modified()
            ]

            return row_values[index.column()]

    @QtCore.Slot(result="QVariantList")
    def roleNameArray(self):
        return self.headers

    def sort(self, column, order):
        self.sortOrder = order
        self.sortColumn = column

        if (order == QtCore.Qt.AscendingOrder):
            print(f"Sorting column {column} ASC")
        elif (order == QtCore.Qt.DescendingOrder):
            print(f"Sorting column {column} DESC")

        reverse = (order == QtCore.Qt.DescendingOrder)

        if (column == 0):
            self.requests = sorted(self.requests, key=lambda r: r.id, reverse=reverse)
        elif (column == 1):
            self.requests = sorted(self.requests, key=lambda r: int(r.client_id or 0), reverse=reverse)
        elif (column == 2):
            self.requests = sorted(self.requests, key=lambda r: r.request_type, reverse=reverse)
        elif (column == 3):
            self.requests = sorted(self.requests, key=lambda r: [r.method, r.id], reverse=reverse)
        elif (column == 4):
            self.requests = sorted(self.requests, key=lambda r: [r.host, r.id], reverse=reverse)
        elif (column == 5):
            self.requests = sorted(self.requests, key=lambda r: [r.path, r.id], reverse=reverse)
        elif (column == 6):
            self.requests = sorted(self.requests, key=self.response_status_sort_key, reverse=reverse)

        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def response_status_sort_key(self, request):
        if (request.response_status == ''):
            status = 0
        else:
            status = int(request.response_status)

        return [status, request.id]

    def refresh(self):
        self.layoutChanged.emit()

    def get_index_of(self, request_id):
        for i, r in enumerate(self.requests):
            if r.id == request_id:
                return i
