from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets


# Used for highlighting the intercept button
class SidebarStyleDelegate(QtWidgets.QStyledItemDelegate):
    highlight: bool
    bg_color: QtGui.QColor

    HOVER_COLOUR = "#FC6A0C"

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super(SidebarStyleDelegate, self).__init__(parent=None)
        self.bg_color = QtGui.QColor(self.HOVER_COLOUR)
        self.highlight = False
        self.parent = parent # type:ignore

    def paint(self, painter: QtGui.QPainter, options: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        if index.row() == 1 and self.highlight:
            painter.fillRect(options.rect, self.bg_color)
        super().paint(painter, options, index)

class Sidebar(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(Sidebar, self).__init__(parent)
        self.setup()

    def setup(self):
        print("Setting up sidebar!")
        self.itemSelectionChanged.connect(self.selection_changed)

        self.setObjectName('sideBar')
        #self.setSelectionBehavior()
        self.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.setFlow(QtWidgets.QListView.Flow.TopToBottom)
        self.setMovement(QtWidgets.QListView.Movement.Static)
        self.setUniformItemSizes(True)
        # icon_size = QSize(52, 35)

        # Proxy Item
        proxy_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-cloud-backup-restore-50.png"), "Proxy", None)
        proxy_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'proxy')
        proxy_item.setToolTip("Proxy")
        self.addItem(proxy_item)

        # Intercept Item
        intercept_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-rich-text-converter-50.png"), "Intercept", None)
        intercept_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'intercept')
        intercept_item.setToolTip("Intercept")
        self.addItem(intercept_item)

        self.delegate = SidebarStyleDelegate()
        self.setItemDelegate(self.delegate)

        # Editor Item
        editor_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-compose-50.png"), "Editor", None)
        editor_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'editor')
        editor_item.setToolTip("Request Editor")
        self.addItem(editor_item)

        # Docker Item
        docker_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-docker-64.png"), "Docker", None)
        docker_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'docker')
        docker_item.setToolTip("Docker")
        self.addItem(docker_item)

        # Browser Item
        browser_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-browse-page-50.png"), "Browser", None)
        browser_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'browser')
        browser_item.setToolTip("Clients")
        self.addItem(browser_item)

        # Extensions Item
        # extensions_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-plus-math-50.png"), None)
        # extensions_item.setData(QtCore.Qt.UserRole, 'extensions')
        # self.addItem(extensions_item)
        self.setCurrentRow(0)

        self.intercept_highlighted = False


    # DO not let the user de-select from the sidebar
    def selection_changed(self):
        row = self.currentRow()
        items = self.selectedItems()

        if len(items) == 0:
            self.setCurrentRow(row)

    def highlight_intercept(self):
        self.delegate.highlight = True
        self.update()

    def un_highlight_intercept(self):
        self.delegate.highlight = False
        self.update()

    # Code for flashing the intercept button:
        # self._timer = QtCore.QTimer(self)
        # self._timer.timeout.connect(self.flash_intercept)
        # self.updateTimer()
        # self._timer.start()
    # def flash_intercept(self):
    #     print("Flashing intercept!")
    #     self.intercept_highlighted = not self.intercept_highlighted

    #     if self.intercept_highlighted:
    #         self.delegate.bg_color = QtGui.QColor("#FC6A0C")
    #     else:
    #         self.delegate.bg_color = QtGui.QColor("#000000")
    #     self.update()

    # def updateTimer(self):
    #     self._timer.setInterval(500)
