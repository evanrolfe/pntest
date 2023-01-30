from __future__ import annotations
import json
import base64
import subprocess
import signal
import os
import sys
from typing import Optional, TypedDict
from PyQt6 import QtCore
from models.available_client import AvailableClient
from models.client import Client
from models.http_flow import HttpFlow
from models.project_settings import ProjectSettings
from models.websocket_message import WebsocketMessage
from lib.proxy_handler import ProxyHandler
from lib.paths import get_app_path
from lib.utils import is_dev_mode
from lib.browser_launcher.launch import launch_chrome_or_chromium, launch_firefox
from lib.browser_launcher.browser_proc import BrowserProc
from models.http_response import HttpResponse
from mitmproxy.common_types import ProxyRequest, ProxyResponse, ProxyWebsocketMessage
from repos.client_repo import ClientRepo
from repos.http_flow_repo import HttpFlowRepo
from repos.project_settings_repo import ProjectSettingsRepo

class RunningProcess(TypedDict):
    client: Client
    type: str
    process: Optional[subprocess.Popen[bytes]]
    worker: Optional[BrowserProc]

class ProcessManager(QtCore.QObject):
    proxy_request = QtCore.pyqtSignal(HttpFlow)
    proxy_response = QtCore.pyqtSignal(HttpFlow)
    proxy_ws_message = QtCore.pyqtSignal(WebsocketMessage)
    flow_intercepted = QtCore.pyqtSignal(HttpFlow)
    proxy_started = QtCore.pyqtSignal(int)

    clients_changed = QtCore.pyqtSignal()
    recording_changed = QtCore.pyqtSignal(bool)
    intercept_changed = QtCore.pyqtSignal(bool)

    app_path: str
    proxy_handler: ProxyHandler
    processes: list[RunningProcess]
    recording_enabled: bool
    intercept_enabled: bool

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance() -> ProcessManager:
        # Static access method.
        if ProcessManager.__instance is None:
            raise Exception("Calling ProcessManager.get_instance() when there is not instance!")
        return ProcessManager.__instance

    def __init__(self, app_path: str):
        super().__init__()
        self.init(app_path)

        # Virtually private constructor.
        if ProcessManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ProcessManager.__instance = self
    # /Singleton method stuff

    def init(self, app_path: str):
        self.app_path = app_path
        self.processes = []
        self.threadpool = QtCore.QThreadPool()

        self.proxy_handler = ProxyHandler(self)
        self.proxy_handler.start()

        self.proxy_handler.signals.proxy_request.connect(self.proxy_request_slot)
        self.proxy_handler.signals.proxy_response.connect(self.proxy_response_slot)
        self.proxy_handler.signals.proxy_ws_message.connect(self.proxy_ws_message_slot)
        self.proxy_handler.signals.proxy_started.connect(self.proxy_was_launched)

        self.recording_enabled = True
        self.intercept_enabled = False

    def get_open_clients(self) -> list[Client]:
        return [c['client'] for c in self.processes if c['type'] == 'proxy']

    def on_exit(self):
        print("[ProcessManager] killing all processes...")
        self.proxy_handler.stop()

        for running_process in self.processes:
            proc = running_process.get('process')
            if proc is not None:
                os.kill(proc.pid, signal.SIGTERM)

            worker = running_process.get('worker')
            if worker is not None:
                worker.kill()

    def close_proxy(self, client: Client):
        process = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'proxy'][0]
        if process['process'] is None:
            return
        pid = process['process'].pid
        print(f'[ProcessManager] killing process {pid}')
        os.kill(pid, signal.SIGTERM)
        self.processes.remove(process)
        self.clients_changed.emit()

    def close_browser(self, client: Client):
        process = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'browser'][0]
        if process['worker'] is None:
            return
        process['worker'].kill()
        self.processes.remove(process)

    # Close the proxy when the browser is closed
    def browser_was_closed(self, client: Client):
        print(f"[ProcessManager] browser {client.id} closed, closing proxy")
        self.close_proxy(client)

        browser_processes = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'browser']
        if len(browser_processes) == 0:
            return

        self.processes.remove(browser_processes[0])

        client.open = False
        ClientRepo().save(client)
        self.clients_changed.emit()

    def launch_client(self, client: Client, client_info: AvailableClient, settings: ProjectSettings):
        print(f"Launching client:")
        self.launch_proxy(client, settings)

        browser_command = client_info.command
        if browser_command:
            self.launch_browser(client, browser_command)

    def proxy_was_launched(self, client_id: int):
        self.set_settings(ProjectSettingsRepo().get())
        self.proxy_handler.set_recording_enabled(self.recording_enabled)
        self.proxy_handler.set_intercept_enabled(self.intercept_enabled)

        client = ClientRepo().find(client_id)
        if client is None:
            return

        client.open = True
        ClientRepo().save(client)
        self.clients_changed.emit()

    def close_client(self, client: Client):
        if client.type != 'anything':
            self.close_browser(client)
        else:
            self.close_proxy(client)

        client.open = False
        ClientRepo().save(client)

    def launch_browser(self, client: Client, browser_command: str):
        if client.type in ['chrome', 'chromium']:
            worker = BrowserProc(client, lambda: launch_chrome_or_chromium(client, browser_command))
        elif client.type == 'firefox':
            worker = BrowserProc(client, lambda: launch_firefox(client, browser_command))
        else:
            return

        worker.signals.exited.connect(self.browser_was_closed)
        self.threadpool.start(worker)
        self.processes.append({'client': client, 'type': 'browser', 'worker': worker, 'process': None})

    def launch_proxy(self, client: Client, settings: ProjectSettings):
        print(f"[ProcessManager] Launching proxy, app_path: {self.app_path}")

        recording_enabled = 1 if self.recording_enabled else 0
        intercept_enabled = 1 if self.intercept_enabled else 0
        args_str = f'{client.id} {recording_enabled} {intercept_enabled}'

        if is_dev_mode():
            proxy_command = f'mitmdump -s {self.app_path}/src/mitmproxy/addon.py -p {client.proxy_port} --set confdir=./include --set client_certs=./include/mitmproxy-client.pem {args_str}'
        else:
            proxy_command = f'{self.app_path}/mitmdump -s {self.app_path}/addon.py -p {client.proxy_port} --set confdir={self.app_path}/include --set client_certs={self.app_path}/include/mitmproxy-client.pem {args_str}'

        print(proxy_command)
        # To get logging from the proxy, add the stdout,stderr lines to Popen() args
        # file_out = open(f'{self.app_path}/log.txt','w')
        # stdout=file_out,
        # stderr=file_out
        current_env = os.environ.copy()
        process = subprocess.Popen(
            proxy_command.split(' '),
            preexec_fn=os.setsid,
            env=current_env,
        )
        self.processes.append({'client': client, 'type': 'proxy', 'process': process, 'worker': None})

    def forward_flow(self, flow: HttpFlow, intercept_response: bool):
        self.proxy_handler.forward_flow(flow, intercept_response)

    def forward_all(self):
        self.proxy_handler.forward_all()

    def drop_flow(self, flow: HttpFlow):
        self.proxy_handler.drop_flow(flow)

    def toggle_intercept_enabled(self):
        self.intercept_enabled = not self.intercept_enabled

        if self.intercept_enabled and not self.recording_enabled:
            self.toggle_recording_enabled()

        self.proxy_handler.set_intercept_enabled(self.intercept_enabled)
        self.intercept_changed.emit(self.intercept_enabled)

    def toggle_recording_enabled(self):
        self.recording_enabled = not self.recording_enabled

        if not self.recording_enabled and self.intercept_enabled:
            self.toggle_intercept_enabled()

        self.proxy_handler.set_recording_enabled(self.recording_enabled)
        self.recording_changed.emit(self.recording_enabled)

    def set_settings(self, settings: ProjectSettings) -> None:
        self.proxy_handler.set_settings(settings)

    def proxy_request_slot(self, proxy_request: ProxyRequest):
        flow = HttpFlow.from_proxy_request(proxy_request)
        HttpFlowRepo().save(flow)

        self.proxy_request.emit(flow)
        if proxy_request['intercepted']:
            self.flow_intercepted.emit(flow)

    def proxy_response_slot(self, proxy_response: ProxyResponse):
        flow = HttpFlowRepo().find_by_uuid(proxy_response['flow_uuid'])
        if flow is None:
            return
        response = HttpResponse.from_state(proxy_response)
        flow.add_response(response)
        HttpFlowRepo().save(flow)

        # So we dont use unecessary memory
        flow.clear_extra_data()

        self.proxy_response.emit(flow)
        if proxy_response['intercepted']:
            self.flow_intercepted.emit(flow)

    def proxy_ws_message_slot(self, proxy_ws_message: ProxyWebsocketMessage):
        flow = HttpFlowRepo().find_by_uuid(proxy_ws_message['flow_uuid'])
        if flow is None:
            return

        ws_message = WebsocketMessage.from_state(proxy_ws_message)
        flow.add_ws_message(ws_message)
        HttpFlowRepo().save(flow)

        self.proxy_ws_message.emit(ws_message)
        if proxy_ws_message['intercepted']:
            flow.intercept_websocket_message = True
            self.flow_intercepted.emit(flow)
