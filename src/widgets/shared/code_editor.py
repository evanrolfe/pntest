from PyQt6 import QtCore, QtWidgets

from views._compiled.shared.code_editor import Ui_CodeEditor

class WebBridge(QtCore.QObject):
    set_code = QtCore.pyqtSignal(str, str)

    def __init__(self, *args, **kwargs):
        super(WebBridge, self).__init__(*args, **kwargs)
        self.value = ''
        self.format = ''

    def set_value(self, value, format):
        self.value = value
        self.format = format
        self.emit_set_code()

    def emit_set_code(self):
        self.set_code.emit(self.value, self.format)

    def code_changed(self, value):
        self.value = value

class CodeEditor(QtWidgets.QWidget):
    set_code = QtCore.pyqtSignal(str, str)

    def __init__(self, *args, **kwargs):
        super(CodeEditor, self).__init__(*args, **kwargs)
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)

    def set_value(self, value, format=''):
        self.ui.code.setPlainText(value)

    def get_value(self) -> str:
        return self.ui.code.toPlainText()
