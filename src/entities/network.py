from dataclasses import dataclass
from typing import Optional

from entities.container import Container

# TODO: Use the real image
# from version import PROXY_DOCKER_IMAGE
PROXY_DOCKER_IMAGE = 'proxy:latest'


@dataclass(kw_only=True)
# A Docker network
class Network():
    id: str
    name: str
    scope: str
    driver: str
    labels: dict[str, str]
    raw_network: object
    subnet: str
    gateway: str
    containers: list[Container]

    def container_ids(self) -> list[str]:
        return list(self.raw_network.attrs['Containers'].keys()) # type: ignore

    def human_readable_desc(self) -> str:
        desc = f'ID: {self.id}\n'
        desc += f'Name: {self.name}\n'
        desc += f'Driver: {self.driver}\n'
        desc += f'Subnet: {self.subnet}\n'
        desc += f'Labels: {self.labels}'

        return desc

    def has_active_gateway_container(self) -> bool:
        container = self.gateway_container()
        if not container:
            return False

        return (container.status == 'running')

    def gateway_container(self) -> Optional[Container]:
        containers_found = [c for c in self.containers if c.image == PROXY_DOCKER_IMAGE]

        if len(containers_found) > 0:
            return containers_found[0]
