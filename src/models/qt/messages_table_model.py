from typing import Any, Optional
from PyQt6 import QtCore

from lib.utils import format_timestamp
from models.websocket_message import WebsocketMessage
from repos.ws_message_repo import WsMessageRepo

class MessagesTableModel(QtCore.QAbstractTableModel):
    # dataChanged: QtCore.pyqtSignalInstance
    # layoutChanged: QtCore.pyqtSignalInstance

    headers: list[str]
    messages: list[WebsocketMessage]

    def __init__(self, messages: list[WebsocketMessage], parent: Optional[QtCore.QObject] = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['ID', 'Request', 'Direction', 'Time', 'Modified']
        self.messages = list(messages)

    def add_message(self, message: WebsocketMessage) -> None:
        rowIndex = 0
        self.beginInsertRows(QtCore.QModelIndex(), rowIndex, rowIndex)
        self.messages.insert(0, message)
        self.endInsertRows()

    # def update_request(self, request):
    #     for i, r in enumerate(self.messages):
    #         if r.id == request.id:
    #             self.messages[i] = request

    #     rowIndex = self.get_index_of(request.id)
    #     start_index = self.index(rowIndex, 0)
    #     end_index = self.index(rowIndex, len(self.headers) - 1)
    #     self.dataChanged.emit(start_index, end_index)

    def delete_messages(self, message_ids: list[int]) -> None:
        row_index = self.get_index_of(message_ids[0])
        row_index2 = self.get_index_of(message_ids[-1])

        if row_index is None or row_index2 is None:
            return

        self.beginRemoveRows(QtCore.QModelIndex(), row_index, row_index2)
        [WsMessageRepo().delete(m) for m in self.messages if m.id in message_ids]

        self.messages = list(filter(lambda r: r.id not in message_ids, self.messages))
        self.endRemoveRows()

    # def roleNames(self):
    #     roles = {}
    #     for i, header in enumerate(self.headers):
    #         roles[QtCore.Qt.UserRole + i + 1] = header.encode()
    #     return roles

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt.ItemDataRole = QtCore.Qt.ItemDataRole.DisplayRole) -> Optional[str]:
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent: Optional[QtCore.QObject] = None) -> int:
        return len(self.headers)

    def rowCount(self, parent: Optional[QtCore.QObject] = None) -> int:
        return len(self.messages)

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if not index.isValid():
                return None

            if index.row() > len(self.messages):
                return None

            message = self.messages[index.row()]

            row_values = [
                message.id,
                message.http_flow_id,
                message.direction,
                format_timestamp(message.created_at),
                message.modified()
            ]

            return row_values[index.column()]

    def roleNameArray(self) -> list[str]:
        return self.headers

    def sort(self, column: int, order: QtCore.Qt.SortOrder) -> None:
        self.sortOrder = order
        self.sortColumn = column

        if (order == QtCore.Qt.SortOrder.AscendingOrder):
            print(f"Sorting column {column} ASC")
        elif (order == QtCore.Qt.SortOrder.DescendingOrder):
            print(f"Sorting column {column} DESC")

        reverse = (order == QtCore.Qt.SortOrder.DescendingOrder)

        if (column == 0):
            self.messages = sorted(self.messages, key=lambda r: r.id, reverse=reverse)
        elif (column == 1):
            self.messages = sorted(self.messages, key=lambda r: int(r.http_flow_id or 0), reverse=reverse)
        elif (column == 2):
            self.messages = sorted(self.messages, key=lambda r: r.direction, reverse=reverse)
        elif (column == 3):
            self.messages = sorted(self.messages, key=lambda r: r.created_at, reverse=reverse)

        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def refresh(self) -> None:
        self.layoutChanged.emit()

    def get_index_of(self, http_flow_id: int) -> Optional[int]:
        for i, r in enumerate(self.messages):
            if r.id == http_flow_id:
                return i
