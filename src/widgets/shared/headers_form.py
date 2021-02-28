from PySide2 import QtWidgets, QtCore

from views._compiled.shared.ui_headers_form import Ui_HeadersForm
from models.qt.request_headers_table_model import RequestHeadersTableModel

class HeadersForm(QtWidgets.QWidget):
    CALCULATED_TEXT = '<calculated when request is sent>'
    DEFAULT_HEADERS = [
        [True, 'Content-Length', CALCULATED_TEXT],
        [True, 'Host', CALCULATED_TEXT],
        [True, 'Accept', '*/*'],
        [True, 'Accept-Encoding', 'gzip, deflate'],
        [True, 'Connection', 'keep-alive'],
        [True, 'User-Agent', 'pntest/0.1'],
    ]

    def __init__(self, *args, **kwargs):
        super(HeadersForm, self).__init__(*args, **kwargs)

        self.ui = Ui_HeadersForm()
        self.ui.setupUi(self)

        self.table_model = RequestHeadersTableModel([])
        self.set_header_line('')
        self.set_headers({})

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

    def set_header_line(self, header_line):
        if header_line is not None:
            self.ui.headerLine.setText(header_line)
        else:
            self.ui.headerLine.setVisible(False)

    def set_headers(self, headers):
        if headers is None:
            # headers = self.DEFAULT_HEADERS[:]
            headers = []
        else:
            headers = [[True, key, value] for key, value in headers.items()]

        self.table_model.set_headers(headers)

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
