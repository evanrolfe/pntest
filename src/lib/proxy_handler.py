from PySide2 import QtCore
import zmq
import simplejson as json
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from models.data.websocket_message import WebsocketMessage

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

    @QtCore.Slot()
    def run(self):
        print('\n\nRpyc server starting..')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind("tcp://*:%s" % PROXY_ZMQ_PORT)

        print('[ProxyZmqServer] loop starting...')
        while True:
            identity = self.socket.recv()
            message = self.socket.recv_string()
            print(f'[ProxyZmqServer] Received {message} from {identity}')
            self.handle_message(message)

    def stop(self):
        print('[ProxyZmqServer] stopping...')
        self.socket.close()
        self.context.term()

    def handle_message(self, message):
        obj = json.loads(message)
        if (obj['type'] == 'request'):
            self.request(obj)
        elif (obj['type'] == 'response'):
            self.response(obj)
        elif (obj['type'] == 'websocket_message'):
            self.websocket_message(obj)

    def request(self, request_state):
        http_request = HttpRequest.from_state(request_state)
        http_request.save()

        http_flow = HttpFlow()
        http_flow.uuid = request_state['flow_uuid']
        http_flow.client_id = request_state['client_id']
        http_flow.request_id = http_request.id
        http_flow.type = 'proxy'
        http_flow.save()

        self.signals.flow_created.emit(http_flow)

        if request_state['intercepted']:
            self.signals.flow_intercepted.emit(http_flow)

    def response(self, response_state):
        http_response = HttpResponse.from_state(response_state)
        http_response.save()

        http_flow = HttpFlow.where('uuid', '=', response_state['flow_uuid']).first()
        http_flow.response_id = http_response.id
        http_flow.save()

        self.signals.flow_updated.emit(http_flow)

    def websocket_message(self, message_state):
        http_flow = HttpFlow.where('uuid', '=', message_state['flow_uuid']).first()

        websocket_message = WebsocketMessage.from_state(message_state)
        websocket_message.http_flow_id = http_flow.id
        websocket_message.save()

        self.signals.websocket_message_created.emit(websocket_message)

    def forward_intercepted_flow(self, flow):
        print(f"[ProxyZmqServer] forwarding request on proxy {flow.client_id}")
        message = {'type': 'forward', 'flow_uuid': flow.uuid}
        self.socket.send_multipart([str(flow.client_id).encode(), json.dumps(message).encode()])

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

    def forward_intercepted_flow(self, client_id):
        self.zmq_server.forward_intercepted_flow(client_id)
