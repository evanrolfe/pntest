from unittest import mock
from PySide2 import QtCore

from support.factories import factory

from widgets.crawls.crawls_page import CrawlsPage
from models.data.crawl import Crawl
from models.data.client import Client

class TestCrawlsPage:
    #@mock.patch("lib.backend.Backend.get_instance", mock.MagicMock())
    def test_crawls_page(self, database, qtbot):
        client = factory(Client).create()
        factory(Crawl).create(client_id=client.id)
        factory(Crawl).create(client_id=client.id, status='running')

        widget = CrawlsPage()
        qtbot.addWidget(widget)
        qtbot.waitForWindowShown(widget)

        # Click the second row of the table
        table = widget.ui.crawlsTable.ui.crawlsTable
        index = table.model().index(1, 0)
        rect = table.visualRect(index)
        qtbot.mouseClick(table.viewport(), QtCore.Qt.LeftButton, pos=rect.center())

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # time.sleep(1)

        assert widget.ui.crawlView.ui.crawlBodyText.toPlainText() == 'Selected crawl: 2'
        assert table.model().rowCount(0) == 2
