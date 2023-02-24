from PyQt6 import QtCore, QtGui, QtWidgets

from lib.debounce import debounce


class HeaderViewFilter(QtCore.QObject):
    headers_hovered = QtCore.pyqtSignal()

    def __init__(self, parent=None, *args):
        super(HeaderViewFilter, self).__init__(parent, *args)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Type.MouseMove:
            self.headers_hovered.emit()

        return False

class HoverableQTableView(QtWidgets.QTableView):
    hover_index_changed = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(HoverableQTableView, self).__init__(parent)

        self.hover_index = None
        self.header_filter = HeaderViewFilter()
        # self.horizontalHeader().viewport().installEventFilter(self.header_filter)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())

        if index != self.hover_index:
            self.hover_index = index
            self.hover_index_changed.emit(self.hover_index)

    def leaveEvent(self, event=None):
        if self.hover_index is not None:
            self.hover_index = QtCore.QModelIndex() # blank index
            self.hover_index_changed.emit(self.hover_index)

    # Its slow to resize the QTableView, so we debounce it when the user resizes the pane or window
    @debounce(0.1)
    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
