from PySide2 import QtCore
import zmq

class ProxyEventsWorker(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @QtCore.Slot()
    def run(self):
        print('\n\nRpyc server starting..')
        port = "5556"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % port)

        print('ProxyEventsWorker loop starting...')
        while True:
            print('Running loop..')
            #  Wait for next request from client
            message = self.socket.recv()
            print("Received message: %s" % message)

        print('ProxyEventsWorker loop done.')

    def stop(self):
        print('ProxyEventsWorker stopping...')
        self.socket.close()
        self.context.term()

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
