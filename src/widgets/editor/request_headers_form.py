from PySide2 import QtWidgets, QtCore

from views._compiled.editor.ui_request_headers_form import Ui_RequestHeadersForm
from models.qt.editor_request_headers_table_model import EditorRequestHeadersTableModel

class RequestHeadersForm(QtWidgets.QWidget):
    CALCULATED_TEXT = '<calculated when request is sent>'
    DEFAULT_HEADERS = [
        [True, 'Content-Length', CALCULATED_TEXT],
        [True, 'Host', CALCULATED_TEXT],
        [True, 'Accept', '*/*'],
        [True, 'Accept-Encoding', 'gzip, deflate'],
        [True, 'Connection', 'keep-alive'],
        [True, 'User-Agent', 'pntest/0.1'],
    ]

    def __init__(self, editor_item, *args, **kwargs):
        super(RequestHeadersForm, self).__init__(*args, **kwargs)
        self.editor_item = editor_item

        self.ui = Ui_RequestHeadersForm()
        self.ui.setupUi(self)
        self.load_headers()

        self.table_model = EditorRequestHeadersTableModel(self.headers)
        self.ui.headersTable.setModel(self.table_model)
        self.ui.headersTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        horizontalHeader = self.ui.headersTable.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

        verticalHeader = self.ui.headersTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        self.ui.headersTable.setColumnWidth(0, 20)
        self.ui.headersTable.setColumnWidth(1, 250)

        # self.ui.showGeneratedHeaders.setTristate(False)
        # self.ui.showGeneratedHeaders.stateChanged.connect(self.show_generated_headers)

    def load_headers(self):
        headers = self.editor_item.item().get_request_headers()

        if headers is None:
            self.headers = self.DEFAULT_HEADERS[:]
        else:
            self.headers = [[True, key, value]
                            for key, value in headers.items()]

    @QtCore.Slot()
    def show_generated_headers(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.headersTable.showRow(0)
            self.ui.headersTable.showRow(1)
        else:
            self.ui.headersTable.hideRow(0)
            self.ui.headersTable.hideRow(1)

    def get_headers(self):
        return self.table_model.get_headers()
