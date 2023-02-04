from __future__ import annotations
from typing import Optional
from PyQt6 import QtCore
from models.available_client import AvailableClient
from models.browser import Browser
from models.client import Client
from repos.browser_repo import BrowserRepo
from repos.client_repo import ClientRepo
from repos.process_repo import ProcessRepo
from repos.project_settings_repo import ProjectSettingsRepo
from repos.app_settings_repo import AppSettingsRepo
from repos.available_client_repo import AvailableClientRepo

class ClientService(QtCore.QObject):
    open_clients: list[Client]
    process_repo: ProcessRepo
    browser_repo: BrowserRepo

    clients_changed = QtCore.pyqtSignal()

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance() -> ClientService:
        # Static access method.
        if ClientService.__instance is None:
            ClientService()

        return ClientService.__instance # type:ignore

    def __init__(self):
        super().__init__()

        self.open_clients = []
        self.process_repo = ProcessRepo.get_instance()
        self.browser_repo = BrowserRepo.get_instance()
        self.browser_repo.browser_exited.connect(self.__browser_was_closed)

        # Virtually private constructor.
        if ClientService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ClientService.__instance = self
    # /Singleton method stuff

    def launch_client(self, client: Client):
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

        # 1. Close the client's proxy
        if open_client.proxy is not None:
            self.process_repo.close_proxy(open_client.proxy)

        # 2. Optionally close the client's browser
        if open_client.browser is not None:
            self.browser_repo.close_browser(open_client.browser)

        # 3. Set the client to closed and update the widget (via a signal)
        open_client.open = False
        ClientRepo().save(open_client)
        self.clients_changed.emit()

        # 4. Remove from open_clients
        self.open_clients.remove(open_client)

    def on_exit(self):
        print("[ClientService] killing all clients...")
        for open_client in self.open_clients:
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
        self.clients_changed.emit()

        # 3. Remove from open_clients
        self.open_clients.remove(open_client)

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
