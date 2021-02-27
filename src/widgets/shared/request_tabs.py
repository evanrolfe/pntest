from PySide2 import QtWidgets

from widgets.shared.request_headers_form import RequestHeadersForm
from widgets.shared.request_body_form import RequestBodyForm

class RequestTabs(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super(RequestTabs, self).__init__(*args, **kwargs)

    def set_editor_item(self, editor_item):
        self.editor_item = editor_item

        self.request_headers_form = RequestHeadersForm(self.editor_item)
        self.request_body_form = RequestBodyForm(self.editor_item)

        self.insertTab(0, self.request_headers_form, 'Headers')
        self.insertTab(1, self.request_body_form, 'Body')
