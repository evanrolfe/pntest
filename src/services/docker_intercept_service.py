from __future__ import annotations

from entities.available_client import AvailableClient
from entities.container import Container
from entities.network import Network
from repos.app_settings_repo import AppSettingsRepo
from repos.available_client_repo import AvailableClientRepo
from repos.container_repo import ContainerRepo


# DockerInterceptService first ensures a gateway container is running in the network, then
# points the container to use that gateway
class DockerInterceptService():
    def __init__(self):
        super().__init__()

    def run(self, network: Network, container: Container):
        # 1. Check ip & curl installed on container
        if not container.has_tools_installed():
            raise Exception("the container needs to have ip & curl installed!")

        # 2. Enure gateway container is running
        gateway_container = network.gateway_container()
        if gateway_container is None:
            gateway_container = ContainerRepo.get_instance().run_gateway_container(network)
            print("Started new gateway container: ", gateway_container.short_id)
        else:
            print("Found running gateway container: ", gateway_container.short_id)

        print("Gateway IP: ", gateway_container.ip)

        # 3. Set the gateway on the container
        container.set_gateway(gateway_container)
