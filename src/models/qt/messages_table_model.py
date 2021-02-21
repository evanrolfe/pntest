from PySide2 import QtCore

from lib.utils import format_timestamp
from lib.backend import Backend
from models.data.websocket_message import WebsocketMessage

class MessagesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, messages, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['ID', 'Request', 'Direction', 'Time']
        self.messages = list(messages)

        # Register callback with the backend:
        # self.backend = Backend.get_instance()
        # self.backend.register_callback('newRequest', self.add_request)
        # self.backend.register_callback('updatedRequest', self.update_request)

    # def add_request(self, request):
    #     rowIndex = 0
    #     self.beginInsertRows(QtCore.QModelIndex(), rowIndex, rowIndex)
    #     self.messages.insert(0, request)
    #     self.endInsertRows()

    # def update_request(self, request):
    #     for i, r in enumerate(self.messages):
    #         if r.id == request.id:
    #             self.messages[i] = request

    #     rowIndex = self.get_index_of(request.id)
    #     start_index = self.index(rowIndex, 0)
    #     end_index = self.index(rowIndex, len(self.headers) - 1)
    #     self.dataChanged.emit(start_index, end_index)

    def delete_messages(self, message_ids):
        row_index = self.get_index_of(message_ids[0])
        row_index2 = self.get_index_of(message_ids[-1])

        self.beginRemoveRows(QtCore.QModelIndex(), row_index, row_index2)
        WebsocketMessage.destroy(*message_ids)
        self.messages = list(filter(lambda r: r.id not in message_ids, self.messages))
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
        return len(self.messages)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            if not index.isValid():
                return None

            if index.row() > len(self.messages):
                return None

            message = self.messages[index.row()]

            row_values = [
                message.id,
                message.request_id,
                message.direction,
                format_timestamp(message.created_at)
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
            self.messages = sorted(self.messages, key=lambda r: r.id, reverse=reverse)
        elif (column == 1):
            self.messages = sorted(self.messages, key=lambda r: int(r.request_id or 0), reverse=reverse)
        elif (column == 2):
            self.messages = sorted(self.messages, key=lambda r: r.direction, reverse=reverse)
        elif (column == 3):
            self.messages = sorted(self.messages, key=lambda r: r.created_at, reverse=reverse)

        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def refresh(self):
        self.layoutChanged.emit()

    def get_index_of(self, request_id):
        for i, r in enumerate(self.messages):
            if r.id == request_id:
                return i
