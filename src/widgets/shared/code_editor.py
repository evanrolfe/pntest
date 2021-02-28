from PySide2 import QtCore, QtWidgets, QtWebChannel

from views._compiled.shared.ui_code_editor import Ui_CodeEditor

class CodeEditor(QtWidgets.QWidget):
    set_code = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super(CodeEditor, self).__init__(*args, **kwargs)
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)

        url = QtCore.QUrl('qrc:/html/codemirror.html')
        self.ui.code.setUrl(url)

        channel = QtWebChannel.QWebChannel(self)
        channel.registerObject('codeEditorPython', self)
        self.ui.code.page().setWebChannel(channel)

    def set_value(self, value):
        self.set_code.emit(value)

    def get_value(self):
        return 'TODO!'
