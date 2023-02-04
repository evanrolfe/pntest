from dataclasses import dataclass
from dataclasses import field
import os
import signal
import subprocess
from typing import Optional
from PyQt6 import QtCore

class WorkerSignals(QtCore.QObject):
    exited = QtCore.pyqtSignal(object)

class Browser(QtCore.QRunnable):
    proc: subprocess.Popen
    type: str

    def __init__(self, fn):
        super(Browser, self).__init__()

        self.fn = fn
        self.signals = WorkerSignals()

    def run(self):
        self.proc: subprocess.Popen = self.fn()

        stdout, stderr = self.proc.communicate(input=None, timeout=None)
        exit_code = self.proc.wait()

        # TODO: Figure out how to prevent this error. It is thrown sometimes when you have a browser open
        # but close PnTest without closing the browser first.
        # See: http://enki-editor.org/2014/08/23/Pyqt_mem_mgmt.html
        try:
            self.signals.exited.emit(self)
        except RuntimeError as err:
            print("RuntimeError: ", err)

    def kill(self):
        os.kill(self.proc.pid, signal.SIGTERM)
