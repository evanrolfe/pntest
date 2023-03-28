from __future__ import annotations

import os
import pty
import re
import signal
import sys

import pyte
from PyQt6 import Qsci, QtCore, QtGui, QtWidgets

from lib.paths import get_app_config_path, get_app_path, get_resource_path
from lib.qbash_utils import QtKeyToAscii
from lib.stylesheet_loader import StyleheetLoader
from ui.widgets.shared.code_themes import DarkTheme

NUM_LINES = 500

class ConsoleScintilla(Qsci.QsciScintilla):
    esc_pressed = QtCore.pyqtSignal()
    key_pressed = QtCore.pyqtSignal(bytes)

    clipboard: QtGui.QClipboard

    def __init__(self, *args, **kwargs):
        super(ConsoleScintilla, self).__init__(*args, **kwargs)

        self.setUtf8(True)
        self.clipboard = QtWidgets.QApplication.clipboard()
        # Right click behaviour
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_clicked)

        self.theme = DarkTheme
        self.apply_theme()

        self.setWrapMode(Qsci.QsciScintilla.WrapMode.WrapWord)
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)

    def output_received(self, screenData: pyte.Screen):
        lastFg, lastBg = 'default', '#1E1E1E'

        # Strip the trailing empty lines
        only_empty_lines_encountered = True
        non_empty_lines = []
        for line in screenData.display[::-1]:
            if only_empty_lines_encountered and line.strip() == '':
                continue

            non_empty_lines = [line] + non_empty_lines
            only_empty_lines_encountered = False

        self.setText('\n'.join(non_empty_lines))
        self.setCursorPosition(screenData.cursor.y, screenData.cursor.x)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ShiftModifier| QtCore.Qt.KeyboardModifier.ControlModifier:
            if event.key() == QtCore.Qt.Key.Key_C:
                self.copy_clicked()

            if event.key() == QtCore.Qt.Key.Key_V:
                self.paste_clicked()
                return

        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.esc_pressed.emit()
            return

        # Convert the Qt key to the correct ASCII code.
        byte_code = QtKeyToAscii(event)
        if byte_code is not None:
            self.key_pressed.emit(byte_code)

    def right_clicked(self, position: QtCore.QPoint):
        clipboard_text = self.clipboard.text(mode=QtGui.QClipboard.Mode.Clipboard)
        menu = QtWidgets.QMenu(self)

        copy_action = QtGui.QAction("Copy (Ctrl+Shift+C)")
        copy_action.triggered.connect(self.copy_clicked)
        copy_action.setEnabled(self.hasSelectedText())

        paste_action = QtGui.QAction("Paste (Ctrl+Shift+V)")
        paste_action.triggered.connect(self.paste_clicked)
        paste_action.setEnabled(len(clipboard_text) > 0)

        menu.addAction(copy_action)
        menu.addAction(paste_action)

        position = self.sender().mapToGlobal(position) # type: ignore
        menu.exec(position)

    def copy_clicked(self):
        text = self.selectedText()
        self.clipboard.clear(mode=QtGui.QClipboard.Mode.Clipboard)
        self.clipboard.setText(text, mode=QtGui.QClipboard.Mode.Clipboard)

    def paste_clicked(self):
        text = self.clipboard.text(mode=QtGui.QClipboard.Mode.Clipboard)
        print("pasting ", text)
        byte_code = text.encode('utf8')
        self.key_pressed.emit(byte_code)

    def apply_theme(self):
        self.setPaper(QtGui.QColor(self.theme.default_bg))
        self.setColor(QtGui.QColor(self.theme.default_color))
        self.setCaretForegroundColor(QtGui.QColor(self.theme.default_color))

        self.setMarginsBackgroundColor(QtGui.QColor(self.theme.default_bg))
        self.setMarginsForegroundColor(QtGui.QColor(self.theme.darker_color))

        self.setIndentationGuidesBackgroundColor(QtGui.QColor(self.theme.darker_color))

        # Set Search Indicator Style
        self.setMatchedBraceForegroundColor(QtGui.QColor(self.theme.default_color))
        self.setMatchedBraceBackgroundColor(QtGui.QColor(self.theme.selected_secondary_color))
        font = self.theme.get_font()
        self.setFont(font)
