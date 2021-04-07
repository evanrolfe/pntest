import subprocess
import signal
import atexit
import os
import sys
from PySide2 import QtCore
from models.data.http_flow import HttpFlow
from models.data.websocket_message import WebsocketMessage
from lib.proxy_handler import ProxyHandler

CHROMIUM_COMMAND = 'chromium-browser --no-sandbox --noerrdialogs --user-data-dir=/home/evan/Code/pntest/include/chromium-profile' # noqa
PROXY_COMMAND = f'{sys.executable} /home/evan/Code/pntest/src/proxy'

class ProcessManager(QtCore.QObject):
    flow_created = QtCore.Signal(HttpFlow)
    flow_updated = QtCore.Signal(HttpFlow)
    flow_intercepted = QtCore.Signal(HttpFlow)
    websocket_message_created = QtCore.Signal(WebsocketMessage)

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance():
        # Static access method.
        if ProcessManager.__instance is None:
            ProcessManager()
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

        self.proxy_handler = ProxyHandler(self)
        self.proxy_handler.start()
        self.proxy_handler.signals.flow_created.connect(self.flow_created)
        self.proxy_handler.signals.flow_updated.connect(self.flow_updated)
        self.proxy_handler.signals.flow_intercepted.connect(self.flow_intercepted)
        self.proxy_handler.signals.websocket_message_created.connect(self.websocket_message_created)

        atexit.register(self.on_exit)
        signal.signal(signal.SIGTERM, self.on_exit)
        signal.signal(signal.SIGINT, self.on_exit)

    def on_exit(self):
        print("[ProcessManager] killing all processes...")
        self.proxy_handler.stop()

        for process_dict in self.processes:
            os.kill(process_dict['process'].pid, signal.SIGTERM)

    def close_proxy(self, client):
        process = [p for p in self.processes if p['client'].id == client.id and p['type'] == 'proxy'][0]
        pid = process['process'].pid
        print(f'[ProcessManager] killing process {pid}')
        os.kill(pid, signal.SIGTERM)
        self.processes.remove(process)

    def launch_browser(self, client):
        process = subprocess.Popen(
            CHROMIUM_COMMAND.split(' '),
            preexec_fn=os.setsid
        )
        self.processes.append({'client': client, 'type': 'browser', 'process': process})

    def launch_proxy(self, client):
        proxy_command = f'{sys.executable} {self.src_path}/proxy {client.proxy_port} {client.id}'

        process = subprocess.Popen(
            proxy_command.split(' '),
            preexec_fn=os.setsid
        )
        self.processes.append({'client': client, 'type': 'proxy', 'process': process})

    def forward_flow(self, flow, intercept_response):
        self.proxy_handler.forward_flow(flow, intercept_response)

    def forward_all(self, client_ids):
        self.proxy_handler.forward_all(client_ids)

    def drop_flow(self, flow):
        self.proxy_handler.drop_flow(flow)
