from PySide2 import QtWidgets, QtCore

from views._compiled.crawls.ui_crawls_table import Ui_CrawlsTable
# from lib.backend import Backend

class CrawlsTable(QtWidgets.QWidget):
    crawl_selected = QtCore.Signal(QtCore.QItemSelection, QtCore.QItemSelection)

    def __init__(self, *args, **kwargs):
        super(CrawlsTable, self).__init__(*args, **kwargs)
        self.ui = Ui_CrawlsTable()
        self.ui.setupUi(self)

        horizontalHeader = self.ui.crawlsTable.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        horizontalHeader.setSortIndicator(0, QtCore.Qt.DescendingOrder)
        self.ui.crawlsTable.setSortingEnabled(True)

        self.ui.crawlsTable.setColumnWidth(0, 50)
        self.ui.crawlsTable.setColumnWidth(1, 80)
        self.ui.crawlsTable.setColumnWidth(2, 400)
        self.ui.crawlsTable.setColumnWidth(3, 60)

        verticalHeader = self.ui.crawlsTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        # Set row selection behaviour:
        self.ui.crawlsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Set right-click behaviour:
        self.ui.crawlsTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.ui.crawlsTable.customContextMenuRequested.connect(self.right_clicked)

        # self.backend = Backend.get_instance()

    def setTableModel(self, model):
        self.table_model = model
        self.ui.crawlsTable.setModel(model)

        # Client Selected Signal:
        self.ui.crawlsTable.selectionModel().selectionChanged.connect(self.crawl_selected)

    # @Slot()
    # def right_clicked(self, position):
    #   index = self.ui.crawlsTable.indexAt(position)
    #   crawl = self.table_model.crawl_data.crawls[index.row()]

    #   menu = QMenu()

    #   if (crawl.open == True):
    #     action = QAction("Close Client (TODO)")
    #     menu.addAction(action)
    #   else:
    #     action = QAction("Open Client")
    #     menu.addAction(action)
    #     action.triggered.connect(lambda: self.open_browser_clicked(crawl))

    #   menu.exec_(self.mapToGlobal(position))

    # @Slot()
    # def open_browser_clicked(self, crawl):
    #   self.backend.open_crawl(crawl.id)
