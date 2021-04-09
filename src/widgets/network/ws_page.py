from PySide2 import QtCore, QtWidgets

from views._compiled.network.ui_ws_page import Ui_WsPage

from lib.app_settings import AppSettings
from models.qt.messages_table_model import MessagesTableModel
from models.data.websocket_message import WebsocketMessage

class WsPage(QtWidgets.QWidget):
    toggle_page = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(WsPage, self).__init__(*args, **kwargs)
        self.ui = Ui_WsPage()
        self.ui.setupUi(self)

        # Setup the table model
        messages = WebsocketMessage.order_by('id', 'desc').get()

        self.table_model = MessagesTableModel(messages)
        self.ui.messagesTable.setTableModel(self.table_model)

        self.ui.toggleButton.clicked.connect(self.toggle_page)
        self.ui.messagesTable.row_selected.connect(self.select_message)
        self.ui.messagesTable.delete_rows.connect(self.delete_messages)
        # self.ui.messagesTable.search_text_changed.connect(self.search_requests)

        self.restore_layout_state()

    def reload(self):
        self.ui.messageViewWidget.clear_request()
        messages = WebsocketMessage.order_by('id', 'desc').get()
        self.table_model = MessagesTableModel(messages)
        self.ui.messagesTable.setTableModel(self.table_model)

    def restore_layout_state(self):
        settings = AppSettings.get_instance()
        splitterState = settings.get("WsPage.messagesTableAndViewSplitter", None)
        splitterState2 = settings.get("WsPage.messageViewSplitterState", None)

        self.ui.messagesTableAndViewSplitter.restoreState(splitterState)
        self.ui.messageViewWidget.ui.splitter.restoreState(splitterState2)

    def save_layout_state(self):
        splitter_state = self.ui.messagesTableAndViewSplitter.saveState()
        splitter_state2 = self.ui.messageViewWidget.ui.splitter.saveState()

        settings = AppSettings.get_instance()
        settings.save("WsPage.messagesTableAndViewSplitter", splitter_state)
        settings.save("WsPage.messageViewSplitterState", splitter_state2)

    @QtCore.Slot()
    def select_message(self, selected, deselected):
        if (len(selected.indexes()) > 0):
            selected_id_cols = list(filter(lambda i: i.column() == 0, selected.indexes()))
            selected_id = selected_id_cols[0].data()
            message = WebsocketMessage.find(selected_id)
            self.ui.messageViewWidget.set_message(message)

    @QtCore.Slot()
    def delete_messages(self, message_ids):
        if len(message_ids) > 1:
            message = f'Are you sure you want to delete {len(message_ids)} websocket messages?'
        else:
            message = 'Are you sure you want to delete this websocket message?'

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('PNTest')
        message_box.setText(message)
        message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        message_box.setDefaultButton(QtWidgets.QMessageBox.Yes)
        response = message_box.exec_()

        if response == QtWidgets.QMessageBox.Yes:
            self.table_model.delete_messages(message_ids)

    @QtCore.Slot()
    def websocket_message_created(self, websocket_message):
        self.table_model.add_message(websocket_message)

    # @QtCore.Slot()
    # def search_requests(self, search_text):
    #     # requests = HttpFlow.search({'search': search_text})
    #     # self.table_model.requests = requests
    #     # self.table_model.refresh()
    #     self.request_data = RequestData()
    #     self.request_data.set_filter_param('search', search_text)
    #     self.request_data.load_requests()
    #     self.table_model.requests = self.request_data.requests
    #     self.table_model.refresh()
