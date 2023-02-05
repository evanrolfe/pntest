from typing import Optional
from PyQt6 import QtWidgets, QtCore
from repos.container_repo import ContainerRepo
from repos.project_settings_repo import ProjectSettingsRepo
from repos.app_settings_repo import AppSettingsRepo
from repos.available_client_repo import AvailableClientRepo
from models.available_client import AvailableClient
from services.client_service import ClientService
from views._compiled.clients.docker_window import Ui_DockerWindow

class DockerWindow(QtWidgets.QDialog):
    # available_clients: list[AvailableClient]
    # browser_commands: dict[str, dict[str, str]]
    # network_layout_changed = QtCore.pyqtSignal(str)
    # app_settings_saved = QtCore.pyqtSignal()
    container_repo: ContainerRepo
    client_service: ClientService

    check_boxes: list[QtWidgets.QCheckBox]

    def __init__(self, *args, **kwargs):
        super(DockerWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_DockerWindow()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)

        self.container_repo = ContainerRepo.get_instance()
        self.client_service = ClientService.get_instance()
        self.check_boxes = []

        self.load_containers()

    def showEvent(self, event):
        self.load_containers()

    def save(self):
        self.close()

    def load_containers(self):
        # Clear existing check boxes
        for check_box in self.check_boxes:
            self.ui.verticalLayout_2.removeWidget(check_box)

        # Load the containers and display new check boxes
        containers = self.container_repo.get_all()
        self.check_boxes = []

        for container in containers:
            check_box = QtWidgets.QCheckBox(self)
            check_box.setObjectName(f"container{container.short_id}")
            check_box.setText(f"Container ID: {container.short_id} | Image: {container.image} | Ports: {container.ports} | Name: {container.name} |  Networks: {container.networks}")
            check_box.setChecked(True)
            self.ui.verticalLayout_2.addWidget(check_box)
            self.check_boxes.append(check_box)
