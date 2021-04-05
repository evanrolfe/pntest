from PySide2 import QtCore, QtGui, QtWidgets

from views._compiled.clients.ui_clients_page import Ui_ClientsPage

# from lib.backend import Backend
from models.qt.clients_table_model import ClientsTableModel
from models.data.client import Client

ENABLED_CLIENTS = ['anything']

class ClientsPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ClientsPage, self).__init__(*args, **kwargs)
        self.ui = Ui_ClientsPage()
        self.ui.setupUi(self)

        Client.where('open', '=', 1).update(open=0)
        clients = Client.all()
        self.clients_table_model = ClientsTableModel(clients)

        self.ui.clientsTable.setTableModel(self.clients_table_model)
        self.ui.clientsTable.open_client_clicked.connect(self.open_client_clicked)
        self.ui.clientsTable.close_client_clicked.connect(self.close_client_clicked)
        self.ui.clientsTable.bring_to_front_client_clicked.connect(self.bring_to_front_client_clicked)

        # Add Icons:
        self.ui.chromiumButton.setIcon(QtGui.QIcon(':/icons/icons8-chromium.svg'))
        self.ui.chromeButton.setIcon(QtGui.QIcon(':/icons/icons8-chrome.svg'))
        self.ui.firefoxButton.setIcon(QtGui.QIcon(':/icons/icons8-firefox.svg'))
        self.ui.anythingButton.setIcon(QtGui.QIcon(':/icons/icons8-question-mark.png'))

        # Connect client buttons:
        self.ui.chromiumButton.clicked.connect(lambda: self.create_client('chromium'))
        self.ui.chromeButton.clicked.connect(lambda: self.create_client('chrome'))
        self.ui.firefoxButton.clicked.connect(lambda: self.create_client('firefox'))
        self.ui.anythingButton.clicked.connect(lambda: self.create_client('anything'))
        self.ui.terminalButton.clicked.connect(lambda: self.create_client('terminal'))

        # Disable clients not available
        self.client_buttons = {
            'chromium': self.ui.chromiumButton,
            'chrome': self.ui.chromeButton,
            'firefox': self.ui.firefoxButton,
            'anything': self.ui.anythingButton
        }
        self.set_enabled_clients(ENABLED_CLIENTS)

    def reload(self):
        # self.ui.clientView.clear()
        self.reload_table_data()

    def reload_table_data(self):
        clients = Client.all()
        self.clients_table_model.set_clients(clients)

    @QtCore.Slot()
    def new_client_click(self):
        self.new_client_modal.show()

    @QtCore.Slot()
    def create_client(self, client_type):
        ports = Client.get_next_port_available()

        client = Client()
        client.type = client_type
        client.proxy_port = ports['proxy']

        if client_type != 'anything':
            client.browser_port = ports['browser']

        client.save()

        print(client)
        self.reload_table_data()

    def set_enabled_clients(self, enabled_clients):
        self.enabled_clients = enabled_clients

        for client in self.enabled_clients:
            button = self.client_buttons[client]
            button.setEnabled(True)

        # Update the anything button port
        # anything_client_info = self.get_client_info('anything')
        # self.ui.anythingButton.setText(f'Anything (Port {anything_client_info["proxyPort"]})')

    def get_client_info(self, browser_type):
        return 'TODO!'
        # client_infos = [c for c in self.enabled_clients if c == browser_type]

        # if len(client_infos) == 0:
        #     client_info = {'version': 'N/A', 'proxyPort': 'N/A',
        #                    'browserPort': 'N/A', 'command': 'N/A'}
        # else:
        #     client_info = client_infos[0]

        # return client_info

    @QtCore.Slot()
    def open_client_clicked(self, client):
        client.launch()
        self.reload_table_data()

    @QtCore.Slot()
    def close_client_clicked(self, client):
        client.close()
        self.reload_table_data()

    @QtCore.Slot()
    def bring_to_front_client_clicked(self, client):
        print(f'============> bring to front client {client}')
