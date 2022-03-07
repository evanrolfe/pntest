# from html5print import HTMLBeautifier
from PySide2 import QtWidgets
from PySide2 import QtCore

from views._compiled.editor.ui_fuzz_view import Ui_FuzzView
from lib.types import Headers
from models.qt.payloads_files_table_model import PayloadFilesTableModel
from models.data.payload_file import PayloadFile

class FuzzView(QtWidgets.QWidget):
    save_example_clicked = QtCore.Signal()
    cancel_clicked = QtCore.Signal()

    FORMATS = ['JSON', 'XML', 'HTML', 'Javascript', 'Unformatted']

    def __init__(self, *args, **kwargs):
        super(FuzzView, self).__init__(*args, **kwargs)
        self.ui = Ui_FuzzView()
        self.ui.setupUi(self)

        self.ui.requestHeaders.set_editable(True)
        self.ui.addPayloadButton.clicked.connect(self.add_payload)

        # Configure Table
        horizontalHeader = self.ui.payloadsTable.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        horizontalHeader.setHighlightSections(False)

        verticalHeader = self.ui.payloadsTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        self.ui.payloadsTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.ui.payloadsTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        self.ui.loaderWidget.ui.cancelButton.clicked.connect(self.hide_loader)
        self.ui.loaderWidget.ui.cancelButton.clicked.connect(self.cancel_clicked)

    def get_request_headers(self) -> Headers:
        return self.ui.requestHeaders.get_headers()

    def get_request_body(self) -> str:
        return self.ui.requestBody.get_value()

    def get_request_payload_files(self) -> list[PayloadFile]:
        return self.table_model.payloads

    def clear_request(self):
        # Request:
        self.ui.requestHeaders.set_header_line('')
        self.ui.requestHeaders.set_headers({})
        self.ui.requestBody.set_value('')

    def set_flow(self, flow):
        self.flow = flow
        self.set_request(flow)

    def set_request(self, flow):
        request = flow.request

        self.ui.requestHeaders.set_header_line(request.get_header_line())
        if request.form_data['headers']:
            self.ui.requestHeaders.set_headers(request.form_data['headers'])
        else:
            self.ui.requestHeaders.set_default_headers()
        self.ui.requestBody.set_value(request.form_data['content'] or '')

        self.table_model = PayloadFilesTableModel(request.payload_files())
        self.ui.payloadsTable.setModel(self.table_model)

    @QtCore.Slot()  # type:ignore
    def add_payload(self):
        file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Import Payload File",
            "~/"
        )
        file_path = file[0]

        if file_path == '':  # Cancel was pressed:
            return

        payload = PayloadFile(file_path, f'payload{len(self.table_model.payloads) + 1}')
        payload.verify_file()

        self.table_model.insert_payload(payload)
        print(f'adding payload from {file_path}')

    @QtCore.Slot()  # type:ignore
    def show_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.loaderWidget)

    @QtCore.Slot()  # type:ignore
    def hide_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.requestTabs)
