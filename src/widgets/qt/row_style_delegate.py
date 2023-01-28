from typing import Optional
from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils import get_method_colour, get_status_colour
from models.qt.requests_table_model import RequestsTableModel

class RowStyleDelegate(QtWidgets.QStyledItemDelegate):
    HOVER_COLOUR = "#252526"

    hovered_index: QtCore.QModelIndex
    prev_hovered_index: QtCore.QModelIndex
    hover_background: QtGui.QBrush

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super(RowStyleDelegate, self).__init__(parent=None)
        self.parent = parent # type:ignore
        self.hovered_index = QtCore.QModelIndex()

    def highlight_index(self, index: QtCore.QModelIndex):
        self.hovered_index = index
        self.parent.viewport().update()

    # https://stackoverflow.com/questions/20565930/qtableview-how-can-i-highlight-the-entire-row-for-mouse-hover
    def initStyleOption(self, options: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        super().initStyleOption(options, index)
        # options.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter
        if self.hovered_index.row() == index.row():
            options.backgroundBrush = QtGui.QBrush(QtGui.QColor(self.HOVER_COLOUR))

    def paint(self, painter: QtGui.QPainter, options: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        super().paint(painter, options, index)

        model: RequestsTableModel = index.model()  # type: ignore
        value = model.get_value(index)

        rect = self.parent.viewport().rect()
        x = self.parent.columnViewportPosition(index.column())
        x_next = self.parent.columnViewportPosition(index.column()+1)

        # Method column
        if index.column() == 3:
            color = get_method_colour(str(value))

            label = QtWidgets.QLabel(value)
            label.setAutoFillBackground(True)
            label.setObjectName("mylabel")
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setMinimumWidth(50)
            label.setStyleSheet(f"color: {color}; background: transparent;")

            # painter.fillRect(options.rect, QtGui.QColor("#C3E88D"))
            x_offest = 5
            y_offset = 0
            painter.drawPixmap(x+x_offest, options.rect.y()+y_offset, label.grab())

        # Response status column
        elif index.column() == 6:
            if value is None:
                return
            bg_color = get_status_colour(int(value)) # type:ignore

            label = QtWidgets.QLabel(str(value))
            label.setAutoFillBackground(True)
            label.setObjectName("responseStatusLabelTable")
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setMinimumWidth(30)
            label.setStyleSheet(f"background-color: {bg_color};")
            # painter.fillRect(options.rect, QtGui.QColor("#C3E88D"))
            x_offest = 9
            y_offset = 0
            painter.drawPixmap(options.rect.x()+x_offest, options.rect.y()+y_offset, label.grab())

