from PyQt6 import QtCore, QtGui, QtWidgets

from entities.available_client import AvailableClient
from entities.client import Client
from entities.container import Container
from lib.background_worker import BackgroundWorker
from repos.client_repo import ClientRepo
from repos.container_repo import PROXY_DOCKER_IMAGE
from services.available_clients_service import AvailableClientsService
from services.open_clients_service import OpenClientsService
from services.proxy_service import ProxyService
from ui.views._compiled.clients.clients_page import Ui_ClientsPage
from ui.widgets.clients.docker_window import DockerWindow


class ClientsPage(QtWidgets.QWidget):
    clients_changed = QtCore.pyqtSignal()

    proxy_service: ProxyService
    open_clients_service: OpenClientsService
    available_clients: list[AvailableClient]
    threadpool: QtCore.QThreadPool

    def __init__(self, *args, **kwargs):
        super(ClientsPage, self).__init__(*args, **kwargs)
        self.ui = Ui_ClientsPage()
        self.ui.setupUi(self)

        self.ui.clientsTable.open_client_clicked.connect(self.open_client_clicked_async)
        self.ui.clientsTable.close_client_clicked.connect(self.close_client_clicked_async)
        self.ui.clientsTable.clients_changed.connect(self.clients_changed)

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
        self.ui.clientsTable.reload()

    def create_client(self, client_type: str):
        if client_type != 'docker':
            client = self.open_clients_service.build_client(client_type)
            ClientRepo().save(client)
            self.open_client_clicked_async(client)
            return

        if not self.open_clients_service.container_repo.has_proxy_image_downloaded():
            message_box = QtWidgets.QMessageBox()
            # message_box.setWindowTitle('PNTest')
            message_box.setText(f"You must download the PnTest proxy image with this command, then try again:\ndocker pull {PROXY_DOCKER_IMAGE}")
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.exec()
            return

        self.docker_window.show()
        return

    def create_clients_for_containers(self, containers: list[Container]):
        for container in containers:
            print(f'Building client for container id {container.short_id}')
            client = self.open_clients_service.build_client('docker', container)
            ClientRepo().save(client)
            print(client, "\n")
            self.reload()
            self.open_client_clicked_async(client)

    def load_available_clients(self):
        available_clients = AvailableClientsService().get_all()

        for key, button in self.client_buttons.items():
            available_client = [ac for ac in available_clients if ac.name == key][0]
            button.setEnabled(available_client.enabled())

    def open_client_clicked_async(self, client: Client):
        worker = BackgroundWorker(lambda x: self.open_clients_service.launch_client(client))
        worker.signals.error.connect(self.client_error)
        worker.signals.finished.connect(self.reload)
        self.threadpool.start(worker)
        self.reload()

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
        worker.signals.finished.connect(self.reload)
        self.threadpool.start(worker)
        self.reload()
