from PySide2 import QtCore

class ExamplesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, flows, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['Title', 'Status', 'Response Length']
        self.flows = flows

    # def set_clients(self, clients):
    #     self.flows = clients
    #     self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
    #     self.layoutChanged.emit()

    def flow_for_index(self, index):
        row = index.row()
        return self.flows[row]

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
        return len(self.flows)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            if not index.isValid():
                return None

            if index.row() > len(self.flows):
                return None

            flow = self.flows[index.row()]

            if (index.column() == 0):
                return flow.title
            elif (index.column() == 1):
                return flow.response.status_code
            elif (index.column() == 2):
                return len(flow.response.content)

    @QtCore.Slot(result="QVariantList")
    def roleNameArray(self):
        return self.headers
