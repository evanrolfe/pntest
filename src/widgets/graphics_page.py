from PyQt6 import QtWidgets, QtCore, QtGui
from ui.views._compiled.graphics_page import Ui_GraphicsPage

class HoverRectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normal_color = QtGui.QBrush(QtGui.QColor("#2D2D2D"))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setBrush(QtGui.QColor("#3A3A3A"))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(self.normal_color)
        super().hoverLeaveEvent(event)

class GraphicsPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(GraphicsPage, self).__init__(*args, **kwargs)
        self.ui = Ui_GraphicsPage()
        self.ui.setupUi(self)

        size = self.ui.graphicsView.viewport().size()
        print(f"width: {size.width()}, height: {size.height()}")
        scene = QtWidgets.QGraphicsScene()

        bg_color = QtGui.QBrush(QtGui.QColor("#2D2D2D"))
        border_color = QtGui.QPen(QtGui.QColor("#474747"))
        border_color.setWidth(3)

        # ---------------------------------------------------------------------
        # Rectangles
        # ---------------------------------------------------------------------
        rect = HoverRectItem(0, 0, 200, 50)
        rect.setBrush(bg_color)
        rect.setPen(border_color)
        rect.setZValue(1)
        rect_proxy = QtWidgets.QGraphicsProxyWidget(rect)

        rect2 = HoverRectItem(0, -300, 200, 50)
        rect2.setBrush(bg_color)
        rect2.setPen(border_color)
        rect2.setZValue(1)
        rect_proxy2 = QtWidgets.QGraphicsProxyWidget(rect2)

        scene.addItem(rect)
        scene.addItem(rect2)

        # ---------------------------------------------------------------------
        # Labels
        # ---------------------------------------------------------------------
        label = QtWidgets.QLabel()
        label.setText("backend")
        label.setStyleSheet("font-size: 30pt;")
        rect_proxy.setWidget(label)
        rect_proxy.setPos(rect.boundingRect().center() - rect_proxy.boundingRect().center()) # type:ignore

        label2 = QtWidgets.QLabel()
        label2.setText("frontend")
        label2.setStyleSheet("font-size: 30pt;")
        rect_proxy2.setWidget(label2)
        rect_proxy2.setPos(rect2.boundingRect().center() - rect_proxy2.boundingRect().center()) # type:ignore

        # ---------------------------------------------------------------------
        # Lines+Arrows
        # ---------------------------------------------------------------------
        line = QtWidgets.QGraphicsLineItem()
        line.setPen(QtGui.QPen(bg_color, 5, QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.RoundCap, QtCore.Qt.PenJoinStyle.RoundJoin))
        line.setZValue(0)
        line.setLine(
            rect.boundingRect().center().x(),
            rect.boundingRect().center().y(),
            rect2.boundingRect().center().x(),
            rect2.boundingRect().center().y()
        )

        # arrow = QtGui.QPolygonF([QtCore.QPointF(-5, 5), QtCore.QPointF(0, 0), QtCore.QPointF(-5, -5)])
        # # line.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        # line.setPen(QtCore.Qt.GlobalColor.white)
        # # line.setPolygon(arrow)
        # line.setPos(rect2.pos())

        scene.addItem(line)

        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(rect, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.graphicsView.setBackgroundBrush(QtGui.QColor("#1E1E1E"))
        self.ui.graphicsView.show()

