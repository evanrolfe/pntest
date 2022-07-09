# import time
from py import process
from pytestqt.qtbot import QtBot
from support.fixtures import load_fixtures
from lib.process_manager import ProcessManager
from widgets.main_window import MainWindow
from models.data.http_flow import HttpFlow

class TestMainWindow:
    def test_editor_page_saving_a_request(self, database, qtbot: QtBot):
        load_fixtures()

        process_manager = ProcessManager('')
        widget = MainWindow()
        widget.set_process_manager(process_manager)

        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # QtBot is unable to click context menus, so we simulate the right-click by triggering the signal here directly:
        proxy_flow = widget.network_page.http_page.ui.requestsTableWidget.table_model.flows[0]
        widget.network_page.http_page.ui.requestsTableWidget.send_flow_to_editor.emit(proxy_flow)  # type: ignore
        qtbot.wait(500)

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # time.sleep(3)

        editor_flows = HttpFlow.where('type', '=', HttpFlow.TYPE_EDITOR).order_by('id', 'desc').get()
        editor_flow = editor_flows[0]

        assert len(editor_flows) == 1
        assert editor_flow.id != proxy_flow.id
        assert editor_flow.request.id != proxy_flow.request.id

        process_manager.on_exit()
