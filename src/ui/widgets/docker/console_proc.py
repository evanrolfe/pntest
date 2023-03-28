from __future__ import annotations

import os
import pty
import re
import signal
import sys

import pyte
from PyQt6 import Qsci, QtCore, QtGui, QtWidgets

import qbash_util
from lib.paths import get_app_config_path, get_app_path, get_resource_path
from lib.stylesheet_loader import StyleheetLoader
from ui.widgets.shared.code_themes import DarkTheme

THEME = 'dark'
NUM_LINES = 500

class WorkerSignals(QtCore.QObject):
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)

class ConsoleProc(QtCore.QRunnable):
    pid: int
    file_desc: int
    line_prefix: str
    last_cmd: str

    screen: pyte.Screen
    stream: pyte.ByteStream
    args: list[str]

    def __init__(self, args: list[str], numLines=24, numColumns=80):
        super(ConsoleProc, self).__init__()

        self.args = args

        self.signals = WorkerSignals()
        self.alive = True
        self.last_cmd = ''

        # Setup Pyte (hard coded display size for now).
        self.screen = pyte.Screen(numColumns, numLines)
        self.stream = pyte.ByteStream()
        self.stream.attach(self.screen)

        # Change the 'TERM' environment variable to 'linux' to ensure
        # that Bash does not internally disable the readline library.
        self.envVars = {'TERM': 'linux', 'LANG': 'en_GB.UTF-8'}

    def kill(self):
        print("[ConsoleProc] killing proc ", self.pid)
        os.kill(self.pid, signal.SIGTERM)

    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            # Start the TTY process
            self.pid, self.file_desc = pty.fork()
            if self.pid == 0:
                # We are in the child process: flush stdout to be safe.
                sys.stdout.flush()

                # Setup the environment variables for the new terminal.
                for key, value in self.envVars.items():
                    os.environ[key] = value
                os.execvp('docker', self.args)

            # Read from the TTY process and write to standard output
            while True:
                try:
                    data = os.read(self.file_desc, 1024)
                    if not data:
                        break
                    print('received data:', data.decode())
                    # Feed output into Pyte's state machine and send the new screen
                    # output to the GUI thread.
                    self.stream.feed(data)
                    self.signals.result.emit(self.screen)
                except:
                    break

        except:  # noqa: E722
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value))

    def key_pressed(self, byte_code: bytes):
        print("Sending: ", byte_code)
        os.write(self.file_desc, byte_code)
