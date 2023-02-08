from __future__ import annotations
import json
import os
import signal
import subprocess
from typing import Generic, Optional, Type, TypeVar
from models.app_settings import AppSettings
from models.available_client import AvailableClient
from models.container import Container
from models.client import Client
from models.process import Process
from models.project_settings import ProjectSettings
from lib.browser_launcher.launch_browser import launch_chrome_or_chromium, launch_firefox
from PyQt6 import QtCore
import docker

PROXY_DOCKER_IMAGE = 'pntest-proxy:latest'

class ContainerRepo(QtCore.QObject):
    containers: list[Container]
    docker: docker.DockerClient

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance() -> ContainerRepo:
        # Static access method.
        if ContainerRepo.__instance is None:
            ContainerRepo("")

        return ContainerRepo.__instance # type:ignore

    def __init__(self, app_path: str):
        super().__init__()

        self.docker = docker.from_env()

        # Virtually private constructor.
        if ContainerRepo.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ContainerRepo.__instance = self
    # /Singleton method stuff

    def get_all(self) -> list[Container]:
        containers = []
        raw_containers = self.docker.containers.list()
        for raw_container in raw_containers:
            container = self.__raw_container_to_container(raw_container)
            containers.append(container)

        return containers

    def find_by_short_id(self, short_id: str) -> Optional[Container]:
        containers = self.get_all()
        try:
            container = [c for c in containers if c.short_id == short_id][0]
        except IndexError:
            return

        return container

    # Starts a proxy container, then restarts the inputted container with its network set to the proxy
    # returns the newly restarted intercepted container and the proxy container instance.
    # TODO: Maybe this should just accept client, so its not "primitive obsession"...
    def proxify_container(self, container: Container, client_id: int) -> tuple[Container, Container]:
        if len(container.networks) > 1:
            raise Exception("The docker container must only be on a single network")
        network = container.networks[0]
        image = container.image

        # 1. Stop the running container
        print(f'Stopping container: {container.short_id}')
        container.raw_container.stop() # type:ignore
        print('Stopped.')

        # 2. Start a proxy container
        proxy_container_id = self.__run_proxy_container(container, client_id)
        # IMPORTANT: THIS NEEDS TO BE .get() because it calls docker inspect!!!
        proxy_raw_container = self.docker.containers.get(proxy_container_id)

        # 3. Restart the original container but with the network set to the proxy container
        intercepted_raw_container = self.docker.containers.run(
            image,
            detach=True,
            network=f'container:{proxy_raw_container.short_id}', # type:ignore
            links={}
        )
        print(f'Restarted container: {intercepted_raw_container.short_id}') # type:ignore

        intercepted_container = self.__raw_container_to_container(intercepted_raw_container)
        proxy_container = self.__raw_container_to_container(proxy_raw_container)

        return intercepted_container, proxy_container

    def close_container(self, container: Container):
        if container.raw_container is None:
            return
        container.raw_container.stop() # type:ignore

    def __raw_container_to_container(self, raw_container) -> Container:
        # print("---> Container: ", raw_container.short_id)
        # print(json.dumps(raw_container.attrs))
        return Container(
            short_id=raw_container.short_id,
            name=raw_container.name,
            status=raw_container.status,
            ports=raw_container.ports,
            image=raw_container.attrs['Config']['Image'],
            networks=list(raw_container.attrs['NetworkSettings']['Networks'].keys()),
            raw_container=raw_container,
        )

    # def close_container(self, container: Container):
    #     # container.kill()
    #     return

    def __run_proxy_container(self, container: Container, client_id: int) -> str:
        print(f'Starting proxy container with image: {PROXY_DOCKER_IMAGE}')
        # network = container.networks[0]
        proxy_env = [f'CLIENT_ID={client_id}', 'ZMQ_SERVER=host.docker.internal:5556']

        old_network_config = container.raw_container.attrs['NetworkSettings']['Networks']['example_app_default'] # type:ignore

        proxy_networking_config = self.docker.api.create_networking_config({
            # TODO: DONT HARDCODE THE NETWORK HERE!
            'example_app_default': self.docker.api.create_endpoint_config(
                aliases=old_network_config['Aliases'],
                links=old_network_config['Links']
            )
        })
        proxy_host_config = self.docker.api.create_host_config(
            port_bindings=container.ports, # type:ignore
            privileged=True,
        )
        exposed_ports = {}
        for export_port,_ in container.ports.items(): #type:ignore
            exposed_ports[export_port] = {}

        result = self.docker.api.create_container(
            PROXY_DOCKER_IMAGE,
            None,
            networking_config=proxy_networking_config,
            host_config=proxy_host_config,
            ports=exposed_ports,
            environment=proxy_env,
        )
        proxy_container_id = result['Id']
        print("Created proxy container id: ", proxy_container_id)

        self.docker.api.start(proxy_container_id)
        print(f'Started proxy container: {proxy_container_id}') # type:ignore

        return proxy_container_id
