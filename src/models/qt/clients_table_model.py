from PySide2 import QtCore

class ClientsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, clients, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['ID', 'Type', 'Name',
                        'Status', 'Proxy Port', 'Browser Port']
        self.clients = clients

    def set_clients(self, clients):
        self.clients = clients
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        self.layoutChanged.emit()

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
        return len(self.clients)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            if not index.isValid():
                return None

            if index.row() > len(self.clients):
                return None

            client = self.clients[index.row()]

            if (index.column() == 0):
                return client.id
            elif (index.column() == 1):
                return client.type
            elif (index.column() == 2):
                return client.title
            elif (index.column() == 3):
                return client.open_text()
            elif (index.column() == 4):
                return client.proxy_port
            elif (index.column() == 5):
                return client.browser_port

    @QtCore.Slot(result="QVariantList")
    def roleNameArray(self):
        return self.headers
