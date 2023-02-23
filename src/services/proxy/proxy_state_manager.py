from PyQt6 import QtCore

from services.proxy.proxy_zmq_server import ProxyZmqServer

# ProxyStateManager keeps track of the state of all the proxies. Mainly around whether or not network
# recording or intercept is enabled/disabled.
class ProxyStateManager(QtCore.QObject):
    proxy_zmq_server: ProxyZmqServer
    recording_enabled: bool
    intercept_enabled: bool

    recording_changed = QtCore.pyqtSignal(bool)
    intercept_changed = QtCore.pyqtSignal(bool)

    def __init__(self, proxy_zmq_server: ProxyZmqServer):
        super().__init__()

        self.proxy_zmq_server = proxy_zmq_server
        self.recording_enabled = True
        self.intercept_enabled = False

    def toggle_intercept_enabled(self):
        self.intercept_enabled = not self.intercept_enabled

        if self.intercept_enabled and not self.recording_enabled:
            self.toggle_recording_enabled()

        self.proxy_zmq_server.set_intercept_enabled(self.intercept_enabled)
        self.intercept_changed.emit(self.intercept_enabled)

    def toggle_recording_enabled(self):
        self.recording_enabled = not self.recording_enabled

        if not self.recording_enabled and self.intercept_enabled:
            self.toggle_intercept_enabled()

        self.proxy_zmq_server.set_recording_enabled(self.recording_enabled)
        self.recording_changed.emit(self.recording_enabled)
