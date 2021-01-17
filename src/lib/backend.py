import json
import time

from PySide2.QtCore import QProcess, Slot, QByteArray
from PySide2.QtWidgets import QMessageBox

from models.request import Request

LIST_AVAILABLE_CLIENTS_COMMAND = b'{"command": "listAvailableClientTypes"}'

class Backend:
  # Singleton method stuff:
  __instance = None
  @staticmethod
  def get_instance():
    # Static access method.
    if Backend.__instance == None:
        Backend()
    return Backend.__instance

  def __init__(self, app_path, db_path, backend_path_rel):
    self.app_path = app_path
    self.db_path = db_path
    self.backend_path = f'{self.app_path}/{backend_path_rel}'
    self.callbacks = {
      'newRequest': [],
      'updatedRequest': [],
      'clientsAvailable': [],
      'clientsChanged': [],
      'requestIntercepted': [],
      'responseIntercepted': [],
      'backendLoaded': []
    }

    # Virtually private constructor.
    if Backend.__instance != None:
        raise Exception("This class is a singleton!")
    else:
        Backend.__instance = self
  # /Singleton method stuff

  def start(self):
    print("Starting the backend...")
    #loop = asyncio.get_event_loop()
    #future = loop.create_future()
    #self.register_callback('backendLoaded', lambda: loop.call_soon(print('!!!!!!!!!!!!!!! done'), future, 'backendLoaded'))

    self.backend_proc = QProcess()
    self.backend_proc.start(f'{self.backend_path} --appPath={self.app_path} --dbPath={self.db_path}')
    self.backend_proc.readyReadStandardOutput.connect(self.std_out_received)
    self.backend_proc.readyReadStandardError.connect(self.std_err_received)

    #result = await future
    #print(f'----------> the result is: {result}')

  def kill(self):
    print("Stopping the backend...")
    self.backend_proc.terminate()
    self.backend_proc.waitForFinished(-1)

  def std_out_received(self):
    output = self.backend_proc.readAllStandardOutput()
    lines = str(output, encoding='utf-8').split("\n")

    for line in lines:
      if (line[0:6] == '[JSON]'):
        self.process_json(line[6:].strip())
      else:
        print(line)

  def send_command(self, command):
    print(command)
    command_bytes = QByteArray(command + b'\n')
    self.backend_proc.write(command_bytes)

  def std_err_received(self):
    line = self.backend_proc.readAllStandardError()
    line = str(line, encoding='utf-8')
    self._show_error_box(line)

  def _show_error_box(self, message):
    message_box = QMessageBox()
    message_box.setWindowTitle('Error')
    message_box.setText(message)
    message_box.exec_()

    print(message)

  def register_callback(self, message_type, callback):
    self.callbacks[message_type].append(callback)

  def process_json(self, line):
    try:
      obj = json.loads(line)

      if (obj['type'] == 'newRequest'):
        for callback in self.callbacks['newRequest']:
          request = Request(obj['request'])
          callback(request)

      elif (obj['type'] == 'updatedRequest'):
        print(obj)
        for callback in self.callbacks['updatedRequest']:
          request = Request(obj['request'])
          callback(request)

      elif (obj['type'] == 'clientsAvailable'):
        for callback in self.callbacks['clientsAvailable']:
          callback(obj['clients'])

      elif (obj['type'] == 'clientsChanged'):
        for callback in self.callbacks['clientsChanged']:
          callback()

      elif (obj['type'] == 'requestIntercepted'):
        for callback in self.callbacks['requestIntercepted']:
          callback(obj['request'])

      elif (obj['type'] == 'responseIntercepted'):
        for callback in self.callbacks['responseIntercepted']:
          callback(obj['request'])

      elif (obj['type'] == 'backendLoaded'):
        for callback in self.callbacks['backendLoaded']:
          callback()


    except json.decoder.JSONDecodeError:
      print("[BackendHandler] could not parse json: ")
      print(line)

  #-----------------------------------------------------------------------------
  # Commands:
  #-----------------------------------------------------------------------------
  def get_available_clients(self):
    self.send_command(LIST_AVAILABLE_CLIENTS_COMMAND)

  def start_crawler(self, crawl_id):
    command = b'{"command": "createCrawl", "crawlId": ' + bytes(str(crawl_id), 'utf8') + b'}'
    self.send_command(command)

  def open_client(self, client_id):
    command = b'{"command": "openClient", "id": ' + bytes(str(client_id), 'utf8') + b'}'
    self.send_command(command)

  def close_client(self, client_id):
    command = b'{"command": "closeClient", "id": ' + bytes(str(client_id), 'utf8') + b'}'
    self.send_command(command)

  def bring_to_front_client(self, client_id):
    command = b'{"command": "bringToFrontClient", "id": ' + bytes(str(client_id), 'utf8') + b'}'
    self.send_command(command)

  def forward_request(self, request):
    request_json = json.dumps(request)
    command = b'{"command": "forward", "request": ' + bytes(request_json, 'utf8') + b'}'
    self.send_command(command)

  def forward_intercept_request(self, request):
    request_json = json.dumps(request)
    command = b'{"command": "forwardAndIntercept", "request": ' + bytes(request_json, 'utf8') + b'}'
    self.send_command(command)

  def change_setting(self, key, value):
    if (isinstance(value, bool)):
      value = str(value).lower()

    elif (isinstance(value, int)):
      value = str(value)

    else:
      # Otherwise add quotes:
      value = f'"value"'

    key = bytes(key, 'utf8')
    value = bytes(value, 'utf8')
    command = b'{"command": "changeSetting", "key": "' + key + b'", "value": ' + value + b'}'
    self.send_command(command)

