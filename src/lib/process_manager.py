import subprocess
import signal
import atexit
import os
import sys
from PySide2 import QtCore
from models.data.http_flow import HttpFlow
from models.data.websocket_message import WebsocketMessage
from lib.proxy_events_manager import ProxyEventsManager

CHROMIUM_COMMAND = 'chromium-browser --no-sandbox --noerrdialogs --user-data-dir=/home/evan/Code/pntest/include/chromium-profile' # noqa
PROXY_COMMAND = f'{sys.executable} /home/evan/Code/pntest/src/proxy'

class ProcessManager(QtCore.QObject):
    flow_created = QtCore.Signal(HttpFlow)
    flow_updated = QtCore.Signal(HttpFlow)
    websocket_message_created = QtCore.Signal(WebsocketMessage)

    def __init__(self):
        super().__init__()

        self.processes = []

        atexit.register(self.on_exit)
        signal.signal(signal.SIGTERM, self.on_exit)
        signal.signal(signal.SIGINT, self.on_exit)

    def on_exit(self):
        print("ProcessManager closing all processes...")
        self.proxy_events_manager.stop()

        for process in self.processes:
            os.kill(process.pid, signal.SIGTERM)

    def launch_browser(self):
        process = subprocess.Popen(
            CHROMIUM_COMMAND.split(' '),
            preexec_fn=os.setsid
        )
        self.processes.append(process)

    # TODO: Make the proxy/__main__ accept a port number (and also ProxyEventsManager),
    #       does it need a differt port actually? (server/client)
    # TODO: allow to launch multiple proxies on different ports
    def launch_proxy(self, listen_port):
        process = subprocess.Popen(
            PROXY_COMMAND.split(' '),
            preexec_fn=os.setsid
        )
        self.processes.append(process)

        self.proxy_events_manager = ProxyEventsManager(self)
        self.proxy_events_manager.start()

        self.proxy_events_manager.signals.flow_created.connect(self.flow_created)
        self.proxy_events_manager.signals.flow_updated.connect(self.flow_updated)
        self.proxy_events_manager.signals.websocket_message_created.connect(self.websocket_message_created)
