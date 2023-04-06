from __future__ import annotations

from entities.available_client import AvailableClient
from entities.container import Container
from entities.network import Network
from repos.app_settings_repo import AppSettingsRepo
from repos.available_client_repo import AvailableClientRepo
from repos.container_repo import ContainerRepo
from version import PROXY_DOCKER_IMAGE_TAG


# DockerService
class DockerService():
    def __init__(self):
        super().__init__()

    def load_containers_to_network(self, network: Network):
        containers = ContainerRepo.get_instance().find_by_ids(network.container_ids())
        network.containers = containers

        for container in containers:
            print(f"Container: {container.short_id}, interception_active: {container.interception_active} network has gateway? {network.has_active_gateway_container()}")
            if not network.has_active_gateway_container():
                container.interception_active = False


