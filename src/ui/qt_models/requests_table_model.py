from typing import Any, Dict, Optional, cast

from PyQt6 import QtCore

from entities.http_flow import HttpFlow
from services.http_flow_service import HttpFlowService

BATCH_SIZE = 100

# TODO: Rename this to FlowsTableModel
class RequestsTableModel(QtCore.QAbstractTableModel):
    # dataChanged: QtCore.pyqtSignalInstance
    # layoutChanged: QtCore.pyqtSignalInstance

    headers: list[str]
    flows: list[HttpFlow]

    offset: int
    limit: int
    total_count: int

    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['ID', 'Source', 'Type', 'Method', 'Host', 'Path', 'Status', 'Modified']

        self.offset = 0
        self.limit = BATCH_SIZE
        self.flows, self.total_count = HttpFlowService().find_for_table('', self.offset, self.limit)

    def add_flow(self, flow: HttpFlow) -> None:
        rowIndex = 0
        # TODO: Use self.index() here
        self.beginInsertRows(QtCore.QModelIndex(), rowIndex, rowIndex)
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

    def delete_requests(self, flow_ids: list[int]) -> None:
        row_index = self.get_index_of(flow_ids[0])
        row_index2 = self.get_index_of(flow_ids[-1])

        if row_index is None or row_index2 is None:
            return

        self.beginRemoveRows(QtCore.QModelIndex(), row_index, row_index2)
        [HttpFlowService().delete(f) for f in self.flows if f.id in flow_ids]

        self.flows = list(filter(lambda r: r.id not in flow_ids, self.flows))
        self.endRemoveRows()

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
        return len(self.flows)

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if not index.isValid():
                return None

            if index.row() > len(self.flows):
                return None

            flow = self.flows[index.row()]

            row_values = flow.values_for_table()
            if index.column() in [3,6]:
                return ''
            return row_values[index.column()]

    def get_value(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return None

        if index.row() > len(self.flows):
            return None

        flow = self.flows[index.row()]

        row_values = flow.values_for_table()

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
            self.flows = sorted(self.flows, key=lambda flow: flow.id, reverse=reverse)
        elif (column == 1):
            self.flows = sorted(self.flows, key=lambda flow: int(flow.source_id or 0), reverse=reverse)
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

        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def response_status_sort_key(self, flow: HttpFlow) -> tuple[int, int]:
        # TODO: Fix this:
        response = flow.response
        if response is not None and flow.has_response():
            status = response.status_code
        else:
            status = 0

        return (status, flow.id)

    def refresh(self) -> None:
        self.layoutChanged.emit()

    def reload_flows(self, search_text: str):
        self.offset = 0
        self.limit = BATCH_SIZE

        self.flows, self.total_count = HttpFlowService().find_for_table(search_text, self.offset, self.limit)
        print("flows reloaded, total_count: ", self.total_count)

        self.layoutChanged.emit()

    def get_index_of(self, request_id: int) -> Optional[int]:
        for i, r in enumerate(self.flows):
            if r.id == request_id:
                return i

    def canFetchMore(self, parent: QtCore.QModelIndex) -> bool:
        if parent.isValid():
            print("can fetch more? invalid parent")
            return False

        result = (len(self.flows) < self.total_count)
        print("Can fetch more? ", result, " len(flows)=", len(self.flows), ", total_count=",self.total_count)
        return result

    def fetchMore(self, parent: QtCore.QModelIndex) -> None:
        print("fetching more!!!")
        self.offset += BATCH_SIZE

        new_flows, _ = HttpFlowService().find_for_table('', self.offset, self.limit)
        print(f"found {len(new_flows)} new flows! (offset {self.offset})")

        self.beginInsertRows(QtCore.QModelIndex(), self.offset, self.offset+len(new_flows))
        self.flows = self.flows + new_flows
        self.endInsertRows()
