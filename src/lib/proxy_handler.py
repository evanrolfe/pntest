from typing import ByteString
from PyQt6 import QtCore, QtWidgets
import zmq
import sys
import simplejson as json
from models.data.http_flow import HttpFlow
from models.data.websocket_message import WebsocketMessage
from proxy.common_types import SettingsJson, ProxyRequest, ProxyResponse, ProxyWebsocketMessage

PROXY_ZMQ_PORT = 5556

class ProxySignals(QtCore.QObject):
    flow_created = QtCore.pyqtSignal(HttpFlow)
    flow_updated = QtCore.pyqtSignal(HttpFlow)
    websocket_message_created = QtCore.pyqtSignal(WebsocketMessage)
    flow_intercepted = QtCore.pyqtSignal(HttpFlow)

class ProxyZmqServer(QtCore.QObject):
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

        print('[ProxyZmqServer] starting...')
        self.should_continue = True
        while self.should_continue:
            try:
                sockets = dict(poll.poll(1000))
            except zmq.error.ZMQError:
                # TODO: Figure out why this error is raise from here on exit:
                # zmq.error.ZMQError: Socket operation on non-socket
                print('[ProxyZmqServer] error')
                return

            # print(f'[ProxyZmqServer] polling client_ids {list(self.client_ids)}')
            for client_id in list(self.client_ids):
                message = {'type': 'poll'}
                self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

            if sockets:
                try:
                    identity = self.socket.recv()
                    message = self.socket.recv_string()

                    # ZMQ typing is not accurate here
                    if type(identity) is not bytes:
                        raise Exception(f'Could not parse identity of type: {type(identity)}')

                    identity_str = identity.decode('utf-8')

                    self.client_ids.add(int(identity_str))
                    self.handle_message(message)
                except Exception:  # noqa
                    exctype, value = sys.exc_info()[:2]
                    print(f'{exctype}: {value}')
                    pass

    def stop(self):
        print('[ProxyZmqServer] stopping...')
        self.should_continue = False
        self.socket.close()
        self.context.term()

    def handle_message(self, message):
        obj = json.loads(message)
        if (obj['type'] == 'request'):
            print(f'[ProxyZmqServer] Received http request')
            self.request(obj)
        elif (obj['type'] == 'response'):
            print(f'[ProxyZmqServer] Received http response')
            self.response(obj)
        elif (obj['type'] == 'websocket_message'):
            print(f'[ProxyZmqServer] Received websocket message')
            self.websocket_message(obj)

    def request(self, request_state: ProxyRequest):
        http_flow = HttpFlow.create_from_proxy_request(request_state)

        self.signals.flow_created.emit(http_flow)

        if request_state['intercepted']:
            self.signals.flow_intercepted.emit(http_flow)

    def response(self, response_state: ProxyResponse):
        http_flow = HttpFlow.update_from_proxy_response(response_state)

        if not http_flow:
            return

        self.signals.flow_updated.emit(http_flow)

        if response_state['intercepted']:
            self.signals.flow_intercepted.emit(http_flow)

    def websocket_message(self, message_state: ProxyWebsocketMessage):
        http_flow, websocket_message = HttpFlow.create_from_proxy_websocket_message(message_state)

        self.signals.websocket_message_created.emit(websocket_message)

        if message_state['intercepted']:
            http_flow.intercept_websocket_message = True
            self.signals.flow_intercepted.emit(http_flow)

    def forward_flow(self, flow, intercept_response):
        if intercept_response:
            type = 'forward_and_intercept'
        else:
            type = 'forward'

        message = {'type': type, 'flow': flow.serialize()}
        self.socket.send_multipart([str(flow.client_id).encode(), json.dumps(message).encode()])

    def forward_all(self):
        message = {'type': 'forward_all'}
        for client_id in list(self.client_ids):
            self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

    def drop_flow(self, flow):
        message = {'type': 'drop', 'flow': flow.serialize()}
        self.socket.send_multipart([str(flow.client_id).encode(), json.dumps(message).encode()])

    def set_enabled(self, enabled):
        message = {'type': 'enable_intercept', 'value': enabled}
        for client_id in list(self.client_ids):
            self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

    def set_settings(self, settings: SettingsJson) -> None:
        message = {'type': 'set_settings', 'value': settings}
        for client_id in list(self.client_ids):
            self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

    def __show_error_box(self, message):
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('ProxyZmqServer: Error')
        message_box.setText(message)
        message_box.exec()

        print(message)

class ProxyHandler():
    def __init__(self, parent=None):
        self.thread = QtCore.QThread(parent)
        self.zmq_server = ProxyZmqServer()
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

    def forward_flow(self, flow, intercept_response):
        self.zmq_server.forward_flow(flow, intercept_response)

    def forward_all(self):
        self.zmq_server.forward_all()

    def drop_flow(self, flow):
        self.zmq_server.drop_flow(flow)

    def set_enabled(self, enabled):
        self.zmq_server.set_enabled(enabled)

    def set_settings(self, settings: SettingsJson) -> None:
        self.zmq_server.set_settings(settings)
