import os
import signal
import subprocess
from typing import Callable
from PyQt6 import QtCore

class WorkerSignals(QtCore.QObject):
    exited = QtCore.pyqtSignal(object)

class BrowserProc(QtCore.QRunnable):
    process: subprocess.Popen

    def __init__(self, client, fn):
        super(BrowserProc, self).__init__()

        self.client = client
        self.fn = fn
        self.signals = WorkerSignals()

    def run(self):
        self.process: subprocess.Popen = self.fn()
        stdout, stderr = self.process.communicate(input=None, timeout=None)
        exit_code = self.process.wait()
        print(stdout, stderr, exit_code)
        if self.signals:
            # NOTE: if you close the app then self.signals will be garbage collected and this line will
            # throw an exception
            self.signals.exited.emit(self.client)

    def kill(self):
        os.kill(self.process.pid, signal.SIGTERM)
