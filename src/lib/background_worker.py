import sys
import traceback
from typing import cast
from PySide2 import QtCore

class WorkerSignals(QtCore.QObject):
    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)

    # Only used by FuzzHttpRequest
    response_received = QtCore.Signal(object)

class BackgroundWorker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(BackgroundWorker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.alive = True

    def kill(self):
        self.alive = False

    @QtCore.Slot()  # type: ignore
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(self.signals)

            # Hacky way of allow us to "cancel" a worker
            if not self.alive:
                return
        except:  # noqa: E722
            exctype, value = sys.exc_info()[:2]
            cast(QtCore.SignalInstance, self.signals.error).emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            cast(QtCore.SignalInstance, self.signals.result).emit(result)
        finally:
            cast(QtCore.SignalInstance, self.signals.finished).emit()
