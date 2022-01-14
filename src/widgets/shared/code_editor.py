from PySide2 import QtCore, QtWidgets, QtWebChannel

from views._compiled.shared.ui_code_editor import Ui_CodeEditor

class WebBridge(QtCore.QObject):
    set_code = QtCore.Signal(str, str)

    def __init__(self, *args, **kwargs):
        super(WebBridge, self).__init__(*args, **kwargs)
        self.value = ''
        self.format = ''

    def set_value(self, value, format):
        self.value = value
        self.format = format
        self.emit_set_code()

    @QtCore.Slot()  # type:ignore
    def emit_set_code(self):
        self.set_code.emit(self.value, self.format)

    @QtCore.Slot(str)
    def code_changed(self, value):
        self.value = value

class CodeEditor(QtWidgets.QWidget):
    set_code = QtCore.Signal(str, str)

    def __init__(self, *args, **kwargs):
        super(CodeEditor, self).__init__(*args, **kwargs)
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)

        url = QtCore.QUrl('qrc:/html/codemirror.html')
        self.ui.code.setUrl(url)

        self.web_bridge = WebBridge()
        channel = QtWebChannel.QWebChannel(self.web_bridge)
        channel.registerObject('codeEditorPython', self.web_bridge)
        self.ui.code.page().setWebChannel(channel)

    def set_value(self, value, format=''):
        self.web_bridge.set_value(value, format)

    def get_value(self):
        return self.web_bridge.value
