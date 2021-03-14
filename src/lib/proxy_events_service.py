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
        self.server = ThreadedServer(self.service, port=18861, protocol_config={'allow_public_attrs': True})
        self.server.start()

    def stop(self):
        self.server.close()

class ProxyEventsManager():
    def __init__(self, parent=None):
        self.thread = QtCore.QThread(parent)
        self.proxy_events = ProxyEventsWorker()
        self.proxy_events.moveToThread(self.thread)
        self.thread.started.connect(self.proxy_events.run)

    def start(self):
        self.thread.start()

    def stop(self):
        print("Stopping ProxyEventsWorker...")
        self.proxy_events.stop()
        self.thread.quit()
        self.thread.wait()
