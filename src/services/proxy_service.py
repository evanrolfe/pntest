from __future__ import annotations
from PyQt6 import QtCore
from lib.proxy_message_receiver import ProxyMessageReceiver

from lib.proxy_zmq_server import ProxyZmqServer
from services.proxy_state_manager import ProxyStateManager

class ProxyService(QtCore.QObject):
    process_manager: ProxyMessageReceiver
    proxy_state_manager: ProxyStateManager

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance() -> ProxyService:
        # Static access method.
        if ProxyService.__instance is None:
            raise Exception("Calling ProxyService.get_instance() when there is not instance!")
        return ProxyService.__instance

    def __init__(self):
        super().__init__()

        self.proxy_zmq_server = ProxyZmqServer()
        self.proxy_zmq_server.start()

        self.process_manager = ProxyMessageReceiver(self.proxy_zmq_server)
        self.proxy_state_manager = ProxyStateManager(self.proxy_zmq_server)

        # Virtually private constructor.
        if ProxyService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ProxyService.__instance = self
    # /Singleton method stuff

