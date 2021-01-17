import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from views._compiled.crawls.ui_crawl_view import Ui_CrawlView

class CrawlView(QWidget):
  def __init__(self, *args, **kwargs):
    super(CrawlView, self).__init__(*args, **kwargs)
    self.ui = Ui_CrawlView()
    self.ui.setupUi(self)

  def set_crawl(self, crawl):
    text = f"Selected crawl: {crawl.id}" \

    self.ui.crawlBodyText.setPlainText(text)
