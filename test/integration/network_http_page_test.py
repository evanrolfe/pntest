# import time
from PyQt6 import QtCore
from support.fixtures import load_fixtures
from widgets.network.http_page import HttpPage
import time

EXPECTED_BODY = """{
  "ipv": false,
  "pvm": null,
  "rej": 0,
  "bln": 0,
  "acc": 1,
  "efi": []
}"""

class TestNetworkHttpPage:
    def get_data_at(self, table, row: int, column: int):
        index = table.model().index(row, column)
        return table.model().data(index, QtCore.Qt.ItemDataRole.DisplayRole)

    def test_network_http_page(self, database, qtbot):
        load_fixtures()

        widget = HttpPage()
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Click the second row of the table
        # table = widget.ui.crawlsTable.ui.crawlsTable
        table = widget.ui.requestsTableWidget.ui.requestsTable
        index = widget.table_model.index(1, 0)
        rect = table.visualRect(index)
        qtbot.mouseClick(table.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=rect.center())

        # Check request header line:
        header_line_text = widget.ui.requestViewWidget.ui.requestHeaders.ui.headerLine.text()
        assert header_line_text == 'GET / HTTP/1.1'

        # Check request headers table:
        table = widget.ui.requestViewWidget.ui.requestHeaders.ui.headersTable
        assert self.get_data_at(table, 0, 1) == 'Host'
        assert self.get_data_at(table, 0, 2) == 'synack.com'

        # Click the body tab
        response_tabs = widget.ui.requestViewWidget.ui.responseTabs
        response_tabs.setCurrentIndex(1)

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # time.sleep(3)

        body = widget.ui.requestViewWidget.ui.responseRaw.get_value()
        print(body)

        assert body == EXPECTED_BODY
