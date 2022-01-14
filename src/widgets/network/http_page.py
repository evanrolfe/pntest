from PySide2 import QtCore, QtWidgets

from views._compiled.network.ui_http_page import Ui_HttpPage

from lib.app_settings import AppSettings
from models.qt.requests_table_model import RequestsTableModel
from models.data.http_flow import HttpFlow

class HttpPage(QtWidgets.QWidget):
    toggle_page = QtCore.Signal()
    send_flow_to_editor = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(HttpPage, self).__init__(*args, **kwargs)
        self.ui = Ui_HttpPage()
        self.ui.setupUi(self)

        # Setup the request model
        http_flows = HttpFlow.find_for_table()
        self.table_model = RequestsTableModel(http_flows)
        self.ui.requestsTableWidget.setTableModel(self.table_model)

        self.ui.requestsTableWidget.request_selected.connect(self.select_request)
        self.ui.requestsTableWidget.delete_requests.connect(self.delete_requests)
        self.ui.requestsTableWidget.search_text_changed.connect(self.search_requests)
        self.ui.requestsTableWidget.send_flow_to_editor.connect(self.send_flow_to_editor)

        self.ui.toggleButton.clicked.connect(self.toggle_page)
        self.ui.requestViewWidget.set_show_rendered(True)
        self.ui.requestViewWidget.set_save_as_example_visible(False)
        self.ui.requestViewWidget.show_modified_dropdown()

        self.restore_layout_state()

    def reload(self):
        self.ui.requestViewWidget.clear_request()
        http_flows = HttpFlow.find_for_table()
        self.table_model = RequestsTableModel(http_flows)
        self.ui.requestsTableWidget.setTableModel(self.table_model)

    def restore_layout_state(self):
        settings = AppSettings.get_instance()
        splitterState = settings.get("HttpPage.requestsTableAndViewSplitterState", None)
        splitterState2 = settings.get("HttpPage.requestsViewSplitterState", None)

        self.ui.requestsTableAndViewSplitter.restoreState(splitterState)
        self.ui.requestViewWidget.ui.splitter.restoreState(splitterState2)

    def save_layout_state(self):
        splitter_state = self.ui.requestsTableAndViewSplitter.saveState()
        splitter_state2 = self.ui.requestViewWidget.ui.splitter.saveState()

        settings = AppSettings.get_instance()
        settings.save("HttpPage.requestsTableAndViewSplitterState", splitter_state)
        settings.save("HttpPage.requestsViewSplitterState", splitter_state2)

    @QtCore.Slot()  # type:ignore
    def select_request(self, selected, deselected):
        if (len(selected.indexes()) > 0):
            selected_id_cols = list(filter(lambda i: i.column() == 0, selected.indexes()))
            selected_id = selected_id_cols[0].data()
            flow = HttpFlow.find(selected_id)
            self.ui.requestViewWidget.set_flow(flow)

    @QtCore.Slot()  # type:ignore
    def delete_requests(self, request_ids):
        if len(request_ids) > 1:
            message = f'Are you sure you want to delete {len(request_ids)} requests?'
        else:
            message = 'Are you sure you want to delete this request?'

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('PNTest')
        message_box.setText(message)
        message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        message_box.setDefaultButton(QtWidgets.QMessageBox.Yes)
        response = message_box.exec_()

        if response == QtWidgets.QMessageBox.Yes:
            self.table_model.delete_requests(request_ids)

    @QtCore.Slot()  # type:ignore
    def search_requests(self, search_text):
        return True
        # requests = HttpFlow.search({'search': search_text})
        # self.table_model.requests = requests
        # self.table_model.refresh()
        # self.request_data = RequestData()
        # self.request_data.set_filter_param('search', search_text)
        # self.request_data.load_requests()
        # self.table_model.requests = self.request_data.requests
        # self.table_model.refresh()

    @QtCore.Slot()  # type:ignore
    def flow_created(self, flow):
        self.table_model.add_flow(flow)

    @QtCore.Slot()  # type:ignore
    def flow_updated(self, flow):
        self.table_model.update_flow(flow)
