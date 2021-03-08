from unittest import mock
from PySide2 import QtCore

from support.factories import factory

from widgets.network.http_page import HttpPage
from models.data.network_request import NetworkRequest

class TestNetworkPageHttp:
    @mock.patch("lib.backend.Backend.get_instance", mock.MagicMock())
    def test_crawls_page(self, database, qtbot):
        factory(NetworkRequest, 'with_response').create()
        factory(NetworkRequest, 'with_response').create()

        widget = HttpPage()
        qtbot.addWidget(widget)
        qtbot.waitForWindowShown(widget)

        # Click the first row of the table
        table = widget.ui.requestsTableWidget.ui.requestsTable
        index = table.model().index(0, 0)
        rect = table.visualRect(index)
        qtbot.mouseClick(table.viewport(), QtCore.Qt.LeftButton, pos=rect.center())

        # Requests Table:
        assert table.model().rowCount(0) == 2

        # RequestView/Request:
        request_headers = widget.ui.requestViewWidget.get_request_headers()
        request_header_line = widget.ui.requestViewWidget.ui.requestHeaders.ui.headerLine
        assert 'example.com' == request_headers['host']
        assert 'GET / HTTP/1.1' == request_header_line.text()

        # RequestView/Response
        response_headers = widget.ui.requestViewWidget.ui.responseHeaders.get_headers()
        response_header_line = widget.ui.requestViewWidget.ui.responseHeaders.ui.headerLine
        assert 'HTTP/1.1 200 OK' == response_header_line.text()
        assert '20' in response_headers['content-length']


