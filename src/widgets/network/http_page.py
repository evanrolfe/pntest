from typing import Optional
from PyQt6 import QtCore, QtWidgets
from models.http_response import HttpResponse
from proxy.common_types import ProxyRequest, ProxyResponse
from views._compiled.network.http_page import Ui_HttpPage

from lib.background_worker import BackgroundWorker
from lib.app_settings import AppSettings
from models.qt.requests_table_model import RequestsTableModel
from models.http_flow import HttpFlow
from repos.http_flow_repo import HttpFlowRepo

class HttpPage(QtWidgets.QWidget):
    toggle_page = QtCore.pyqtSignal()
    send_flow_to_editor = QtCore.pyqtSignal(object)

    search_text: Optional[str]
    table_model: RequestsTableModel

    def __init__(self, *args, **kwargs):
        super(HttpPage, self).__init__(*args, **kwargs)
        self.ui = Ui_HttpPage()
        self.ui.setupUi(self)

        self.search_text = None
        # Setup the request model
        http_flows = HttpFlowRepo().find_for_table('')
        self.table_model = RequestsTableModel(http_flows)
        self.ui.requestsTableWidget.setTableModel(self.table_model)

        self.ui.requestsTableWidget.request_selected.connect(self.select_request)
        self.ui.requestsTableWidget.delete_requests.connect(self.delete_requests)
        self.ui.requestsTableWidget.search_text_changed.connect(self.search_flows_async)
        self.ui.requestsTableWidget.display_filters_saved.connect(self.load_flows_async)
        self.ui.requestsTableWidget.send_flow_to_editor.connect(self.send_flow_to_editor)

        # Site Map
        self.ui.siteMap.setVisible(False)
        self.ui.requestsTableWidget.ui.siteMapButton.clicked.connect(self.toggle_sitemap)

        self.ui.toggleButton.clicked.connect(self.toggle_page)
        self.ui.requestViewWidget.set_show_rendered(True)
        self.ui.requestViewWidget.set_save_as_example_visible(False)
        self.ui.requestViewWidget.show_modified_dropdown()

        self.restore_layout_state()
        self.threadpool = QtCore.QThreadPool()

    def toggle_sitemap(self):
        visible = not self.ui.siteMap.isVisible()
        self.ui.siteMap.setVisible(visible)

        if (visible):
            self.ui.requestsTableWidget.ui.siteMapButton.setText("<<")
        else:
            self.ui.requestsTableWidget.ui.siteMapButton.setText(">>")

    def reload(self):
        self.search_text = None
        self.load_flows_async()

    def load_flows_async(self):
        self.show_loader()
        self.worker = BackgroundWorker(self.load_flows)
        self.worker.signals.result.connect(self.update_table)
        self.worker.signals.error.connect(self.request_error)
        self.worker.signals.finished.connect(self.hide_loader)
        self.threadpool.start(self.worker)

    def search_flows_async(self, search_text: str):
        print(f'Searching async for {search_text}')
        self.search_text = search_text
        self.load_flows_async()

    def load_flows(self, signals):
        print(f'Searching for {self.search_text}')

        http_flows = HttpFlowRepo().find_for_table(self.search_text or '')

        return http_flows

    def update_table(self, http_flows):
        print('Update table called')
        self.table_model = RequestsTableModel(http_flows)
        self.ui.requestsTableWidget.setTableModel(self.table_model)

    def request_error(self, error):
        exctype, value, traceback = error
        print(value)
        print(traceback)

    def restore_layout_state(self):
        settings = AppSettings.get_instance()
        splitterState = settings.get("HttpPage.requestsTableAndViewSplitterState", None)
        splitterState2 = settings.get("HttpPage.requestsViewSplitterState", None)

        if splitterState is not None:
            self.ui.requestsTableAndViewSplitter.restoreState(splitterState)
        if splitterState2 is not None:
            self.ui.requestViewWidget.ui.splitter.restoreState(splitterState2)

    def save_layout_state(self):
        splitter_state = self.ui.requestsTableAndViewSplitter.saveState()
        splitter_state2 = self.ui.requestViewWidget.ui.splitter.saveState()

        settings = AppSettings.get_instance()
        settings.save("HttpPage.requestsTableAndViewSplitterState", splitter_state)
        settings.save("HttpPage.requestsViewSplitterState", splitter_state2)

    def select_request(self, selected, deselected):
        if (len(selected.indexes()) > 0):
            selected_id_cols = list(filter(lambda i: i.column() == 0, selected.indexes()))
            selected_id = selected_id_cols[0].data()

            flow = [f for f in self.table_model.flows if f.id == selected_id][0]
            if flow is not None:
                self.ui.requestViewWidget.set_flow(flow)

    def delete_requests(self, request_ids):
        if len(request_ids) > 1:
            message = f'Are you sure you want to delete {len(request_ids)} requests?'
        else:
            message = 'Are you sure you want to delete this request?'

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('PNTest')
        message_box.setText(message)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
        message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
        response = message_box.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            self.table_model.delete_requests(request_ids)

    def proxy_request_received(self, flow: HttpFlow):
        self.table_model.add_flow(flow)

    def proxy_response_received(self, flow: HttpFlow):
        self.table_model.update_flow(flow)

    def show_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.loaderWidget)

    def hide_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.requestsTableWidget)
