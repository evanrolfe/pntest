from copy import deepcopy
from typing import Optional
from PyQt6 import QtWidgets, QtCore, QtGui

from views._compiled.shared.headers_form import Ui_HeadersForm
from models.qt.request_headers_table_model import RequestHeadersTableModel, HeaderTuple
from widgets.shared.line_scintilla import LineScintilla
from lib.types import Headers

class MyDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent = None):
        super(MyDelegate, self).__init__(parent)

    def createEditor(self, parent: QtWidgets.QWidget, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        return LineScintilla(parent)

    def setModelData(self, editor: LineScintilla, model: RequestHeadersTableModel, index: QtCore.QModelIndex):
        value = editor.text()
        model.setData(index, value, QtCore.Qt.ItemDataRole.EditRole)

    def setEditorData(self, editor: LineScintilla, index: QtCore.QModelIndex):
        value = index.model().data(index, QtCore.Qt.ItemDataRole.EditRole)
        editor.setText(value)

class HeadersForm(QtWidgets.QWidget):
    CALCULATED_TEXT = '<calculated when request is sent>'
    DEFAULT_HEADERS = [
        (True, 'Content-Length', CALCULATED_TEXT),
        (True, 'Host', CALCULATED_TEXT),
        (True, 'Accept', '*/*'),
        (True, 'Accept-Encoding', 'gzip, deflate'),
        (True, 'Connection', 'keep-alive'),
        (True, 'User-Agent', 'pntest/0.1'),
    ]
    EMPTY_HEADER = (False, '', '')

    def __init__(self, *args, **kwargs):
        super(HeadersForm, self).__init__(*args, **kwargs)

        self.ui = Ui_HeadersForm()
        self.ui.setupUi(self)

        self.editable = False
        self.table_model = RequestHeadersTableModel([])
        self.set_header_line('')
        self.set_headers({})

        self.ui.headersTable.setModel(self.table_model)
        delegate = MyDelegate()
        self.ui.headersTable.setItemDelegate(delegate)

        self.ui.headersTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)

        horizontalHeader = self.ui.headersTable.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)

        verticalHeader = self.ui.headersTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        self.ui.headersTable.setColumnWidth(0, 20)
        self.ui.headersTable.setColumnWidth(1, 250)

    def set_editable(self, editable):
        self.editable = editable

    def set_header_line(self, header_line):
        if header_line is not None:
            self.ui.headerLine.setText(header_line)
        else:
            self.ui.headerLine.setVisible(False)

    def set_default_headers(self):
        headers = self.DEFAULT_HEADERS[:] + [self.EMPTY_HEADER]
        self.table_model.set_headers(deepcopy(headers))

    def set_headers(self, headers: Optional[Headers]):
        if headers is None:
            new_headers: list[HeaderTuple] = []
        else:
            new_headers = [(True, key, value) for key, value in headers.items()]

        if self.editable:
            new_headers.append(deepcopy(self.EMPTY_HEADER))

        self.table_model.set_headers(new_headers)

    def show_generated_headers(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            self.ui.headersTable.showRow(0)
            self.ui.headersTable.showRow(1)
        else:
            self.ui.headersTable.hideRow(0)
            self.ui.headersTable.hideRow(1)

    def get_header_line(self):
        return self.ui.headerLine.text()

    def get_headers(self) -> Headers:
        return self.table_model.get_headers()
