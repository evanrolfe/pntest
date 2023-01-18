from PyQt6 import QtCore, QtGui, QtWidgets
from models.settings import Settings
from repos.client_repo import ClientRepo
from repos.settings_repo import SettingsRepo
from repos.available_client_repo import AvailableClientRepo
from models.available_client import AvailableClient

from views._compiled.clients.clients_page import Ui_ClientsPage

from models.qt.clients_table_model import ClientsTableModel
from models.client import Client
from lib.process_manager import ProcessManager

class ClientsPage(QtWidgets.QWidget):
    process_manager: ProcessManager
    available_clients: list[AvailableClient]

    def __init__(self, *args, **kwargs):
        super(ClientsPage, self).__init__(*args, **kwargs)
        self.ui = Ui_ClientsPage()
        self.ui.setupUi(self)

        ClientRepo().update_all_to_closed()
        clients = ClientRepo().find_all()
        self.clients_table_model = ClientsTableModel(clients)

        self.ui.clientsTable.setTableModel(self.clients_table_model)
        self.ui.clientsTable.open_client_clicked.connect(self.open_client_clicked)
        self.ui.clientsTable.close_client_clicked.connect(self.close_client_clicked)

        # Add Icons:
        self.ui.chromiumButton.setIcon(QtGui.QIcon('assets:icons/icons8-chromium.svg'))
        self.ui.chromeButton.setIcon(QtGui.QIcon('assets:icons/icons8-chrome.svg'))
        self.ui.firefoxButton.setIcon(QtGui.QIcon('assets:icons/icons8-firefox.svg'))
        self.ui.anythingButton.setIcon(QtGui.QIcon('assets:icons/icons8-question-mark.png'))

        # Connect client buttons:
        self.ui.chromiumButton.clicked.connect(lambda: self.create_client('chromium'))
        self.ui.chromeButton.clicked.connect(lambda: self.create_client('chrome'))
        self.ui.firefoxButton.clicked.connect(lambda: self.create_client('firefox'))
        self.ui.anythingButton.clicked.connect(lambda: self.create_client('anything'))
        self.ui.terminalButton.clicked.connect(lambda: self.create_client('terminal'))

        # Disable clients not available
        self.client_buttons = {
            'chrome': self.ui.chromeButton,
            'chromium': self.ui.chromiumButton,
            'firefox': self.ui.firefoxButton,
            'anything': self.ui.anythingButton
        }
        self.load_available_clients()

        self.process_manager = ProcessManager.get_instance()
        self.process_manager.clients_changed.connect(self.reload)

    def showEvent(self, event):
        self.load_available_clients()

    def reload(self):
        self.reload_table_data()

    def reload_table_data(self):
        clients = ClientRepo().find_all()
        self.clients_table_model.set_clients(clients)

    def create_client(self, client_type):
        # TODO: Move this logic out of the widget and into a model or class somewhere
        settings = SettingsRepo().get_settings()
        available_ports = settings.json['proxy']['ports_available']
        used_ports = ClientRepo().get_used_ports()
        first_port_available = None

        for available_port in available_ports:
            if available_port not in used_ports:
                first_port_available = available_port
                break

        if first_port_available is None:
            raise Exception("no more ports available! add some in the settings.")

        client = Client(
            type = client_type,
            proxy_port = first_port_available,
            title = 'client'
        )

        ClientRepo().save(client)

        self.open_client_clicked(client)

    def load_available_clients(self):
        settings = SettingsRepo().get_settings()
        self.available_clients = AvailableClientRepo().find_all_with_settings_override(settings)

        for key, button in self.client_buttons.items():
            available_client = [ac for ac in self.available_clients if ac.name == key][0]
            button.setEnabled(available_client.enabled())

    def open_client_clicked(self, client: Client):
        available_client = [c for c in self.available_clients if c.name == client.type][0]

        settings = SettingsRepo().get_settings()
        self.process_manager.launch_client(client, available_client, settings.json)
        self.reload_table_data()

    def close_client_clicked(self, client: Client):
        self.process_manager.close_client(client)
        self.reload_table_data()
