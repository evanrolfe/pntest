from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject, Slot, Signal

from operator import itemgetter, attrgetter

class ClientsTableModel(QAbstractTableModel):
  def __init__(self,clients, parent = None):
    QAbstractTableModel.__init__(self, parent)
    self.headers = ['ID', 'Type', 'Name', 'Status', 'Proxy Port', 'Browser Port']
    self.clients = clients

  def set_clients(self, clients):
    self.clients = clients
    self.dataChanged.emit(QModelIndex(), QModelIndex())
    self.layoutChanged.emit()

  def roleNames(self):
    roles = {}
    for i, header in enumerate(self.headers):
      roles[Qt.UserRole + i + 1] = header.encode()
    return roles

  def headerData(self, section, orientation, role = Qt.DisplayRole):
    if role == Qt.DisplayRole and orientation == Qt.Horizontal:
      return self.headers[section]

    return None

  def columnCount(self, parent):
    return len(self.headers)

  def rowCount(self, index):
    return len(self.clients)

  def data(self, index, role):
    if role == Qt.DisplayRole:
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

  @Slot(result="QVariantList")
  def roleNameArray(self):
    return self.headers

