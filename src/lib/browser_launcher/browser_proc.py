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

        # TODO: Figure out how to prevent this error. It is thrown sometimes when you have a browser open
        # but close PnTest without closing the browser first.
        # See: http://enki-editor.org/2014/08/23/Pyqt_mem_mgmt.html
        try:
            self.signals.exited.emit(self.client)
        except RuntimeError as err:
            print("RuntimeError: ", err)

    def kill(self):
        os.kill(self.process.pid, signal.SIGTERM)
