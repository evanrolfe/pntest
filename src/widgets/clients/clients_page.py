from PySide2 import QtCore, QtGui, QtWidgets

from views._compiled.clients.ui_clients_page import Ui_ClientsPage

from lib.backend import Backend
from models.qt.clients_table_model import ClientsTableModel
from models.data.client import Client

CHROMIUM_COMMAND = b'{"command": "createClient", "type": "chromium"}'
CHROME_COMMAND = b'{"command": "createClient", "type": "chrome"}'
FIREFOX_COMMAND = b'{"command": "createClient", "type": "firefox"}'
ANYTHING_COMMAND = b'{"command": "createClient", "type": "anything"}'

class ClientsPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ClientsPage, self).__init__(*args, **kwargs)
        self.ui = Ui_ClientsPage()
        self.ui.setupUi(self)

        clients = Client.all()
        self.clients_table_model = ClientsTableModel(clients)

        self.ui.clientsTable.setTableModel(self.clients_table_model)

        # Reload when the clients have changed:
        self.backend = Backend.get_instance()
        self.backend.register_callback(
            'clientsChanged', self.reload_table_data)

        # Add Icons:
        self.ui.chromiumButton.setIcon(QtGui.QIcon(':/icons/icons8-chromium.svg'))
        self.ui.chromeButton.setIcon(QtGui.QIcon(':/icons/icons8-chrome.svg'))
        self.ui.firefoxButton.setIcon(QtGui.QIcon(':/icons/icons8-firefox.svg'))
        self.ui.anythingButton.setIcon(QtGui.QIcon(':/icons/icons8-question-mark.png'))

        # Connect client buttons:
        self.ui.chromiumButton.clicked.connect(
            lambda: self.launch_client('chromium'))
        self.ui.chromeButton.clicked.connect(
            lambda: self.launch_client('chrome'))
        self.ui.firefoxButton.clicked.connect(
            lambda: self.launch_client('firefox'))
        self.ui.anythingButton.clicked.connect(
            lambda: self.launch_client('anything'))
        self.ui.terminalButton.clicked.connect(
            lambda: self.launch_client('terminal'))

        # Register callback with the backend:
        self.backend = Backend.get_instance()
        self.backend.register_callback('clientsAvailable', self.set_clients)

        # Disable clients not available
        self.client_buttons = {
            'chromium': self.ui.chromiumButton,
            'chrome': self.ui.chromeButton,
            'firefox': self.ui.firefoxButton,
            'anything': self.ui.anythingButton
        }
        self.clients = []

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
    def launch_client(self, client_type):
        launch_commands = {
            'chromium': CHROMIUM_COMMAND,
            'chrome': CHROME_COMMAND,
            'firefox': FIREFOX_COMMAND,
            'anything': ANYTHING_COMMAND,
            'terminal': 'TODO',
        }
        command = launch_commands[client_type]
        print(f'Launching {client_type} with command: {command}')
        self.backend.send_command(command)

    def showEvent(self, event):
        self.backend.get_available_clients()

    def set_clients(self, clients):
        self.clients = clients

        for client in clients:
            button = self.client_buttons[client['name']]
            button.setEnabled(True)

        # Update the anything button port
        anything_client_info = self.get_client_info('anything')
        self.ui.anythingButton.setText(
            f'Anything (Port {anything_client_info["proxyPort"]})')

    def get_client_info(self, browser_type):
        client_infos = [c for c in self.clients if c['type'] == browser_type]

        if len(client_infos) == 0:
            client_info = {'version': 'N/A', 'proxyPort': 'N/A',
                           'browserPort': 'N/A', 'command': 'N/A'}
        else:
            client_info = client_infos[0]

        return client_info
