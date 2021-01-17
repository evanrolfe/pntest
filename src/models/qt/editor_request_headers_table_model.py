from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject, Slot, Signal

from operator import itemgetter, attrgetter

class EditorRequestHeadersTableModel(QAbstractTableModel):
  BLANK_ROW = [False, '', '']
  def __init__(self,headers, parent = None):
    QAbstractTableModel.__init__(self, parent)
    self.row_headers = ['', 'Key', 'Value']
    self.headers = headers
    self.insert_blank_row()

  def insert_blank_row(self):
    count = len(self.headers)
    self.beginInsertRows(QModelIndex(), count, count)
    # Pass array by value
    self.headers.append(self.BLANK_ROW[:])
    self.endInsertRows()

  def get_headers(self):
    header_arrays = [h[1:3] for h in self.headers if h[0] == True]
    headers = {}
    for header_arr in header_arrays:
      headers[header_arr[0]] = header_arr[1]
    return headers

  def flags(self, index):
    if index.column() == 0:
      return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
    else:
      if index.row() < 2:
        return Qt.ItemIsEnabled
      else:
        return Qt.ItemIsEditable | Qt.ItemIsEnabled

  def roleNames(self):
    roles = {}
    for i, header in enumerate(self.row_headers):
      roles[Qt.UserRole + i + 1] = header.encode()
    return roles

  def headerData(self, section, orientation, role = Qt.DisplayRole):
    if role == Qt.DisplayRole and orientation == Qt.Horizontal:
      return self.row_headers[section]

    return None

  def columnCount(self, parent):
    return len(self.row_headers)

  def rowCount(self, index):
    return len(self.headers)

  def setData(self, index, value, role=Qt.EditRole):
    if role == Qt.CheckStateRole and index.column() == 0:
      self.headers[index.row()][0] = (value == Qt.Checked)
      return True

    if role == Qt.EditRole:
      if self.is_item_blank(index) and value != '':
        self.headers[index.row()][0] = True
        self.insert_blank_row()

      self.headers[index.row()][index.column()] = value
      return True

    return False

  def data(self, index, role):
    if role == Qt.CheckStateRole and index.column() == 0:
      checked = self.headers[index.row()][0]
      if checked:
        return Qt.Checked
      else:
        return Qt.Unchecked

    if role == Qt.DisplayRole or role == Qt.EditRole:
      if not index.isValid():
        return None

      if index.row() > len(self.headers) or index.column() == 0:
        return None

      return self.headers[index.row()][index.column()]

  @Slot(result="QVariantList")
  def roleNameArray(self):
    return self.row_headers

  def is_item_blank(self, index):
    return self.headers[index.row()] == self.BLANK_ROW
