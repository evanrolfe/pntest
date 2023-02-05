from __future__ import annotations
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
    def proxify_container(self, container: Container) -> tuple[Container, Container]:
        if len(container.networks) > 1:
            raise Exception("The docker container must only be on a single network")
        network = container.networks[0]
        image = container.image

        # 1. Stop the running container
        print(f'Stopping container: {container.short_id}')
        container.raw_container.stop() # type:ignore
        print('Stopped.')

        # 2. Start a proxy container
        print(f'Starting proxy container with image: {PROXY_DOCKER_IMAGE}')
        proxy_env = ['CLIENT_ID=2', 'ZMQ_SERVER=host.docker.internal:5556']
        proxy_raw_container = self.docker.containers.run(
            PROXY_DOCKER_IMAGE,
            detach=True,
            privileged=True,
            environment=proxy_env,
            ports=container.ports,  #type:ignore
            network=network
        )
        print(f'Started proxy container: {proxy_raw_container.short_id}') # type:ignore

        # 3. Restart the original container but with the network set to the proxy container
        intercepted_raw_container = self.docker.containers.run(
            image,
            detach=True,
            network=f'container:{proxy_raw_container.short_id}' # type:ignore
        )
        print(f'Restarted container: {intercepted_raw_container.short_id}') # type:ignore

        intercepted_container = self.__raw_container_to_container(intercepted_raw_container)
        proxy_container = self.__raw_container_to_container(proxy_raw_container)

        return intercepted_container, proxy_container

    def __raw_container_to_container(self, raw_container) -> Container:
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
