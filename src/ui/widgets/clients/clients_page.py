from PyQt6 import QtCore, QtGui, QtWidgets
from lib.background_worker import BackgroundWorker
from entities.container import Container
from services.available_clients_service import AvailableClientsService
from services.open_clients_service import OpenClientsService
from repos.client_repo import ClientRepo
from entities.available_client import AvailableClient
from services.proxy_service import ProxyService

from ui.views._compiled.clients.clients_page import Ui_ClientsPage

from ui.qt_models.clients_table_model import ClientsTableModel
from entities.client import Client
from ui.widgets.clients.docker_window import DockerWindow

class ClientsPage(QtWidgets.QWidget):
    proxy_service: ProxyService
    open_clients_service: OpenClientsService
    available_clients: list[AvailableClient]
    threadpool: QtCore.QThreadPool

    def __init__(self, *args, **kwargs):
        super(ClientsPage, self).__init__(*args, **kwargs)
        self.ui = Ui_ClientsPage()
        self.ui.setupUi(self)

        ClientRepo().update_all_to_closed()
        clients = ClientRepo().find_all()
        self.clients_table_model = ClientsTableModel(clients)

        self.ui.clientsTable.setTableModel(self.clients_table_model)
        self.ui.clientsTable.open_client_clicked.connect(self.open_client_clicked_async)
        self.ui.clientsTable.close_client_clicked.connect(self.close_client_clicked_async)

        # Add Icons:
        self.ui.chromiumButton.setIcon(QtGui.QIcon('assets:icons/icons8-chromium.svg'))
        self.ui.chromeButton.setIcon(QtGui.QIcon('assets:icons/icons8-chrome.svg'))
        self.ui.firefoxButton.setIcon(QtGui.QIcon('assets:icons/icons8-firefox.svg'))
        self.ui.dockerButton.setIcon(QtGui.QIcon('assets:icons/icons8-docker.svg'))
        self.ui.anythingButton.setIcon(QtGui.QIcon('assets:icons/icons8-question-mark.png'))

        # Connect client buttons:
        self.ui.chromiumButton.clicked.connect(lambda: self.create_client('chromium'))
        self.ui.chromeButton.clicked.connect(lambda: self.create_client('chrome'))
        self.ui.firefoxButton.clicked.connect(lambda: self.create_client('firefox'))
        self.ui.dockerButton.clicked.connect(lambda: self.create_client('docker'))
        self.ui.anythingButton.clicked.connect(lambda: self.create_client('anything'))

        # Disable clients not available
        self.client_buttons = {
            'chrome': self.ui.chromeButton,
            'chromium': self.ui.chromiumButton,
            'firefox': self.ui.firefoxButton,
            'docker': self.ui.dockerButton,
            'anything': self.ui.anythingButton
        }
        self.load_available_clients()

        self.proxy_service = ProxyService.get_instance()
        self.open_clients_service = OpenClientsService.get_instance()

        self.proxy_service.process_manager.clients_changed.connect(self.reload)
        self.open_clients_service.clients_changed.connect(self.reload)

        self.docker_window = DockerWindow(self)
        self.docker_window.proxify_containers.connect(self.create_clients_for_containers)

        self.threadpool = QtCore.QThreadPool()

    def reload(self):
        self.reload_table_data()

    def reload_table_data(self):
        clients = ClientRepo().find_all()
        self.clients_table_model.set_clients(clients)

    def create_client(self, client_type: str):
        if client_type == 'docker':
            self.docker_window.show()
            return

        client = self.open_clients_service.build_client(client_type)
        ClientRepo().save(client)
        self.open_client_clicked_async(client)

    def create_clients_for_containers(self, containers: list[Container]):
        for container in containers:
            print(f'Building client for container id {container.short_id}')
            client = self.open_clients_service.build_client('docker', container)
            ClientRepo().save(client)
            print(client, "\n")
            self.reload_table_data()
            self.open_client_clicked_async(client)

    def load_available_clients(self):
        available_clients = AvailableClientsService().get_all()

        for key, button in self.client_buttons.items():
            available_client = [ac for ac in available_clients if ac.name == key][0]
            button.setEnabled(available_client.enabled())

    def open_client_clicked_async(self, client: Client):
        worker = BackgroundWorker(lambda x: self.open_clients_service.launch_client(client))
        worker.signals.error.connect(self.client_error)
        worker.signals.finished.connect(self.reload_table_data)
        self.threadpool.start(worker)
        self.reload_table_data()

    def client_error(self, err):
        raise Exception(err)

    def close_client_clicked_async(self, client: Client):
        if client.type == 'docker':
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Warning')
            message_box.setText(
                f'WARNING: The intercepted container will be stopped. Please start the container again if you wish to continue running it.'
            )
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
            message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
            response = message_box.exec()

            if response != QtWidgets.QMessageBox.StandardButton.Yes:
                return

        worker = BackgroundWorker(lambda x: self.open_clients_service.close_client(client))
        worker.signals.error.connect(self.client_error)
        worker.signals.finished.connect(self.reload_table_data)
        self.threadpool.start(worker)
        self.reload_table_data()