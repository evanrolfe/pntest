from PyQt6 import QtCore, QtWidgets

from entities.container import Container
from repos.container_repo import ContainerRepo
from ui.views._compiled.clients.docker_window import Ui_DockerWindow


class DockerWindow(QtWidgets.QDialog):
    proxify_containers = QtCore.pyqtSignal(list)
    container_repo: ContainerRepo

    check_boxes_and_containers: dict[QtWidgets.QCheckBox, Container]

    def __init__(self, *args, **kwargs):
        super(DockerWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_DockerWindow()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)

        self.container_repo = ContainerRepo.get_instance()
        self.check_boxes_and_containers = {}

        self.load_containers()

    def showEvent(self, event):
        self.load_containers()

    def save(self):
        containers_to_proxify = []
        for check_box, container in self.check_boxes_and_containers.items():
            if check_box.isChecked():
                containers_to_proxify.append(container)

        self.proxify_containers.emit(containers_to_proxify)
        self.close()

    def load_containers(self):
        if not self.container_repo.has_docker_available():
            return

        # Clear existing check boxes
        for check_box,_ in self.check_boxes_and_containers.items():
            self.ui.verticalLayout_2.removeWidget(check_box)

        # Load the containers and display new check boxes
        containers = self.container_repo.get_all()
        self.check_boxes_and_containers = {}

        for container in containers:
            check_box = QtWidgets.QCheckBox(self)
            check_box.setObjectName(f"container_{container.short_id}")
            check_box.setText(f"Container ID: {container.short_id} | Name: {container.name} | Image: {container.image}")
            check_box.setChecked(False)
            self.ui.verticalLayout_2.addWidget(check_box)
            self.check_boxes_and_containers[check_box] = container
