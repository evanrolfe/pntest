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
from models.http_response import HttpResponse
from mitmproxy.common_types import ProxyRequest, ProxyResponse, ProxyWebsocketMessage
from repos.client_repo import ClientRepo
from repos.http_flow_repo import HttpFlowRepo
from repos.project_settings_repo import ProjectSettingsRepo

# TODO: This should go in a service class
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

    def __init__(self):
        super().__init__()
        self.init()

        # Virtually private constructor.
        if ProcessManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ProcessManager.__instance = self
    # /Singleton method stuff

    def init(self):
        self.proxy_handler = ProxyHandler(self)
        self.proxy_handler.start()

        self.proxy_handler.signals.proxy_request.connect(self.proxy_request_slot)
        self.proxy_handler.signals.proxy_response.connect(self.proxy_response_slot)
        self.proxy_handler.signals.proxy_ws_message.connect(self.proxy_ws_message_slot)
        self.proxy_handler.signals.proxy_started.connect(self.proxy_was_launched)

        self.recording_enabled = True
        self.intercept_enabled = False

    def on_exit(self):
        print("[ProcessManager] killing all proxy handler...")
        self.proxy_handler.stop()

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
