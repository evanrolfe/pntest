from PySide2 import QtCore
import zmq

class ProxyEventsWorker(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @QtCore.Slot()
    def run(self):
        print('\n\nRpyc server starting..')
        port = "5556"
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % port)
        self.run_loop = True

        print('ProxyEventsWorker loop starting...')
        while self.run_loop:
            print('Running loop..')
            #  Wait for next request from client
            message = self.socket.recv(flags=zmq.NOBLOCK)
            print("Received message: %s" % message)

        print('ProxyEventsWorker loop done.')

    def stop(self):
        print('ProxyEventsWorker stopping...')
        self.run_loop = False

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
        msg = socket.recv()
        print(msg)

    def stop(self):
        print("Stopping ProxyEventsWorker...")
        self.proxy_events.stop()
        self.thread.quit()
        self.thread.wait()
