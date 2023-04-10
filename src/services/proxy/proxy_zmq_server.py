from __future__ import annotations

import sys

import simplejson as json
import zmq
from PyQt6 import QtCore, QtWidgets

from entities.http_flow import HttpFlow
from entities.project_settings import ProjectSettings
from mitmproxy.common_types import (ProxyRequest, ProxyResponse,
                                    ProxyWebsocketMessage)

PROXY_ZMQ_PORT = 5556

# ProxyZmqServer is a wrapper for ProxyZmqServerThread and runs ProxyZmqServerThread in a thread.
# All outside code should call ProxyZmqServer and not ProxyZmqServerThread.
# It can send message to proxies and also receives messages from them too.
# There is one ProxyServerServer and there can be multiple (or zero) proxies running.
class ProxyZmqServer():
    def __init__(self):
        self.thread = QtCore.QThread()
        self.zmq_server = ProxyZmqServerThread()
        self.zmq_server.moveToThread(self.thread)
        self.signals = self.zmq_server.signals
        self.thread.started.connect(self.zmq_server.run)

    def start(self):
        self.thread.start()

    def stop(self):
        print("Stopping ProxyEventsWorker...")
        self.zmq_server.stop()
        self.thread.quit()
        self.thread.wait()

    def forward_flow(self, flow: HttpFlow, intercept_response: bool):
        self.zmq_server.forward_flow(flow, intercept_response)

    def forward_all(self):
        self.zmq_server.forward_all()

    def drop_flow(self, flow: HttpFlow):
        self.zmq_server.drop_flow(flow)

    def set_intercept_enabled(self, enabled: bool):
        self.zmq_server.set_intercept_enabled(enabled)

    def set_recording_enabled(self, enabled: bool):
        self.zmq_server.set_recording_enabled(enabled)

    def set_settings(self, settings: ProjectSettings) -> None:
        self.zmq_server.set_settings(settings)

class ProxySignals(QtCore.QObject):
    proxy_request = QtCore.pyqtSignal(object) # NOTE: Needs to be object even though its actually ProxyRequest
    proxy_response = QtCore.pyqtSignal(object) # NOTE: Needs to be object even though its actually ProxyResponse
    proxy_ws_message = QtCore.pyqtSignal(object) # NOTE: ^^
    proxy_started = QtCore.pyqtSignal(int)

class ProxyZmqServerThread(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.signals = ProxySignals()
        self.client_ids = set()

    def run(self):
        print('\n\nRpyc server starting..')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind("tcp://*:%s" % PROXY_ZMQ_PORT)

        poll = zmq.Poller()
        poll.register(self.socket, zmq.POLLIN)

        print('[ProxyZmqServerThread] starting...')
        self.should_continue = True
        while self.should_continue:
            try:
                sockets = dict(poll.poll(1000))
            except zmq.error.ZMQError:
                # TODO: Figure out why this error is raise from here on exit:
                # zmq.error.ZMQError: Socket operation on non-socket
                print('[ProxyZmqServerThread] error')
                return

            # print(f'[ProxyZmqServerThread] polling client_ids {list(self.client_ids)}')
            for client_id in list(self.client_ids):
                message = {'type': 'poll'}
                self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

            if sockets:
                try:
                    identity = self.socket.recv()
                    message = self.socket.recv()

                    # ZMQ typing is not accurate here
                    if type(identity) is not bytes:
                        raise Exception(f'Could not parse identity of type: {type(identity)}')

                    identity_str = identity.decode('utf-8')

                    self.client_ids.add(int(identity_str))
                    self.handle_message(message, int(identity_str))
                except Exception:  # noqa
                    exctype, value = sys.exc_info()[:2]
                    print(f'{exctype}: {value}')

    def stop(self):
        print('[ProxyZmqServerThread] stopping...')
        self.should_continue = False
        self.socket.close()
        self.context.term()

    def handle_message(self, message, id: int):
        obj = json.loads(message)
        if (obj['type'] == 'request'):
            print(f'[ProxyZmqServerThread] Received http request')
            self.request(obj)
        elif (obj['type'] == 'response'):
            print(f'[ProxyZmqServerThread] Received http response')
            # Decode the hex string
            obj['content'] = bytes.fromhex(obj['content'])
            self.response(obj)
        elif (obj['type'] == 'websocket_message'):
            print(f'[ProxyZmqServerThread] Received websocket message')
            self.websocket_message(obj)
        elif (obj['type'] == 'started'):
            self.signals.proxy_started.emit(id)

    def request(self, proxy_request: ProxyRequest):
        self.signals.proxy_request.emit(proxy_request)

    def response(self, response_state: ProxyResponse):
        self.signals.proxy_response.emit(response_state)

    def websocket_message(self, message_state: ProxyWebsocketMessage):
        self.signals.proxy_ws_message.emit(message_state)

    def forward_flow(self, flow: HttpFlow, intercept_response: bool):
        if intercept_response:
            type = 'forward_and_intercept'
        else:
            type = 'forward'

        message = {'type': type, 'flow': flow.serialize()}
        self.socket.send_multipart([str(flow.source_id).encode(), json.dumps(message).encode()])

    def forward_all(self):
        message = {'type': 'forward_all'}
        for client_id in list(self.client_ids):
            self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

    def drop_flow(self, flow):
        message = {'type': 'drop', 'flow': flow.serialize()}
        self.socket.send_multipart([str(flow.client_id).encode(), json.dumps(message).encode()])

    def set_intercept_enabled(self, enabled):
        message = {'type': 'enable_intercept', 'value': enabled}
        for client_id in list(self.client_ids):
            self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

    def set_recording_enabled(self, enabled: bool):
        message = {'type': 'enable_recording', 'value': enabled}
        for client_id in list(self.client_ids):
            self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

    def set_settings(self, settings: ProjectSettings) -> None:
        message = {'type': 'set_settings', 'value': settings}
        for client_id in list(self.client_ids):
            self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

    def __show_error_box(self, message):
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('ProxyZmqServerThread: Error')
        message_box.setText(message)
        message_box.exec()

        print(message)
