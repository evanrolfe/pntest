from __future__ import annotations
import os
import signal
import subprocess
from typing import Generic, Optional, Type, TypeVar
from models.app_settings import AppSettings
from models.available_client import AvailableClient
from models.client import Client
from models.process import Process
from models.project_settings import ProjectSettings
from lib.utils import is_dev_mode

# TODO: This should be imported from teh file that defines the zmq server
ZMQ_SERVER_ADDR = "localhost:5556"

class ProcessRepo():
    procs: list[Process]
    app_path: str

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance() -> ProcessRepo:
        # Static access method.
        if ProcessRepo.__instance is None:
            ProcessRepo()

        return ProcessRepo.__instance # type:ignore

    def __init__(self):
        super().__init__()

        self.procs = []

        # Virtually private constructor.
        if ProcessRepo.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ProcessRepo.__instance = self
    # /Singleton method stuff

    def set_app_path(self, app_path: str):
        self.app_path = app_path

    def launch_proxy(self, client: Client) -> Process:
        print(f"[ProcessManager] Launching proxy, app_path: {self.app_path}")

        recording_enabled = 1 # if self.recording_enabled else 0
        intercept_enabled = 1 # if self.intercept_enabled else 0
        args_str = f'--client-id {client.id} --zmq-server {ZMQ_SERVER_ADDR}'

        if is_dev_mode():
            proxy_command = f'mitmdump -s {self.app_path}/src/mitmproxy/addon.py -p {client.proxy_port} --set confdir=./include --set client_certs=./include/mitmproxy-client.pem - {args_str}'
        else:
            proxy_command = f'{self.app_path}/mitmdump -s {self.app_path}/addon.py -p {client.proxy_port} --set confdir={self.app_path}/include --set client_certs={self.app_path}/include/mitmproxy-client.pem - {args_str}'

        print(proxy_command)
        # To get logging from the proxy, add the stdout,stderr lines to Popen() args
        # file_out = open(f'{self.app_path}/log.txt','w')
        # stdout=file_out,
        # stderr=file_out
        current_env = os.environ.copy()
        proc = subprocess.Popen(
            proxy_command.split(' '),
            preexec_fn=os.setsid,
            env=current_env,
        )
        process = Process(type='proxy', proc=proc)
        self.procs.append(process)
        return process

    def close_proxy(self, process: Process):
        pid = process.proc.pid

        print(f'[ProcessRepo] killing process {pid}')
        os.kill(pid, signal.SIGTERM)
        self.procs.remove(process)

        # self.clients_changed.emit()
