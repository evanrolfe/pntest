from PySide2 import QtCore

class ExamplesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, flows, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['Title', 'Status', 'Response Length']
        self.flows = flows

    def flow_for_index(self, index):
        row = index.row()
        return self.flows[row]

    def roleNames(self):
        roles = {}
        for i, header in enumerate(self.headers):
            roles[QtCore.Qt.UserRole + i + 1] = header.encode()
        return roles

    def flags(self, index):
        if index.column() == 0 and index.row() > 0:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.headers[section]

        return None

    def columnCount(self, parent):
        return len(self.headers)

    def rowCount(self, index):
        return len(self.flows)

    def data(self, index, role):
        if role in [QtCore.Qt.EditRole, QtCore.Qt.DisplayRole]:
            if not index.isValid():
                return None

            if index.row() > len(self.flows):
                return None

            flow = self.flows[index.row()]

            if flow.is_example():
                if (index.column() == 0):
                    return flow.title
                elif (index.column() == 1):
                    return flow.response.status_code
                elif (index.column() == 2):
                    return len(flow.response.content)
            else:
                if (index.column() == 0):
                    return 'Original Request'
                else:
                    return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            if value != '':
                flow = self.flows[index.row()]
                flow.title = value
                flow.save()

            return True

        return False

    @QtCore.Slot(result="QVariantList")
    def roleNameArray(self):
        return self.headers
