import sys
import traceback

from PySide2.QtCore import Slot, Signal, QObject, QRunnable

class WorkerSignals(QObject):
  finished = Signal()
  error = Signal(tuple)
  result = Signal(object)

class BackgroundWorker(QRunnable):
  def __init__(self, fn, *args, **kwargs):
    super(BackgroundWorker, self).__init__()

    # Store constructor arguments (re-used for processing)
    self.fn = fn
    self.args = args
    self.kwargs = kwargs
    self.signals = WorkerSignals()

  @Slot()
  def run(self):
    # Retrieve args/kwargs here; and fire processing using them
    try:
      result = self.fn(*self.args, **self.kwargs)
    except:
      exctype, value = sys.exc_info()[:2]
      self.signals.error.emit((exctype, value, traceback.format_exc()))
    else:
      self.signals.result.emit(result)  # Return the result of the processing
    finally:
      self.signals.finished.emit()  # Done
