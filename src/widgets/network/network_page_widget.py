from PySide2 import QtCore, QtWidgets

from views._compiled.network.ui_network_page_widget import Ui_NetworkPageWidget

from lib.app_settings import AppSettings
from models.qt.requests_table_model import RequestsTableModel
from models.request_data import RequestData
from models.data.network_request import NetworkRequest

class NetworkPageWidget(QtWidgets.QWidget):
    send_request_to_editor = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(NetworkPageWidget, self).__init__(*args, **kwargs)
        self.ui = Ui_NetworkPageWidget()
        self.ui.setupUi(self)

        # Setup the request model
        requests = NetworkRequest.all()
        self.requests_table_model = RequestsTableModel(requests)
        self.ui.requestsTableWidget.setTableModel(self.requests_table_model)

        self.ui.requestsTableWidget.request_selected.connect(self.select_request)
        self.ui.requestsTableWidget.delete_requests.connect(self.delete_requests)
        self.ui.requestsTableWidget.search_text_changed.connect(self.search_requests)
        self.ui.requestsTableWidget.send_request_to_editor.connect(self.send_request_to_editor)

        self.restore_layout_state()

    def reload(self):
        self.ui.requestViewWidget.clear_request()
        requests = NetworkRequest.all()
        self.requests_table_model = RequestsTableModel(requests)
        self.ui.requestsTableWidget.setTableModel(self.requests_table_model)

    def restore_layout_state(self):
        settings = AppSettings.get_instance()
        splitterState = settings.get("NetworkPageWidget.requestsTableAndViewSplitterState", None)
        splitterState2 = settings.get("NetworkPageWidget.requestsViewSplitterState", None)

        self.ui.requestsTableAndViewSplitter.restoreState(splitterState)
        self.ui.requestViewWidget.ui.splitter.restoreState(splitterState2)

    def save_layout_state(self):
        splitter_state = self.ui.requestsTableAndViewSplitter.saveState()
        splitter_state2 = self.ui.requestViewWidget.ui.splitter.saveState()

        settings = AppSettings.get_instance()
        settings.save("NetworkPageWidget.requestsTableAndViewSplitterState", splitter_state)
        settings.save("NetworkPageWidget.requestsViewSplitterState", splitter_state2)

    @QtCore.Slot()
    def select_request(self, selected, deselected):
        if (len(selected.indexes()) > 0):
            selected_id_cols = list(filter(lambda i: i.column() == 0, selected.indexes()))
            selected_id = selected_id_cols[0].data()
            request = NetworkRequest.find(selected_id)
            self.ui.requestViewWidget.set_request(request)

    @QtCore.Slot()
    def delete_requests(self, request_ids):
        self.requests_table_model.delete_requests(request_ids)

    @QtCore.Slot()
    def search_requests(self, search_text):
        # requests = NetworkRequest.search({'search': search_text})
        # self.requests_table_model.requests = requests
        # self.requests_table_model.refresh()
        self.request_data = RequestData()
        self.request_data.set_filter_param('search', search_text)
        self.request_data.load_requests()
        self.requests_table_model.requests = self.request_data.requests
        self.requests_table_model.refresh()
