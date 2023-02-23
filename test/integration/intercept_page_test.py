from PyQt6 import QtCore
from pytestqt.qtbot import QtBot
from lib.proxy_message_receiver import ProxyMessageReceiver
from support.fixtures import load_fixtures
from ui.widgets.intercept.intercept_page import InterceptPage

class TestInterceptPage:
    pass
    # TODO: Only create a ProxyMessageReceiver singleton instance once for the whole test suite, so this test can run
    # along side proxy_test.py
    # def test_receiving_multiple_flows_and_forwarding_them(self, database, cleanup_database, qtbot: QtBot):
    #     Settings.create_defaults()
    #     # try:
    #     #     process_manager = ProxyMessageReceiver('./src')
    #     # except:
    #     #     pass

    #     widget = InterceptPage()
    #     qtbot.addWidget(widget)
    #     qtbot.waitExposed(widget)

    #     # Intercept request 1
    #     http_request = factory(HttpRequest, 'proxy').make(path="/first")
    #     http_request.save()
    #     http_flow = factory(HttpFlow, 'proxy').make(request_id=http_request.id, client_id=1, uuid='1234-abcd-1234-abcd')
    #     http_flow.save()
    #     widget.intercept_queue.flow_intercepted(http_flow)

    #     # Intercept request 2
    #     http_request2 = factory(HttpRequest, 'proxy').make(path="/second")
    #     http_request2.save()
    #     http_flow2 = factory(HttpFlow, 'proxy').make(request_id=http_request2.id, client_id=1, uuid='1234-abcd-1234-abcd')
    #     http_flow2.save()
    #     widget.intercept_queue.flow_intercepted(http_flow2)

    #     assert widget.ui.headers.ui.headerLine.text() == "GET /first"

    #     # Press forward (1)
    #     button = widget.ui.forwardButton
    #     qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

    #     assert widget.ui.headers.ui.headerLine.text() == "GET /second"

    #     # Press forward (2)
    #     button = widget.ui.forwardButton
    #     qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

    #     assert widget.ui.headers.ui.headerLine.text() == ""
    #     # widget.show()
    #     # qtbot.waitForWindowShown(widget)
    #     # qtbot.wait(3000)
