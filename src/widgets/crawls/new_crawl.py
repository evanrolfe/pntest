import json
from PySide2 import QtWidgets, QtCore

from views._compiled.crawls.ui_new_crawl import Ui_NewCrawl

from models.data.client import Client
from models.data.crawl import Crawl

class NewCrawl(QtWidgets.QDialog):
    crawl_saved = QtCore.Signal()

    def __init__(self, parent=None):
        super(NewCrawl, self).__init__(parent)

        self.ui = Ui_NewCrawl()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.start)

        self.load_clients()

    def showEvent(self, event):
        self.load_clients()

    def load_clients(self):
        clients = Client.where('type', '<>', 'anything').get()

        self.ui.clientsDropdown.clear()
        for client in clients:
            self.ui.clientsDropdown.addItem(client.title, client.id)

    @QtCore.Slot()
    def start(self):
        client_id = self.ui.clientsDropdown.itemData(
            self.ui.clientsDropdown.currentIndex())
        headless = (self.ui.browserModeDropdown.currentIndex() == 0)
        base_url = self.ui.baseURLText.text()
        ignore_urls = self.ui.ignoreURLsText.toPlainText().split("\n")
        ignore_urls = list(filter(lambda url: not url == '', ignore_urls))

        max_concurrency = int(self.ui.maxConcurrencyText.text())
        max_depth = int(self.ui.maxDepthText.text())
        xhr_timeout = int(self.ui.xhrTimeoutText.text()) * 1000
        wait_for_page = int(self.ui.waitPageText.text()) * 1000
        verbose = (self.ui.logLevelDropdown.currentIndex() == 1)

        config = {
            "baseUrl": base_url,
            "clickButtons": False,
            "maxConcurrency": max_concurrency,
            "maxDepth": max_depth,
            "xhrTimeout": xhr_timeout,
            "waitOnEachPage": wait_for_page,
            "verboseOutput": verbose,
            "headless": headless,
            "ignoreLinksIncluding": ignore_urls
        }

        crawl = Crawl()
        crawl.client_id = client_id
        crawl.status = "created"
        crawl.config = json.dumps(config)
        crawl.save()

        self.crawl_saved.emit()
        self.close()
