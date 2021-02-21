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

        # Check the text boxes have the right values:
        request_headers = widget.ui.requestViewWidget.ui.requestHeadersText.toPlainText()
        assert 'GET / HTTP/1.1' in request_headers
        assert 'host: example.com' in request_headers

        response_headers = widget.ui.requestViewWidget.ui.responseHeadersText.toPlainText()
        assert 'HTTP/1.1 200 OK' in response_headers
        assert 'content-length: 20' in response_headers

        assert table.model().rowCount(0) == 2
