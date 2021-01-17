from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject, Slot, Signal

from operator import itemgetter, attrgetter

class ClientsTableModel(QAbstractTableModel):
  def __init__(self,clients, parent = None):
    QAbstractTableModel.__init__(self, parent)
    self.headers = ['ID', 'Type', 'Name', 'Status']
    self.clients = clients

  # def add_request(self, request):
  #   rowIndex = 0
  #   self.beginInsertRows(QModelIndex(), rowIndex, rowIndex)
  #   self.client_data.clients.insert(0, request)
  #   self.endInsertRows()
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

  @Slot(result="QVariantList")
  def roleNameArray(self):
    return self.headers

  # def sort(self, column, order):
  #   self.sortOrder = order
  #   self.sortColumn = column

  #   if (order == Qt.AscendingOrder):
  #     print(f"Sorting column {column} ASC")
  #   elif (order == Qt.DescendingOrder):
  #     print(f"Sorting column {column} DESC")

  #   reverse = (order == Qt.DescendingOrder)

  #   if (column == 0):
  #     self.client_data.clients = sorted(self.client_data.clients,key=itemgetter('id'), reverse=reverse)
  #   elif (column == 1):
  #     self.client_data.clients = sorted(self.client_data.clients,key=itemgetter('client_id'), reverse=reverse)
  #   elif (column == 2):
  #     self.client_data.clients = sorted(self.client_data.clients,key=itemgetter('method', 'id'), reverse=reverse)
  #   elif (column == 3):
  #     self.client_data.clients = sorted(self.client_data.clients,key=itemgetter('url', 'id'), reverse=reverse)

  #   self.dataChanged.emit(QModelIndex(), QModelIndex())
