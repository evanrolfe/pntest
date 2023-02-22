from PyQt6 import QtCore, QtWidgets
from mitmproxy.common_types import ProxyWebsocketMessage
from repos.http_flow_repo import HttpFlowRepo

from ui.views._compiled.network.ws_page import Ui_WsPage

from qt_models.messages_table_model import MessagesTableModel
from entities.websocket_message import WebsocketMessage
from repos.ws_message_repo import WsMessageRepo

class WsPage(QtWidgets.QWidget):
    toggle_page = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(WsPage, self).__init__(*args, **kwargs)
        self.ui = Ui_WsPage()
        self.ui.setupUi(self)

        # Setup the table model
        messages = WsMessageRepo().find_for_table('')

        self.table_model = MessagesTableModel(messages)
        self.ui.messagesTable.setTableModel(self.table_model)

        self.ui.toggleButton.clicked.connect(self.toggle_page)
        self.ui.messagesTable.row_selected.connect(self.select_message)
        self.ui.messagesTable.delete_rows.connect(self.delete_messages)
        # self.ui.messagesTable.search_text_changed.connect(self.search_requests)

        self.restore_layout_state()

    def reload(self):
        self.ui.messageViewWidget.clear_message()
        messages = WsMessageRepo().find_for_table('')
        self.table_model = MessagesTableModel(messages)
        self.ui.messagesTable.setTableModel(self.table_model)

    def restore_layout_state(self):
        return
        settings = AppSettings.get_instance()
        splitterState = settings.get("WsPage.messagesTableAndViewSplitter", None)
        splitterState2 = settings.get("WsPage.messageViewSplitterState", None)

        if splitterState is not None:
            self.ui.messagesTableAndViewSplitter.restoreState(splitterState)
        if splitterState2 is not None:
            self.ui.messageViewWidget.ui.splitter.restoreState(splitterState2)

    def save_layout_state(self):
        return
        splitter_state = self.ui.messagesTableAndViewSplitter.saveState()
        splitter_state2 = self.ui.messageViewWidget.ui.splitter.saveState()

        settings = AppSettings.get_instance()
        settings.save("WsPage.messagesTableAndViewSplitter", splitter_state)
        settings.save("WsPage.messageViewSplitterState", splitter_state2)

    def select_message(self, selected, deselected):
        if (len(selected.indexes()) > 0):
            selected_id_cols = list(filter(lambda i: i.column() == 0, selected.indexes()))
            selected_id = selected_id_cols[0].data()
            message = WsMessageRepo().find(selected_id)
            self.ui.messageViewWidget.set_message(message)

    def delete_messages(self, message_ids):
        if len(message_ids) > 1:
            message = f'Are you sure you want to delete {len(message_ids)} websocket messages?'
        else:
            message = 'Are you sure you want to delete this websocket message?'

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('PNTest')
        message_box.setText(message)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
        message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
        response = message_box.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            self.table_model.delete_messages(message_ids)

    def proxy_ws_message_received(self, ws_message: WebsocketMessage):
        self.table_model.add_message(ws_message)

    # def search_requests(self, search_text):
    #     # requests = HttpFlow.search({'search': search_text})
    #     # self.table_model.requests = requests
    #     # self.table_model.refresh()
    #     self.request_data = RequestData()
    #     self.request_data.set_filter_param('search', search_text)
    #     self.request_data.load_requests()
    #     self.table_model.requests = self.request_data.requests
    #     self.table_model.refresh()
