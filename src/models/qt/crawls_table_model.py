from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject, Slot, Signal

from operator import itemgetter, attrgetter

class CrawlsTableModel(QAbstractTableModel):
  def __init__(self,crawls, parent = None):
    QAbstractTableModel.__init__(self, parent)
    self.headers = ['ID', 'Source', 'Status', 'Started', 'Finished']
    self.crawls = crawls

  def set_crawls(self, crawls):
    self.crawls = crawls
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
    return len(self.crawls)

  def data(self, index, role):
    if role == Qt.DisplayRole:
      if not index.isValid():
        return None

      if index.row() > len(self.crawls):
        return None

      crawl = self.crawls[index.row()]

      if (index.column() == 0):
        return crawl.id
      elif (index.column() == 1):
        return crawl.client_id
      elif (index.column() == 2):
        return crawl.status
      elif (index.column() == 3):
        return crawl.started_at
      elif (index.column() == 4):
        return crawl.started_at

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
  #     self.crawl_data.crawls = sorted(self.crawl_data.crawls,key=itemgetter('id'), reverse=reverse)
  #   elif (column == 1):
  #     self.crawl_data.crawls = sorted(self.crawl_data.crawls,key=itemgetter('crawl_id'), reverse=reverse)
  #   elif (column == 2):
  #     self.crawl_data.crawls = sorted(self.crawl_data.crawls,key=itemgetter('method', 'id'), reverse=reverse)
  #   elif (column == 3):
  #     self.crawl_data.crawls = sorted(self.crawl_data.crawls,key=itemgetter('url', 'id'), reverse=reverse)

  #   self.dataChanged.emit(QModelIndex(), QModelIndex())
