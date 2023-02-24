import os
import signal
import sqlite3
import time
import pytestqt
from pytestqt.qtbot import QtBot
from entities.client import Client
from entities.process import Process
from repos.app_settings_repo import AppSettingsRepo
from repos.client_repo import ClientRepo
from repos.process_repo import ProcessRepo
from services.open_clients_service import OpenClientsService
from lib.paths import get_app_path

class TestClientService:
    def test_launching_an_anything_client_and_closing(self, database, cleanup_database):
        app_path = get_app_path()
        src_path = os.path.join(app_path, 'src')
        process_repo = ProcessRepo.get_instance()
        process_repo.set_app_path(str(src_path))

        # Create the Client
        client_repo = ClientRepo()
        client = Client(title="test client", type="anything", proxy_port=8080)
        client_repo.save(client)

        # Start the client
        client_service = OpenClientsService.get_instance()
        client_service.launch_client(client)

        assert len(client_service.open_clients) == 1
        assert client.proxy is not None
        assert client.proxy.proc is not None
        assert client.proxy.proc.pid > 0
        time.sleep(1)

        # Close the client
        client_service.close_client(client)
        assert len(client_service.open_clients) == 0

    def test_launching_a_chrome_client_and_closing(self, database, cleanup_database):
        app_path = get_app_path()
        src_path = os.path.join(app_path, 'src')
        process_repo = ProcessRepo.get_instance()
        process_repo.set_app_path(str(src_path))

        # Set chrome browser to use our fake_browser executable
        app_settings = AppSettingsRepo().get()
        app_settings["browser_commands"]["chrome"] = "./test/fake_browser"
        AppSettingsRepo().save(app_settings)

        # Create the Client
        client_repo = ClientRepo()
        client = Client(title="test client", type="chrome", proxy_port=8080)
        client_repo.save(client)

        # Start the client
        client_service = OpenClientsService.get_instance()
        client_service.launch_client(client)

        assert len(client_service.open_clients) == 1
        assert client.proxy is not None
        assert client.proxy.proc is not None
        assert client.proxy.proc.pid > 0

        time.sleep(1)
        assert client.browser is not None
        assert client.browser.proc is not None
        assert client.browser.proc.pid > 0

        # Close the client
        client_service.close_client(client)
        assert len(client_service.open_clients) == 0

        AppSettingsRepo().reset()

    def test_launching_a_chrome_client_and_killing_the_brower_process(self, database, cleanup_database, qtbot: QtBot):
        app_path = get_app_path()
        src_path = os.path.join(app_path, 'src')
        process_repo = ProcessRepo.get_instance()
        process_repo.set_app_path(str(src_path))

        # Set chrome browser to use our fake_browser executable
        app_settings = AppSettingsRepo().get()
        app_settings["browser_commands"]["chrome"] = "./test/fake_browser"
        AppSettingsRepo().save(app_settings)

        # Create the Client
        client_repo = ClientRepo()
        client = Client(title="test client", type="chrome", proxy_port=8080)
        client_repo.save(client)

        # Start the client
        client_service = OpenClientsService.get_instance()
        client_service.launch_client(client)
        time.sleep(1)

        assert client.browser is not None

        # Make the HTTP request, while waiting for the signals to be verified
        signals = [client_service.clients_changed]
        with qtbot.waitSignals(signals, timeout=2000):
            os.kill(client.browser.proc.pid, signal.SIGTERM)

        assert len(client_service.open_clients) == 0

        AppSettingsRepo().reset()
