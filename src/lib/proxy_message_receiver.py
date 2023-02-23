from __future__ import annotations
import json
import base64
import subprocess
import signal
import os
import sys
from typing import Optional, TypedDict
from PyQt6 import QtCore
from entities.available_client import AvailableClient
from entities.client import Client
from entities.http_flow import HttpFlow
from entities.project_settings import ProjectSettings
from entities.websocket_message import WebsocketMessage
from lib.proxy_zmq_server import ProxyZmqServer
from entities.http_response import HttpResponse
from mitmproxy.common_types import ProxyRequest, ProxyResponse, ProxyWebsocketMessage
from repos.client_repo import ClientRepo
from services.http_flow_service import HttpFlowService
from repos.project_settings_repo import ProjectSettingsRepo

class ProxyMessageReceiver(QtCore.QObject):
    proxy_request = QtCore.pyqtSignal(HttpFlow)
    proxy_response = QtCore.pyqtSignal(HttpFlow)
    proxy_ws_message = QtCore.pyqtSignal(WebsocketMessage)
    flow_intercepted = QtCore.pyqtSignal(HttpFlow)
    proxy_started = QtCore.pyqtSignal(int)

    clients_changed = QtCore.pyqtSignal()

    proxy_handler: ProxyZmqServer

    def __init__(self, proxy_zmq_server: ProxyZmqServer):
        super().__init__()

        self.proxy_zmq_server = proxy_zmq_server
        self.proxy_zmq_server.signals.proxy_request.connect(self.proxy_request_slot)
        self.proxy_zmq_server.signals.proxy_response.connect(self.proxy_response_slot)
        self.proxy_zmq_server.signals.proxy_ws_message.connect(self.proxy_ws_message_slot)
        self.proxy_zmq_server.signals.proxy_started.connect(self.proxy_was_launched)

        self.recording_enabled = True
        self.intercept_enabled = False

    def on_exit(self):
        print("[ProxyMessageReceiver] killing all proxy handler...")
        self.proxy_zmq_server.stop()

    def proxy_was_launched(self, client_id: int):
        self.set_settings(ProjectSettingsRepo().get())
        self.proxy_zmq_server.set_recording_enabled(self.recording_enabled)
        self.proxy_zmq_server.set_intercept_enabled(self.intercept_enabled)

        client = ClientRepo().find(client_id)
        if client is None:
            return

        client.open = True
        ClientRepo().save(client)
        self.clients_changed.emit()

    def set_settings(self, settings: ProjectSettings) -> None:
        self.proxy_zmq_server.set_settings(settings)

    def proxy_request_slot(self, proxy_request: ProxyRequest):
        flow = HttpFlow.from_proxy_request(proxy_request)
        HttpFlowService().save(flow)

        self.proxy_request.emit(flow)
        if proxy_request['intercepted']:
            self.flow_intercepted.emit(flow)

    def proxy_response_slot(self, proxy_response: ProxyResponse):
        flow = HttpFlowService().find_by_uuid(proxy_response['flow_uuid'])
        if flow is None:
            return
        response = HttpResponse.from_state(proxy_response)
        flow.add_response(response)
        HttpFlowService().save(flow)

        # So we dont use unecessary memory
        flow.clear_extra_data()

        self.proxy_response.emit(flow)
        if proxy_response['intercepted']:
            self.flow_intercepted.emit(flow)

    def proxy_ws_message_slot(self, proxy_ws_message: ProxyWebsocketMessage):
        flow = HttpFlowService().find_by_uuid(proxy_ws_message['flow_uuid'])
        if flow is None:
            return

        ws_message = WebsocketMessage.from_state(proxy_ws_message)
        flow.add_ws_message(ws_message)
        HttpFlowService().save(flow)

        self.proxy_ws_message.emit(ws_message)
        if proxy_ws_message['intercepted']:
            flow.intercept_websocket_message = True
            self.flow_intercepted.emit(flow)
