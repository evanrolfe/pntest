import rpyc
from rpyc.utils.server import ThreadedServer
from PySide2 import QtCore

class ProxyEventsSignals(QtCore.QObject):
    request = QtCore.Signal(str)
    response = QtCore.Signal(str)

    def emit_request(self, flow_json):
        print('emitting request')
        self.request.emit(flow_json)

    def emit_response(self, flow_json):
        print(f'emitting response')
        self.response.emit(flow_json)

class ProxyEventsService(rpyc.Service):
    def __init__(self):
        super().__init__()
        self.signals = ProxyEventsSignals()

    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

class ProxyEventsWorker(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.service = ProxyEventsService()

    @QtCore.Slot()
    def run(self):
        print('\n\nRpyc server starting..')
        server = ThreadedServer(self.service, port=18861, protocol_config={'allow_public_attrs': True})
        server.start()

