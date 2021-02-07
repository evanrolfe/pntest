from PySide2 import QtWidgets

from views._compiled.crawls.ui_crawl_view import Ui_CrawlView

class CrawlView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(CrawlView, self).__init__(*args, **kwargs)
        self.ui = Ui_CrawlView()
        self.ui.setupUi(self)

    def clear(self):
        self.ui.crawlBodyText.setPlainText('')

    def set_crawl(self, crawl):
        text = f"Selected crawl: {crawl.id}" \

        self.ui.crawlBodyText.setPlainText(text)
