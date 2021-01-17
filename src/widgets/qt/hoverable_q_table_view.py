from PySide2.QtCore import Qt, Slot, Signal, QModelIndex, QObject, QEvent
from PySide2.QtWidgets import QTableView

class HeaderViewFilter(QObject):
  headers_hovered = Signal()

  def __init__(self, parent = None, *args):
      super(HeaderViewFilter, self).__init__(parent, *args)

  def eventFilter(self, object, event):
    if event.type() == QEvent.MouseMove:
      self.headers_hovered.emit()

    return False

class HoverableQTableView(QTableView):
  hover_index_changed = Signal(object)

  def __init__(self, parent = None):
    super(HoverableQTableView, self).__init__(parent)

    self.hover_index = None
    self.header_filter = HeaderViewFilter()
    self.horizontalHeader().viewport().installEventFilter(self.header_filter)

    self.header_filter.headers_hovered.connect(self.leaveEvent)

  def mouseMoveEvent(self, event):
    index = self.indexAt(event.pos())

    if index != self.hover_index:
      self.hover_index = index
      self.hover_index_changed.emit(self.hover_index)

  def leaveEvent(self, event = None):
    if self.hover_index != None:
      self.hover_index = None
      self.hover_index_changed.emit(self.hover_index)
