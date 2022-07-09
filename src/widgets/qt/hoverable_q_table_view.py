from PyQt6 import QtWidgets, QtCore

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
        self.horizontalHeader().viewport().installEventFilter(self.header_filter)

        self.header_filter.headers_hovered.connect(self.leaveEvent)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())

        if index != self.hover_index:
            self.hover_index = index
            self.hover_index_changed.emit(self.hover_index)

    def leaveEvent(self, event=None):
        if self.hover_index is not None:
            self.hover_index = None
            self.hover_index_changed.emit(self.hover_index)
