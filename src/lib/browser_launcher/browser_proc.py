import os
import signal
from typing import cast
from PySide2 import QtCore

class WorkerSignals(QtCore.QObject):
    exited = QtCore.Signal(object)

class BrowserProc(QtCore.QRunnable):
    def __init__(self, client, fn):
        super(BrowserProc, self).__init__()

        self.client = client
        self.fn = fn
        self.signals = WorkerSignals()

    @QtCore.Slot()  # type: ignore
    def run(self):
        self.process = self.fn()
        stdout, stderr = self.process.communicate()
        exit_code = self.process.wait()

        print(stdout, stderr, exit_code)
        cast(QtCore.SignalInstance, self.signals.exited).emit(self.client)

    def kill(self):
        os.kill(self.process.pid, signal.SIGTERM)
