from PySide2 import QtCore, QtWidgets
import zmq
import sys
import simplejson as json
from typing import cast
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from models.data.websocket_message import WebsocketMessage
from proxy.common_types import SettingsJson

PROXY_ZMQ_PORT = 5556

class ProxySignals(QtCore.QObject):
    flow_created = QtCore.Signal(HttpFlow)
    flow_updated = QtCore.Signal(HttpFlow)
    websocket_message_created = QtCore.Signal(WebsocketMessage)
    flow_intercepted = QtCore.Signal(HttpFlow)

class ProxyZmqServer(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.signals = ProxySignals()
        self.client_ids = set()

    @QtCore.Slot()  # type: ignore
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
            sockets = dict(poll.poll(1000))

            # print(f'[ProxyZmqServer] polling client_ids {list(self.client_ids)}')
            for client_id in list(self.client_ids):
                message = {'type': 'poll'}
                self.socket.send_multipart([str(client_id).encode(), json.dumps(message).encode()])

            if sockets:
                try:
                    identity = self.socket.recv()
                    message = self.socket.recv_string()
                    # print(f'[ProxyZmqServer] Received {message} from {identity}')
                    self.client_ids.add(int(identity))
                    self.handle_message(message)
                except Exception:  # noqa
                    exctype, value = sys.exc_info()[:2]
                    # self.__show_error_box(f'{exctype}: {value}')
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

    def request(self, request_state):
        http_request = HttpRequest.from_state(request_state)
        http_request.save()

        http_flow = HttpFlow()
        http_flow.uuid = request_state['flow_uuid']
        http_flow.client_id = request_state['client_id']
        http_flow.request_id = http_request.id
        http_flow.type = HttpFlow.TYPE_PROXY
        http_flow.save()

        cast(QtCore.SignalInstance, self.signals.flow_created).emit(http_flow)

        if request_state['intercepted']:
            cast(QtCore.SignalInstance, self.signals.flow_intercepted).emit(http_flow)

    def response(self, response_state):
        http_response = HttpResponse.from_state(response_state)
        http_response.save()

        http_flow = HttpFlow.where('uuid', '=', response_state['flow_uuid']).first()
        if http_flow is None:
            return

        http_flow.response_id = http_response.id
        http_flow.save()

        cast(QtCore.SignalInstance, self.signals.flow_updated).emit(http_flow)

        if response_state['intercepted']:
            cast(QtCore.SignalInstance, self.signals.flow_intercepted).emit(http_flow)

    def websocket_message(self, message_state):
        http_flow = HttpFlow.where('uuid', '=', message_state['flow_uuid']).first()

        websocket_message = WebsocketMessage.from_state(message_state)
        websocket_message.http_flow_id = http_flow.id
        websocket_message.save()

        cast(QtCore.SignalInstance, self.signals.websocket_message_created).emit(websocket_message)

        if message_state['intercepted']:
            http_flow.intercept_websocket_message = True
            cast(QtCore.SignalInstance, self.signals.flow_intercepted).emit(http_flow)

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
        message_box.exec_()

        print(message)

class ProxyHandler():
    def __init__(self, parent=None):
        self.thread = QtCore.QThread(parent)
        self.zmq_server = ProxyZmqServer()
        self.zmq_server.moveToThread(self.thread)
        self.signals = self.zmq_server.signals
        self.thread.started.connect(self.zmq_server.run)  # type: ignore

    def start(self):
        self.thread.start()

    def stop(self):
        print("Stopping ProxyEventsWorker...")
        self.zmq_server.stop()
        self.thread.quit()
        self.thread.wait()  # type: ignore

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
