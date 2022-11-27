from typing import ByteString, cast
from PyQt6 import QtCore, QtWidgets
import zmq
import sys
import simplejson as json
from repos.http_flow_repo import HttpFlowRepo
from models.http_flow import HttpFlow
from proxy.common_types import SettingsJson, ProxyRequest, ProxyResponse, ProxyWebsocketMessage

PROXY_ZMQ_PORT = 5556

class ProxySignals(QtCore.QObject):
    proxy_request = QtCore.pyqtSignal(object) # NOTE: Needs to be object even though its actually ProxyRequest
    proxy_response = QtCore.pyqtSignal(object) # NOTE: Needs to be object even though its actually ProxyResponse
    proxy_ws_message = QtCore.pyqtSignal(object) # NOTE: ^^
    proxy_started = QtCore.pyqtSignal(int)

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
                    pass

    def stop(self):
        print('[ProxyZmqServer] stopping...')
        self.should_continue = False
        self.socket.close()
        self.context.term()

    def handle_message(self, message, id: int):
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
        self.socket.send_multipart([str(flow.client_id).encode(), json.dumps(message).encode()])

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

    def forward_flow(self, flow: HttpFlow, intercept_response):
        self.zmq_server.forward_flow(flow, intercept_response)

    def forward_all(self):
        self.zmq_server.forward_all()

    def drop_flow(self, flow: HttpFlow):
        self.zmq_server.drop_flow(flow)

    def set_intercept_enabled(self, enabled: bool):
        self.zmq_server.set_intercept_enabled(enabled)

    def set_recording_enabled(self, enabled: bool):
        self.zmq_server.set_recording_enabled(enabled)

    def set_settings(self, settings: SettingsJson) -> None:
        self.zmq_server.set_settings(settings)
