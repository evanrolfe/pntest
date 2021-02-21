from PySide2 import QtCore, QtGui, QtWidgets

class RowStyleDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        self.hovered_row = None
        self.parent = parent
        super(RowStyleDelegate, self).__init__(parent=None)

    @QtCore.Slot()
    def highlight_index(self, index):
        if index is None:
            self.hovered_row = None
        else:
            self.hovered_row = index.row()

        self.parent.viewport().repaint()

    def paint(self, painter, options, index):
        # if index.row() == 3:
        #   options.state = QStyle.State_MouseOver
        options.backgroundBrush = QtGui.QBrush(QtGui.QColor('#000000'))
        QtWidgets.QStyledItemDelegate.paint(self, painter, options, index)
