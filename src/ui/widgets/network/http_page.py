from typing import Optional

from PyQt6 import QtCore, QtWidgets

from entities.http_flow import HttpFlow
from lib.background_worker import BackgroundWorker
from lib.debounce import debounce
from repos.app_settings_repo import AppSettingsRepo
from services.http_flow_service import HttpFlowService
from ui.views._compiled.network.http_page import Ui_HttpPage

TABLE_BATCH_SIZE = 20

class HttpPage(QtWidgets.QWidget):
    toggle_page = QtCore.pyqtSignal()
    send_flow_to_editor = QtCore.pyqtSignal(object)
    send_flow_to_fuzzer = QtCore.pyqtSignal(object)

    search_text: Optional[str]

    def __init__(self, *args, **kwargs):
        super(HttpPage, self).__init__(*args, **kwargs)
        self.ui = Ui_HttpPage()
        self.ui.setupUi(self)

        self.search_text = None
        # Setup the request model
        self.ui.requestsTableWidget.request_selected.connect(self.select_request)
        self.ui.requestsTableWidget.display_filters_saved.connect(self.reload)
        self.ui.requestsTableWidget.send_flow_to_editor.connect(self.send_flow_to_editor)
        self.ui.requestsTableWidget.send_flow_to_fuzzer.connect(self.send_flow_to_fuzzer)

        # Site Map
        self.ui.siteMap.setVisible(False)
        self.ui.requestsTableWidget.ui.siteMapButton.clicked.connect(self.toggle_sitemap)

        self.ui.toggleButton.clicked.connect(self.toggle_page)
        self.ui.requestViewWidget.set_show_rendered(True)
        self.ui.requestViewWidget.set_request_editable(False)
        self.ui.requestViewWidget.set_save_as_example_visible(False)
        self.ui.requestViewWidget.show_modified_dropdown()

        self.restore_layout_state()
        self.threadpool = QtCore.QThreadPool()

        layout = AppSettingsRepo().get()['network_layout']
        self.set_layout(layout)

    def set_layout(self, layout: str):
        if layout == 'vertical1':
            self.ui.requestsTableAndViewSplitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
            self.ui.requestViewWidget.ui.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        elif layout == 'vertical2':
            self.ui.requestsTableAndViewSplitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
            self.ui.requestViewWidget.ui.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        elif layout == 'horizontal1':
            self.ui.requestsTableAndViewSplitter.setOrientation(QtCore.Qt.Orientation.Vertical)
            self.ui.requestViewWidget.ui.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        elif layout == 'horizontal2':
            self.ui.requestsTableAndViewSplitter.setOrientation(QtCore.Qt.Orientation.Vertical)
            self.ui.requestViewWidget.ui.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)

    def toggle_sitemap(self):
        visible = not self.ui.siteMap.isVisible()
        self.ui.siteMap.setVisible(visible)

        if (visible):
            self.ui.requestsTableWidget.ui.siteMapButton.setText("<<")
        else:
            self.ui.requestsTableWidget.ui.siteMapButton.setText(">>")

    def reload(self):
        self.ui.requestsTableWidget.load_flows_async()

    def load_full_flow(self, signals) -> HttpFlow:
        flow = self.ui.requestViewWidget.flow
        flow_full = HttpFlowService().find(flow.id, load_minimal_response_data=False)
        if flow_full is None:
            return flow
        return flow_full

    def display_full_flow(self, flow: HttpFlow):
        self.ui.requestViewWidget.set_flow(flow)
        return

    # This loads the full flow, mainly the response body that is needed, cause the table does not
    # store that in memory. Debounced so you can hold the up/down arrow button in the table without
    # it freezing up.
    @debounce(0.1)
    def load_full_flow_async(self):
        self.worker = BackgroundWorker(self.load_full_flow)
        self.worker.signals.result.connect(self.display_full_flow)
        self.worker.signals.error.connect(self.request_error)
        self.threadpool.start(self.worker)  # type:ignore

    def request_error(self, error):
        exctype, value, traceback = error
        print(value)
        print(traceback)

    def restore_layout_state(self):
        return
        settings = AppSettings.get_instance()
        splitterState = settings.get("HttpPage.requestsTableAndViewSplitterState", None)
        splitterState2 = settings.get("HttpPage.requestsViewSplitterState", None)

        if splitterState is not None:
            self.ui.requestsTableAndViewSplitter.restoreState(splitterState)
        if splitterState2 is not None:
            self.ui.requestViewWidget.ui.splitter.restoreState(splitterState2)

    def save_layout_state(self):
        return
        splitter_state = self.ui.requestsTableAndViewSplitter.saveState()
        splitter_state2 = self.ui.requestViewWidget.ui.splitter.saveState()

        settings = AppSettings.get_instance()
        settings.save("HttpPage.requestsTableAndViewSplitterState", splitter_state)
        settings.save("HttpPage.requestsViewSplitterState", splitter_state2)

    def select_request(self, selected, deselected):
        if (len(selected.indexes()) > 0):
            selected_id_cols = list(filter(lambda i: i.column() == 0, selected.indexes()))
            selected_id = selected_id_cols[0].data()

            flow = self.ui.requestsTableWidget.get_flow(selected_id)
            if flow is None:
                return
            self.ui.requestViewWidget.set_flow(flow)

        # The flows stored here don't have their content value loaded to save on memory
        # So we need to fetch the flow from the db again when select
        self.load_full_flow_async()

    def proxy_requests_changed(self, flow: HttpFlow):
        self.ui.requestsTableWidget.load_flows_async()

    def show_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.loaderWidget)

    def hide_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.requestsTableWidget)
