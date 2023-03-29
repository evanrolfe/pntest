from __future__ import annotations

import os
import pty
import re
import signal
import sys

import docker
import pyte
from PyQt6 import Qsci, QtCore, QtGui, QtWidgets

from entities.container import Container
from lib.debounce import debounce
from lib.paths import get_app_config_path, get_app_path, get_resource_path
from lib.stylesheet_loader import StyleheetLoader
from ui.widgets.shared.code_themes import DarkTheme


class WorkerSignals(QtCore.QObject):
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)

class LogsProc(QtCore.QRunnable):
    signals: WorkerSignals
    container: Container
    logs_text: QtWidgets.QPlainTextEdit

    log_lines: list[str]

    def __init__(self, container: Container, logs_text: QtWidgets.QPlainTextEdit):
        super(LogsProc, self).__init__()

        self.container = container
        self.logs_text = logs_text
        self.log_lines = []

        self.signals = WorkerSignals()
        self.alive = True
        self.last_cmd = ''
        self.alive = True

    def kill(self):
        print("[ConsoleProc] killing logs worker.. ")
        self.alive = False

    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            # Read from the TTY process and write to standard output
            while True:
                try:
                    client = docker.from_env()
                    container = client.containers.get(self.container.short_id)

                    logs = container.logs(stream=True) # type: ignore

                    for line in logs:
                        # Hacky way of allow us to "cancel" a worker
                        if not self.alive:
                            return

                        self.log_lines.append(line.decode())
                        self.emit_result()

                    print("[LogsProc] done")
                except:
                    break

        except:  # noqa: E722
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value))

    @debounce(0.1)
    def emit_result(self):
        self.signals.result.emit(self.log_lines)
        self.log_lines = []
