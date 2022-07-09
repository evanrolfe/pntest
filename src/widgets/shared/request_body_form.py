from PyQt6 import QtWidgets

from views._compiled.shared.request_body_form import Ui_RequestBodyForm

class RequestBodyForm(QtWidgets.QWidget):
    def __init__(self, request_body, *args, **kwargs):
        super(RequestBodyForm, self).__init__(*args, **kwargs)
        self.ui = Ui_RequestBodyForm()
        self.ui.setupUi(self)
        self.set_body(request_body)

    def set_body(self, request_body):
        self.request_body = request_body

        if self.request_body is not None:
            self.ui.requestBodyInput.setPlainText(self.request_body)

    def get_body(self):
        return self.ui.requestBodyInput.toPlainText()
