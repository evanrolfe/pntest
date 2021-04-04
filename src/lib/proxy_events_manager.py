from PySide2 import QtCore
import zmq
import simplejson as json
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse

class ProxyEventsWorker(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @QtCore.Slot()
    def run(self):
        print('\n\nRpyc server starting..')
        port = "5556"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % port)

        print('ProxyEventsWorker loop starting...')
        while True:
            message = self.socket.recv_string()
            self.handle_message(message)
            self.socket.send_string(json.dumps({'message': 'ok'}))

    def stop(self):
        print('ProxyEventsWorker stopping...')
        self.socket.close()
        self.context.term()

    def handle_message(self, message):
        obj = json.loads(message)
        if (obj['type'] == 'request'):
            self.request_intercepted(obj)
        elif (obj['type'] == 'response'):
            self.response_intercepted(obj)

    def request_intercepted(self, request_state):
        http_request = HttpRequest.from_state(request_state)
        http_request.save()

        http_flow = HttpFlow()
        http_flow.uuid = request_state['flow_uuid']
        http_flow.request_id = http_request.id
        http_flow.type = 'proxy'
        http_flow.save()

    def response_intercepted(self, response_state):
        http_response = HttpResponse.from_state(response_state)
        http_response.save()

        http_flow = HttpFlow.where('uuid', '=', response_state['flow_uuid']).first()
        http_flow.response_id = http_response.id
        http_flow.save()

class ProxyEventsManager():
    def __init__(self, parent=None):
        self.thread = QtCore.QThread(parent)
        self.proxy_events = ProxyEventsWorker()
        self.proxy_events.moveToThread(self.thread)
        self.thread.started.connect(self.proxy_events.run)

    def start(self):
        self.thread.start()

    def resume_request(self):
        socket = self.proxy_events.socket

        print('sending resume message')
        socket.send_string("resume")

    def stop(self):
        print("Stopping ProxyEventsWorker...")
        self.proxy_events.stop()
        self.thread.quit()
        self.thread.wait()
