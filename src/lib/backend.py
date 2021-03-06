import json
from PySide2 import QtCore, QtWidgets
import pendulum

from models.request import Request
from models.data.websocket_message import WebsocketMessage

LIST_AVAILABLE_CLIENTS_COMMAND = b'{"command": "listAvailableClientTypes"}'

class Backend:
    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance():
        # Static access method.
        if Backend.__instance is None:
            Backend()
        return Backend.__instance

    def __init__(self, app_path, data_path, db_path, backend_path):
        self.app_path = app_path
        self.data_path = data_path
        self.db_path = db_path
        self.backend_path = backend_path
        self.callbacks = {
            'newRequest': [],
            'updatedRequest': [],
            'newWebsocketMessage': [],
            'clientsAvailable': [],
            'clientsChanged': [],
            'requestIntercepted': [],
            'responseIntercepted': [],
            'backendLoaded': []
        }

        # Virtually private constructor.
        if Backend.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Backend.__instance = self
    # /Singleton method stuff

    def reload_with_new_database(self, new_db_path):
        self.kill()
        self.db_path = new_db_path
        self.start()

    def start(self):
        print("Starting the backend...")
        cmd = f'{self.backend_path} --appPath={self.app_path} --dbPath={self.db_path} --dataPath={self.data_path}'
        print(cmd)
        self.backend_proc = QtCore.QProcess()
        self.backend_proc.start(cmd)
        self.backend_proc.readyReadStandardOutput.connect(self.std_out_received)
        self.backend_proc.readyReadStandardError.connect(self.std_err_received)

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
        command_bytes = QtCore.QByteArray(command + b'\n')
        self.backend_proc.write(command_bytes)

    def std_err_received(self):
        line = self.backend_proc.readAllStandardError()
        line = str(line, encoding='utf-8')
        self._show_error_box(line)

    def _show_error_box(self, message):
        message_box = QtWidgets.QMessageBox()
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
                for callback in self.callbacks['updatedRequest']:
                    request = Request(obj['request'])
                    callback(request)

            elif (obj['type'] == 'newWebsocketMessage'):
                # TODO: Move this logic to the model
                ws_message = WebsocketMessage()
                ws_message.id = obj['message']['id']
                ws_message.direction = obj['message']['direction']
                ws_message.request_id = obj['message']['request_id']
                ws_message.created_at = pendulum.from_timestamp(obj['message']['created_at'])

                for callback in self.callbacks['newWebsocketMessage']:
                    callback(ws_message)

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

    # -----------------------------------------------------------------------------
    # Commands:
    # -----------------------------------------------------------------------------
    def get_available_clients(self):
        self.send_command(LIST_AVAILABLE_CLIENTS_COMMAND)

    def start_crawler(self, crawl_id):
        command = b'{"command": "createCrawl", "crawlId": ' + \
            bytes(str(crawl_id), 'utf8') + b'}'
        self.send_command(command)

    def open_client(self, client_id):
        command = b'{"command": "openClient", "id": ' + \
            bytes(str(client_id), 'utf8') + b'}'
        self.send_command(command)

    def close_client(self, client_id):
        command = b'{"command": "closeClient", "id": ' + \
            bytes(str(client_id), 'utf8') + b'}'
        self.send_command(command)

    def bring_to_front_client(self, client_id):
        command = b'{"command": "bringToFrontClient", "id": ' + \
            bytes(str(client_id), 'utf8') + b'}'
        self.send_command(command)

    def forward_request(self, request):
        request_json = json.dumps(request)
        command = b'{"command": "forward", "request": ' + \
            bytes(request_json, 'utf8') + b'}'
        self.send_command(command)

    def forward_intercept_request(self, request):
        request_json = json.dumps(request)
        command = b'{"command": "forwardAndIntercept", "request": ' + \
            bytes(request_json, 'utf8') + b'}'
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
        command = b'{"command": "changeSetting", "key": "' + \
            key + b'", "value": ' + value + b'}'
        self.send_command(command)
