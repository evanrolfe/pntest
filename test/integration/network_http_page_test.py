# import time
from PyQt6 import QtCore
from pytestqt.qtbot import QtBot
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from support.fixtures import load_fixtures
from models.data.settings import Settings
from widgets.network.http_page import HttpPage
import time
from support.factories import factory

EXPECTED_BODY = """{
  "ipv": false,
  "pvm": null,
  "rej": 0,
  "bln": 0,
  "acc": 1,
  "efi": []
}"""

def create_http_flow(scheme: str, host: str, port: int, path: str) -> HttpFlow:
    http_request = factory(HttpRequest, 'proxy').make(scheme=scheme, host=host, port=port, path=path)
    http_request.save()

    http_response = factory(HttpResponse, 'http_response').make()
    http_response.save()

    http_flow = factory(HttpFlow, 'proxy').make(
        request_id=http_request.id,
        response_id=http_response.id,
        client_id=1
    )
    http_flow.save()
    return http_flow

class TestNetworkHttpPage:
    def get_data_at(self, table, row: int, column: int):
        index = table.model().index(row, column)
        return table.model().data(index, QtCore.Qt.ItemDataRole.DisplayRole)

    def test_network_http_page(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()
        Settings.create_defaults()

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

    def test_network_http_page_display_filters_host(self, database, cleanup_database, qtbot: QtBot):
        Settings.create_defaults()
        flow1 = create_http_flow("http", "example.com", 80, "/admin/login.php")
        flow2 = create_http_flow("http", "example.com", 80, "/admin/test.php")
        flow3 = create_http_flow("http", "example.com", 80, "/users/index.php")
        flow4 = create_http_flow("http", "pntest.com", 80, "/index.html")

        widget = HttpPage()
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Click display filters button
        button = widget.ui.requestsTableWidget.ui.displayFiltersButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        # Enter hosts to filter
        widget.ui.requestsTableWidget.network_display_filters.ui.hostSettingDropdown.setCurrentIndex(1)
        widget.ui.requestsTableWidget.network_display_filters.ui.hostsText.setPlainText("pntest.com")

        # Click save
        button = widget.ui.requestsTableWidget.network_display_filters.ui.saveButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        # Wait for loading finished signal
        with qtbot.waitSignal(widget.worker.signals.finished, timeout=10000):
            pass

        # Check the correct requests are displayed in the table
        table_model = widget.ui.requestsTableWidget.table_model
        assert len(table_model.flows) == 1
        assert table_model.flows[0].id == flow4.id

    def test_network_http_page_searching_requests_by_path(self, database, cleanup_database, qtbot: QtBot):
        Settings.create_defaults()
        flow1 = create_http_flow("http", "example.com", 80, "/admin/login.php")
        flow2 = create_http_flow("http", "example.com", 80, "/admin/test.php")
        flow3 = create_http_flow("http", "example.com", 80, "/users/index.php")
        flow4 = create_http_flow("http", "pntest.com", 80, "/index.html")

        widget = HttpPage()
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Enter the search terms
        search_box = widget.ui.requestsTableWidget.ui.searchBox
        qtbot.keyClicks(search_box, "/admin")
        qtbot.keyClick(search_box, QtCore.Qt.Key.Key_Return)

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # time.sleep(3)

        # Wait for loading finished signal
        with qtbot.waitSignal(widget.worker.signals.finished, timeout=10000):
            pass

        # Check the correct requests are displayed in the table
        table_model = widget.ui.requestsTableWidget.table_model
        assert len(table_model.flows) == 2

        request_ids = [f.id for f in table_model.flows]
        assert flow1.id in request_ids
        assert flow2.id in request_ids
