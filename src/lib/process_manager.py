from __future__ import annotations

import subprocess
import signal
import atexit
import os
import sys
from typing import cast
from PySide2 import QtCore
from models.data.http_flow import HttpFlow
from models.data.websocket_message import WebsocketMessage
from lib.proxy_handler import ProxyHandler
from lib.paths import get_app_path
from lib.utils import is_dev_mode
from lib.browser_launcher.launch import launch_chrome_or_chromium, launch_firefox
from lib.browser_launcher.browser_proc import BrowserProc
from common_types import SettingsJson

class ProcessManager(QtCore.QObject):
    clients_changed = QtCore.Signal()
    flow_created = QtCore.Signal(HttpFlow)
    flow_updated = QtCore.Signal(HttpFlow)
    flow_intercepted = QtCore.Signal(HttpFlow)
    websocket_message_created = QtCore.Signal(WebsocketMessage)

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
        cast(QtCore.SignalInstance, self.proxy_handler.signals.flow_created).connect(self.flow_created)
        cast(QtCore.SignalInstance, self.proxy_handler.signals.flow_updated).connect(self.flow_updated)
        cast(QtCore.SignalInstance, self.proxy_handler.signals.flow_intercepted).connect(self.flow_intercepted)
        cast(QtCore.SignalInstance, self.proxy_handler.signals.websocket_message_created).connect(self.websocket_message_created)

        atexit.register(self.on_exit)
        signal.signal(signal.SIGTERM, self.on_exit)  # type: ignore
        signal.signal(signal.SIGINT, self.on_exit)  # type: ignore

    def on_exit(self):
        print("[ProcessManager] killing all processes...")
        self.proxy_handler.stop()

        for process_dict in self.processes:
            if 'process' in process_dict:
                os.kill(process_dict['process'].pid, signal.SIGTERM)

            if 'worker' in process_dict:
                process_dict['worker'].kill()

    def close_proxy(self, client):
        process = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'proxy'][0]
        pid = process['process'].pid
        print(f'[ProcessManager] killing process {pid}')
        os.kill(pid, signal.SIGTERM)
        self.processes.remove(process)

    def close_browser(self, client):
        process = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'browser'][0]
        process['worker'].kill()
        self.processes.remove(process)

    @QtCore.Slot()  # type: ignore
    def browser_was_closed(self, client):
        print(f"[ProcessManager] browser {client.id} closed, closing proxy")
        browser_process = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'browser'][0]
        self.processes.remove(browser_process)

        self.close_proxy(client)
        client.open = False
        client.save()
        cast(QtCore.SignalInstance, self.clients_changed).emit()

    def launch_browser(self, client, browser_command):
        if client.type in ['chrome', 'chromium']:
            worker = BrowserProc(client, lambda: launch_chrome_or_chromium(client, browser_command))
        elif client.type == 'firefox':
            worker = BrowserProc(client, lambda: launch_firefox(client, browser_command))
        else:
            return

        cast(QtCore.SignalInstance, worker.signals.exited).connect(self.browser_was_closed)
        self.threadpool.start(worker)
        self.processes.append({'client': client, 'type': 'browser', 'worker': worker})

    def launch_proxy(self, client):
        app_path = str(get_app_path())
        print(f"[ProcessManager] Launching proxy, app_path: {app_path}")

        if is_dev_mode():
            proxy_command = f'{sys.executable} {app_path}/proxy {client.proxy_port} {client.id}'
        else:
            proxy_command = f'{app_path}/pntest_proxy {client.proxy_port} {client.id} {app_path}/include'
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

    def drop_flow(self, flow):
        self.proxy_handler.drop_flow(flow)

    def set_enabled(self, enabled):
        self.proxy_handler.set_enabled(enabled)

    def set_settings(self, settings: SettingsJson) -> None:
        self.proxy_handler.set_settings(settings)
