from __future__ import annotations

import json
import platform
from typing import Optional

import docker
from docker.types.services import Mount
from PyQt6 import QtCore

from entities.network import Network
from lib.utils import get_local_ip_addr, is_test_env
from version import PROXY_DOCKER_IMAGE


class NetworkRepo(QtCore.QObject):
    networks: list[Network]
    docker: Optional[docker.DockerClient]

    def __init__(self):
        super().__init__()

        try:
            self.docker = docker.from_env()
        except:
            self.docker = None

    def get_all(self) -> list[Network]:
        if self.docker is None:
            raise Exception("docker is not available!")

        networks = []
        partial_networks = self.docker.networks.list()
        for partial_network in partial_networks:
            raw_network = self.docker.networks.get(partial_network.id)
            network = self.__raw_network_to_network(raw_network)
            networks.append(network)

        return networks

    def __raw_network_to_network(self, raw_network) -> Network:
        subnet = ''
        gateway = ''

        if len(raw_network.attrs['IPAM']['Config']) > 0:
            subnet = raw_network.attrs['IPAM']['Config'][0]['Subnet']
            gateway = raw_network.attrs['IPAM']['Config'][0]['Gateway']

        return Network(
            id=raw_network.attrs['Id'],
            name=raw_network.attrs['Name'],
            scope=raw_network.attrs['Scope'],
            driver=raw_network.attrs['Driver'],
            labels=raw_network.attrs['Labels'],
            raw_network=raw_network,
            subnet=subnet,
            gateway=gateway,
        )
