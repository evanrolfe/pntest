from copy import deepcopy
from typing import Optional
from PyQt6 import QtCore, QtWidgets
from entities.http_flow import HttpFlow

from ui.views._compiled.shared.headers_form import Ui_HeadersForm
from ui.qt_models.request_headers_table_model import RequestHeadersTableModel, HeaderTuple
from ui.widgets.shared.line_scintilla import LineScintilla
from lib.types import Headers
from constants import DEFAULT_HEADERS, EMPTY_HEADER

class MyDelegate(QtWidgets.QItemDelegate):
    flow: HttpFlow
    editable: bool

    # HttpFlow is necessary in order to allow the LineScintilla to access the payloads
    def __init__(self, parent = None):
        self.editable = True
        super(MyDelegate, self).__init__(parent)

    def createEditor(self, parent: QtWidgets.QWidget, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        self.line_scintilla = LineScintilla(parent)
        self.line_scintilla.setReadOnly(not self.editable)
        return self.line_scintilla

    def setModelData(self, editor: LineScintilla, model: RequestHeadersTableModel, index: QtCore.QModelIndex):
        value = editor.text()
        model.setData(index, value, QtCore.Qt.ItemDataRole.EditRole)

    def setEditorData(self, editor: LineScintilla, index: QtCore.QModelIndex):
        value = index.model().data(index, QtCore.Qt.ItemDataRole.EditRole)
        editor.setText(value)

    def set_editable(self, editable: bool):
        self.editable = editable

class HeadersForm(QtWidgets.QWidget):
    # TODO: Add a headers_changed signal
    headers_changed = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(HeadersForm, self).__init__(*args, **kwargs)

        self.ui = Ui_HeadersForm()
        self.ui.setupUi(self)

        self.editable = False
        self.table_model = RequestHeadersTableModel([])
        self.table_model.headers_changed.connect(self.headers_changed)

        self.set_header_line('')
        self.set_headers({})

        self.ui.headersTable.setModel(self.table_model)
        self.delegate = MyDelegate()
        self.ui.headersTable.setItemDelegate(self.delegate)

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

        self.ui.headerLine.setReadOnly(True)

    def set_editable(self, editable):
        self.editable = editable
        self.delegate.set_editable(self.editable)

    def set_header_line(self, header_line):
        if header_line is not None:
            self.ui.headerLine.setText(header_line)
        else:
            self.ui.headerLine.setVisible(False)

    def set_default_headers(self):
        headers = DEFAULT_HEADERS[:] + [EMPTY_HEADER]
        self.table_model.set_headers(deepcopy(headers))

    def set_headers(self, headers: Optional[Headers]):
        if headers is None:
            new_headers: list[HeaderTuple] = []
        else:
            new_headers = [(True, key, value) for key, value in headers.items()]

        if self.editable:
            new_headers.append(deepcopy(EMPTY_HEADER))

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
