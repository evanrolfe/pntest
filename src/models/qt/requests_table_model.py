from typing import Dict, Optional, cast, Any
from PySide2 import QtCore

from models.data.http_flow import HttpFlow

class RequestsTableModel(QtCore.QAbstractTableModel):
    dataChanged: QtCore.SignalInstance
    layoutChanged: QtCore.SignalInstance

    headers: list[str]
    flow: list[HttpFlow]

    def __init__(self, flows, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['ID', 'Source', 'Type', 'Method', 'Host', 'Path', 'Status', 'Modified']
        self.flows = list(flows)

    def add_flow(self, flow: HttpFlow) -> None:
        rowIndex = 0
        # TODO: Use self.index() here
        self.beginInsertRows(QtCore.QModelIndex(), rowIndex, rowIndex)  # type: ignore
        self.flows.insert(0, flow)
        self.endInsertRows()

    def update_flow(self, flow: HttpFlow) -> None:
        for i, r in enumerate(self.flows):
            if r.id == flow.id:
                self.flows[i] = flow

        row_index = self.get_index_of(flow.id)

        if row_index is None:
            return

        start_index = self.index(row_index, 0)
        end_index = self.index(row_index, len(self.headers) - 1)
        self.dataChanged.emit(start_index, end_index)

    def delete_requests(self, request_ids: list[int]) -> None:
        row_index = self.get_index_of(request_ids[0])
        row_index2 = self.get_index_of(request_ids[-1])

        self.beginRemoveRows(QtCore.QModelIndex(), row_index, row_index2)  # type: ignore
        HttpFlow.destroy(*request_ids)
        self.flows = list(filter(lambda r: r.id not in request_ids, self.flows))
        self.endRemoveRows()

    def roleNames(self) -> Dict[int, str]:
        roles = {}
        for i, header in enumerate(self.headers):
            user_role_int = cast(int, QtCore.Qt.UserRole)
            roles[user_role_int + i + 1] = str(header.encode())
        return roles

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.headers)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.flows)

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if role == QtCore.Qt.DisplayRole:
            if not index.isValid():
                return None

            if index.row() > len(self.flows):
                return None

            flow = self.flows[index.row()]

            row_values = flow.values_for_table()

            return row_values[index.column()]

    @QtCore.Slot(result="QVariantList")  # type: ignore
    def roleNameArray(self) -> list[str]:
        return self.headers

    def sort(self, column: int, order: QtCore.Qt.SortOrder) -> None:
        self.sortOrder = order
        self.sortColumn = column

        if (order == QtCore.Qt.AscendingOrder):
            print(f"Sorting column {column} ASC")
        elif (order == QtCore.Qt.DescendingOrder):
            print(f"Sorting column {column} DESC")

        reverse = (order == QtCore.Qt.DescendingOrder)

        if (column == 0):
            self.flows = sorted(self.flows, key=lambda flow: flow.id, reverse=reverse)
        elif (column == 1):
            self.flows = sorted(self.flows, key=lambda flow: int(flow.client_id or 0), reverse=reverse)
        elif (column == 2):
            self.flows = sorted(self.flows, key=lambda flow: flow.request.scheme, reverse=reverse)
        elif (column == 3):
            self.flows = sorted(self.flows, key=lambda flow: [flow.request.method, flow.id], reverse=reverse)
        elif (column == 4):
            self.flows = sorted(self.flows, key=lambda flow: [flow.request.host, flow.id], reverse=reverse)
        elif (column == 5):
            self.flows = sorted(self.flows, key=lambda flow: [flow.request.path, flow.id], reverse=reverse)
        elif (column == 6):
            self.flows = sorted(self.flows, key=self.response_status_sort_key, reverse=reverse)

        self.dataChanged.emit(QtCore.QModelIndex, QtCore.QModelIndex)

    def response_status_sort_key(self, flow: HttpFlow) -> tuple[int, int]:
        if flow.has_response():
            status = flow.response.status_code
        else:
            status = 0

        return (status, flow.id)

    def refresh(self) -> None:
        self.layoutChanged.emit()

    def get_index_of(self, request_id: int) -> Optional[int]:
        for i, r in enumerate(self.flows):
            if r.id == request_id:
                return i
