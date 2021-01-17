import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from views._compiled.crawls.ui_crawls_page import Ui_CrawlsPage

from widgets.crawls.new_crawl import NewCrawl
from lib.backend import Backend
from models.qt.crawls_table_model import CrawlsTableModel
from models.data.crawl import Crawl

class CrawlsPage(QWidget):
  def __init__(self, *args, **kwargs):
    super(CrawlsPage, self).__init__(*args, **kwargs)
    self.ui = Ui_CrawlsPage()
    self.ui.setupUi(self)

    # Setup the crawl model
    crawls = Crawl.all()
    self.crawls_table_model = CrawlsTableModel(crawls)

    self.ui.crawlsTable.setTableModel(self.crawls_table_model)
    self.ui.crawlsTable.crawl_selected.connect(self.select_crawl)

    # Reload when the crawls have changed:
    self.backend = Backend.get_instance()

    # New Crawler Dialog:
    self.new_crawl = NewCrawl(self)
    self.new_crawl.crawl_saved.connect(self.reload_table_data)
    self.ui.newCrawlerButton.clicked.connect(lambda: self.new_crawl.show())

  def showEvent(self, event):
    self.reload_table_data()

  @Slot()
  def reload_table_data(self):
    crawls = Crawl.all()
    self.crawls_table_model.set_crawls(crawls)

  @Slot()
  def select_crawl(self, selected, deselected):
    selected_id = selected.indexes()[0].data()
    crawl = self.crawl_data.load_crawl(selected_id)
    self.ui.crawlView.set_crawl(crawl)
