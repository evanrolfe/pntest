from __future__ import annotations
import json
import base64
import subprocess
import signal
import os
import sys
from PyQt6 import QtCore
from lib.browser_launcher.detect import Browser
from lib.database import Database
from models.data.client import Client
from models.data.http_flow import HttpFlow
from models.data.settings import Settings
from models.data.websocket_message import WebsocketMessage
from lib.proxy_handler import ProxyHandler
from lib.paths import get_app_path
from lib.utils import is_dev_mode
from lib.browser_launcher.launch import launch_chrome_or_chromium, launch_firefox
from lib.browser_launcher.browser_proc import BrowserProc
from proxy.common_types import SettingsJson

class ProcessManager(QtCore.QObject):
    clients_changed = QtCore.pyqtSignal()
    flow_created = QtCore.pyqtSignal(HttpFlow)
    flow_updated = QtCore.pyqtSignal(HttpFlow)
    flow_intercepted = QtCore.pyqtSignal(HttpFlow)
    websocket_message_created = QtCore.pyqtSignal(WebsocketMessage)
    proxy_started = QtCore.pyqtSignal(int)

    proxy_handler: ProxyHandler
    recording_enabled: bool

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance() -> ProcessManager:
        # Static access method.
        if ProcessManager.__instance is None:
            raise Exception("Calling ProcessManager.get_instance() when there is not instance!")
        return ProcessManager.__instance

    def __init__(self, src_path):
        super().__init__()
        self.init(src_path)

        # Virtually private constructor.
        if ProcessManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ProcessManager.__instance = self
    # /Singleton method stuff

    def init(self, src_path):
        self.src_path = src_path
        self.processes = []
        self.threadpool = QtCore.QThreadPool()

        self.proxy_handler = ProxyHandler(self)
        self.proxy_handler.start()
        self.set_settings(Settings.get().parsed())

        self.proxy_handler.signals.flow_created.connect(self.flow_created)
        self.proxy_handler.signals.flow_updated.connect(self.flow_updated)
        self.proxy_handler.signals.flow_intercepted.connect(self.flow_intercepted)
        self.proxy_handler.signals.websocket_message_created.connect(self.websocket_message_created)
        self.proxy_handler.signals.proxy_started.connect(self.proxy_started)
        self.proxy_handler.signals.proxy_started.connect(self.proxy_was_launched)

        self.recording_enabled = True

    def on_exit(self):
        print("[ProcessManager] killing all processes...")
        self.proxy_handler.stop()

        for process_dict in self.processes:
            if 'process' in process_dict:
                os.kill(process_dict['process'].pid, signal.SIGTERM)

            if 'worker' in process_dict:
                process_dict['worker'].kill()

    def close_proxy(self, client: Client):
        process = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'proxy'][0]
        pid = process['process'].pid
        print(f'[ProcessManager] killing process {pid}')
        os.kill(pid, signal.SIGTERM)
        self.processes.remove(process)

    def close_browser(self, client: Client):
        process = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'browser'][0]
        process['worker'].kill()
        self.processes.remove(process)

    # Close the proxy when the browser is closed
    def browser_was_closed(self, client: Client):
        print(f"[ProcessManager] browser {client.id} closed, closing proxy")
        self.close_proxy(client)

        browser_process = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'browser'][0]
        self.processes.remove(browser_process)

        database = Database.get_instance()
        database.db.table('clients').where('id', client.id).update(open=False)
        self.clients_changed.emit()

    def launch_client(self, client: Client, client_info: Browser, settings: SettingsJson):
        print(f"Launching client:")
        self.launch_proxy(client, settings)

        browser_command = client_info.get('command')
        if browser_command:
            self.launch_browser(client, browser_command)

    def proxy_was_launched(self, client_id: int):
        client = Client.find(client_id)
        if client is None:
            return

        database = Database.get_instance()
        database.db.table('clients').where('id', client.id).update(open=True)

        self.clients_changed.emit()

    def close_client(self, client: Client):
        if client.type != 'anything':
            self.close_browser(client)
        else:
            self.close_proxy(client)

        client.open = False
        client.save()

    def launch_browser(self, client: Client, browser_command):
        if client.type in ['chrome', 'chromium']:
            worker = BrowserProc(client, lambda: launch_chrome_or_chromium(client, browser_command))
        elif client.type == 'firefox':
            worker = BrowserProc(client, lambda: launch_firefox(client, browser_command))
        else:
            return

        worker.signals.exited.connect(self.browser_was_closed)
        self.threadpool.start(worker)
        self.processes.append({'client': client, 'type': 'browser', 'worker': worker})

    def launch_proxy(self, client: Client, settings: SettingsJson):
        app_path = str(get_app_path())
        print(f"[ProcessManager] Launching proxy, app_path: {app_path}")

        recording_enabled = 1 if self.recording_enabled else 0
        settings_json_b64 = base64.b64encode(bytes(json.dumps(settings), 'utf-8')).decode('utf-8')

        if is_dev_mode():
            proxy_command = f'{sys.executable} {app_path}/proxy {client.proxy_port} {client.id} _ {recording_enabled} {settings_json_b64}'
        else:
            proxy_command = f'{app_path}/pntest_proxy {client.proxy_port} {client.id} {app_path}/include {recording_enabled} {settings_json_b64}'
        print(proxy_command)
        current_env = os.environ.copy()
        process = subprocess.Popen(
            proxy_command.split(' '),
            preexec_fn=os.setsid,
            env=current_env
        )
        self.processes.append({'client': client, 'type': 'proxy', 'process': process})

    def forward_flow(self, flow, intercept_response):
        self.proxy_handler.forward_flow(flow, intercept_response)

    def forward_all(self):
        self.proxy_handler.forward_all()

    def drop_flow(self, flow: HttpFlow):
        self.proxy_handler.drop_flow(flow)

    def set_enabled(self, enabled: bool):
        self.proxy_handler.set_enabled(enabled)

    def toggle_recording_enabled(self):
        self.recording_enabled = not self.recording_enabled
        self.proxy_handler.set_recording_enabled(self.recording_enabled)

    def set_settings(self, settings: SettingsJson) -> None:
        self.proxy_handler.set_settings(settings)
