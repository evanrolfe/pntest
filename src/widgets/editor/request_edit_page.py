import sys
import time

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView, QPushButton
from PySide2.QtCore import QFile, Slot, Signal, QObject, QRunnable, QThreadPool
from PySide2.QtUiTools import QUiLoader

from views._compiled.editor.ui_request_edit_page import Ui_RequestEditPage
from widgets.editor.request_headers_form import RequestHeadersForm
from widgets.editor.request_body_form import RequestBodyForm

from lib.app_settings import AppSettings
from lib.backend import Backend
from lib.http_request import HttpRequest

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class RequestEditPage(QWidget):
  form_input_changed = Signal(bool)

  METHODS = ['GET','POST','PATCH','PUT','DELETE']

  def __init__(self, editor_item):
    super(RequestEditPage, self).__init__()

    self.editor_item = editor_item
    self.request = self.editor_item.item()
    self.ui = Ui_RequestEditPage()
    self.ui.setupUi(self)

    self.ui.urlInput.setText(self.editor_item.name)
    self.layout().setContentsMargins(0, 0, 0, 0)

    self.hide_fuzz_table()
    self.settings = AppSettings.get_instance()
    self.restore_layout_state()

    self.ui.toggleFuzzTableButton.clicked.connect(self.toggle_fuzz_table)
    self.ui.sendButton.clicked.connect(self.show_loader)
    self.ui.sendButton.clicked.connect(self.send_request)
    self.ui.saveButton.clicked.connect(self.save_request)
    self.ui.methodInput.insertItems(0, self.METHODS)
    self.show_request()
    self.request_is_modified = False

    save_response_button = QPushButton('Save Response')
    save_response_button.setContentsMargins(10, 10, 10, 10)
    self.ui.responseTabs.setCornerWidget(save_response_button)

    # Form inputs:
    self.ui.urlInput.textChanged.connect(self.form_field_changed)
    self.ui.methodInput.currentIndexChanged.connect(self.form_field_changed)

    #self.show_loader()
    self.threadpool = QThreadPool()

  @Slot()
  def show_loader(self):
    print('showing the loader')
    self.ui.stackedWidget.setCurrentWidget(self.ui.loaderWidget)

  def hide_loader(self):
    print('hiding the loader')
    self.ui.stackedWidget.setCurrentWidget(self.ui.responseTabs)

  def show_request(self):
    self.ui.urlInput.setText(self.request.url)
    self.set_method_on_form(self.request.method)

    # Request Headers and body
    self.request_headers_form = RequestHeadersForm(self.editor_item)
    self.request_body_form = RequestBodyForm(self.editor_item)

    self.ui.requestTabs.insertTab(0, self.request_headers_form, 'Headers')
    self.ui.requestTabs.insertTab(1, self.request_body_form, 'Body')

  @Slot()
  def save_request(self):
    method = self.ui.methodInput.currentText()
    url = self.ui.urlInput.text()
    headers = self.request_headers_form.get_headers()

    self.request.url = url
    self.request.method = method
    self.request.request_payload = self.request_body_form.get_body()
    self.request.set_request_headers(headers)
    self.request.save()

    print(f'saving {method} {url} to request {self.request.id}')

  def execute_this_fn(self, progress_callback):
    for n in range(0, 5):
      time.sleep(1)
      print(n)

    return "Done."

  @Slot()
  def print_output(self, s):
    print(s)

  @Slot()
  def send_request(self):
    print('Sending the request!')
    self.show_loader()
    # TODO: https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/

    # Pass the function to execute
    worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
    worker.signals.result.connect(self.print_output)
    worker.signals.finished.connect(self.hide_loader)
    worker.signals.progress.connect(self.print_output)

    self.threadpool.start(worker)

    return
    # method = self.ui.methodInput.currentText()
    # url = self.ui.urlInput.text()
    # headers = self.request_headers_form.get_headers()
    # body = self.request_body_form.get_body()

    # http_request = HttpRequest(method, url, headers, body)
    # response = http_request.send()

    # # Display response headers and body
    # self.ui.responseBodyText.setPlainText(response.text)
    # headers_text = ""
    # for key, value in response.headers.items():
    #   headers_text += f"{key}: {value}\n"
    # self.ui.responseHeadersText.setPlainText(headers_text)

    self.hide_loader()

  @Slot()
  def form_field_changed(self):
    request_on_form = {
      'method': self.ui.methodInput.currentText(),
      'url': self.ui.urlInput.text()
    }
    original_request = {
      'method': self.request.method or self.METHODS[0],
      'url': self.request.url or ''
    }

    self.request_is_modified = (request_on_form != original_request)
    self.form_input_changed.emit(self.request_is_modified)

  def hide_fuzz_table(self):
    self.ui.fuzzRequestsTable.setVisible(False)
    self.ui.toggleFuzzTableButton.setText(">>")

  @Slot()
  def toggle_fuzz_table(self):
    visible = not self.ui.fuzzRequestsTable.isVisible()
    self.ui.fuzzRequestsTable.setVisible(visible)

    if visible:
      self.restore_layout_state()

    if (visible):
      self.ui.toggleFuzzTableButton.setText("<<")
    else:
      self.ui.toggleFuzzTableButton.setText(">>")

  def restore_layout_state(self):
    splitter_state = self.settings.get("RequestEditPage.splitter", None)
    splitter_state2 = self.settings.get("RequestEditPage.splitter2", None)

    self.ui.requestEditSplitter.restoreState(splitter_state)
    self.ui.splitter2.restoreState(splitter_state2)

  def save_layout_state(self):
    splitter_state = self.ui.requestEditSplitter.saveState()
    splitter_state2 = self.ui.splitter2.saveState()

    self.settings.save("RequestEditPage.splitter", splitter_state)
    self.settings.save("RequestEditPage.splitter2", splitter_state2)

  def set_method_on_form(self, method):
    if method == None:
      index = 0
    else:
      index = self.METHODS.index(method)

    self.ui.methodInput.setCurrentIndex(index)
