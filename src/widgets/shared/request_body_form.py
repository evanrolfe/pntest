from PySide2 import QtWidgets

from views._compiled.shared.ui_request_body_form import Ui_RequestBodyForm

class RequestBodyForm(QtWidgets.QWidget):
    def __init__(self, editor_item, *args, **kwargs):
        super(RequestBodyForm, self).__init__(*args, **kwargs)
        self.ui = Ui_RequestBodyForm()
        self.ui.setupUi(self)
        self.editor_item = editor_item
        self.load_body()

    def load_body(self):
        body = self.editor_item.item().request_payload
        if body is not None:
            self.ui.requestBodyInput.setPlainText(body)

    def get_body(self):
        return self.ui.requestBodyInput.toPlainText()
