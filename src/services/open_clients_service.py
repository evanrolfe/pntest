from __future__ import annotations

from typing import Optional

from PyQt6 import QtCore

from entities.available_client import AvailableClient
from entities.browser import Browser
from entities.client import Client
from entities.container import Container
from repos.app_settings_repo import AppSettingsRepo
from repos.available_client_repo import AvailableClientRepo
from repos.browser_repo import BrowserRepo
from repos.client_repo import ClientRepo
from repos.container_repo import ContainerRepo
from repos.process_repo import ProcessRepo


# OpenClientsService is a singleton class which keeps track of which clients are open
class OpenClientsService(QtCore.QObject):
    open_clients: list[Client]
    process_repo: ProcessRepo
    browser_repo: BrowserRepo

    clients_changed = QtCore.pyqtSignal()

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance() -> OpenClientsService:
        # Static access method.
        if OpenClientsService.__instance is None:
            OpenClientsService()

        return OpenClientsService.__instance # type:ignore

    def __init__(self):
        super().__init__()

        self.open_clients = []
        self.process_repo = ProcessRepo.get_instance()
        self.browser_repo = BrowserRepo.get_instance()
        self.container_repo = ContainerRepo.get_instance()
        self.browser_repo.browser_exited.connect(self.__browser_was_closed)

        # Virtually private constructor.
        if OpenClientsService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            OpenClientsService.__instance = self
    # /Singleton method stuff

    # Return the containers which can be intercepted with a proxy
    def get_interceptable_containers(self) -> list[Container]:
        original_container_ids = [c.container_id for c in ClientRepo().find_all() if c.type == 'docker']
        intercepted_container_ids = [c.intercepted_container.short_id for c in self.open_clients if c.intercepted_container]
        proxy_container_ids = [c.proxy_container.short_id for c in self.open_clients if c.proxy_container]

        do_not_intercept_container_ids = original_container_ids + intercepted_container_ids + proxy_container_ids
        all_containers = self.container_repo.get_all()

        return [c for c in all_containers if c.short_id not in do_not_intercept_container_ids]

    # The message that will be displayed to the user when they exit the application
    def on_exit_message(self) -> str:
        msg = f'You have {len(self.open_docker_clients())} open docker clients. These will be stopped now, please allow up to a minute for the containers to be stopped.'
        return msg

    def open_docker_clients(self) -> list[Client]:
        return [c for c in self.open_clients if c.type == 'docker']

    def build_client(self, client_type: str, container: Optional[Container] = None) -> Client:
        if client_type == 'docker':
            if container is None:
                raise Exception("no container given for docker client")

            return Client(
                type = 'docker',
                proxy_port = 0,
                title = container.host_name,
                intercepted_container=container,
                container_id=container.short_id
            )
        else:
            port = self.__get_first_port_available()
            return Client(
                type = client_type,
                proxy_port = port,
                title = client_type
            )

    def launch_client(self, client: Client):
        if client.type == 'docker':
            if client.container_id is None:
                raise Exception("no container_id on client")

            # 1. Get the running container to intercept if its not already there
            # TODO: This probably isn't going to work if client.intercepted_container is set
            # becuase intercepted_container comes from ContainerRepo.get_all() which annoyingly doesn't
            # return as much details (i.e. network aliases are not included in the response)
            # so this should be changed to use ContainerRepo.find_by_short_id() which call docker inspect under the bonnet
            if client.intercepted_container is None:
                container = self.container_repo.find_by_short_id(client.container_id)
                if container is None:
                    raise Exception("no running container found with id: ", client.container_id)
                client.intercepted_container = container

            # 2. Proxify the running container
            new_intercepted, proxy = self.container_repo.proxify_container(client.intercepted_container, client.id)
            client.intercepted_container = new_intercepted
            client.proxy_container = proxy
        else:
            # 1. Get the available client details
            available_client = self.__get_available_client_for_client(client)

            # 2. Launch the proxy
            proxy_proc = self.process_repo.launch_proxy(client)
            client.proxy = proxy_proc

            # 3. Optionally launch the browser
            if client.is_browser() and available_client.command is not None:
                browser = self.browser_repo.launch_browser(client, available_client.command)
                client.browser = browser

        # 4. Save to open_clients
        self.open_clients.append(client)

    def close_client(self, client: Client):
        # NOTE: This is necessary because the clients objects stored in the widget table may be different
        # from the ones in self.open_clients. The widget code could be refactored so we don't need this..
        open_client = self.__get_open_client(client)
        if open_client is None:
            return

        if client.type == 'docker':
            # 1. Close the client's proxy container
            if open_client.proxy_container is None or open_client.intercepted_container is None:
                return

            self.container_repo.close_container(open_client.proxy_container)
            self.container_repo.close_container(open_client.intercepted_container)

        else:
            # 1.1 Close the client's proxy
            if open_client.proxy is not None:
                self.process_repo.close_proxy(open_client.proxy)

            # 1.2. Optionally close the client's browser
            if open_client.browser is not None:
                self.browser_repo.close_browser(open_client.browser)

        # 3. Set the client to closed and update the widget (via a signal)
        open_client.open = False
        ClientRepo().save(open_client)

        # 4. Remove from open_clients
        self.open_clients.remove(open_client)

        # 5. Emit signal
        self.clients_changed.emit()

    def on_exit(self):
        print("[OpenClientsService] killing all clients...")
        for open_client in self.open_clients:
            print("[OpenClientsService] closing ", open_client.title)
            self.close_client(open_client)

    def __browser_was_closed(self, browser: Browser):
        open_client = self.__get_open_client_for_browser(browser)
        if open_client is None:
            return

        # 1. Close the client's proxy
        if open_client.proxy is not None:
            self.process_repo.close_proxy(open_client.proxy)

        # 2. Set the client to closed and update the widget (via a signal)
        open_client.open = False
        ClientRepo().save(open_client)

        # 3. Remove from open_clients
        self.open_clients.remove(open_client)

        # 4. Emit signal
        self.clients_changed.emit()

    def __get_available_client_for_client(self, client: Client) -> AvailableClient:
        settings = AppSettingsRepo().get()
        available_clients = AvailableClientRepo().find_all_with_settings_override(settings)
        available_client = [c for c in available_clients if c.name == client.type][0]

        if available_client is None:
            raise Exception(f"no available client command found for client type {client.type}")

        return available_client

    def __get_open_client_for_browser(self, browser: Browser) -> Optional[Client]:
        try:
            open_client = [c for c in self.open_clients if c.browser == browser == browser][0]
        except IndexError:
            return None
        return open_client

    def __get_open_client(self, client: Client) -> Optional[Client]:
        try:
            open_client = [c for c in self.open_clients if c.id == client.id][0]
        except IndexError:
            return None
        return open_client

    def __get_first_port_available(self) -> int:
        settings = AppSettingsRepo().get()
        available_ports = settings['proxy_ports_available']
        used_ports = ClientRepo().get_used_ports()
        first_port_available = None

        for available_port in available_ports:
            if available_port not in used_ports:
                first_port_available = available_port
                break

        if first_port_available is None:
            raise Exception("no more ports available! add some in the settings.")

        return first_port_available
