from typing import Optional
from PyQt6 import QtCore, QtGui, QtWidgets

class RowStyleDelegate(QtWidgets.QStyledItemDelegate):
    HOVER_COLOUR = "#252526"

    hovered_index: QtCore.QModelIndex
    prev_hovered_index: QtCore.QModelIndex
    hover_background: QtGui.QBrush

    def __init__(self, parent=None):
        super(RowStyleDelegate, self).__init__(parent=None)
        self.parent = parent
        self.hovered_index = QtCore.QModelIndex()

    def highlight_index(self, index: QtCore.QModelIndex):
        self.hovered_index = index
        self.parent.viewport().repaint()

    # https://stackoverflow.com/questions/20565930/qtableview-how-can-i-highlight-the-entire-row-for-mouse-hover
    def initStyleOption(self, options: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        super().initStyleOption(options, index)
        if self.hovered_index.row() == index.row():
            options.backgroundBrush = QtGui.QBrush(QtGui.QColor(self.HOVER_COLOUR))

    # def paint(self, painter: QtGui.QPainter, options: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
    #     if index.column() == 6:
    #         label = QtWidgets.QLabel("HELLO")
    #         label.setAutoFillBackground(True)

    #         painter.fillRect(options.rect, options.palette.highlight())
    #         painter.drawPixmap(options.rect.x(), options.rect.y(), label.grab())

    #     super().paint(painter, options, index)

