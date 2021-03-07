from PySide2 import QtWidgets
from PySide2 import QtCore

from views._compiled.shared.ui_request_view import Ui_RequestView

class RequestView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(RequestView, self).__init__(*args, **kwargs)
        self.ui = Ui_RequestView()
        self.ui.setupUi(self)
        self.modified_dropdown = None
        self.show_modified = False

    def set_show_rendered(self, show_rendered):
        if show_rendered is False:
            self.ui.responseTabs.removeTab(2)

        self.show_rendered = show_rendered

    def show_modified_dropdown(self):
        self.modified_dropdown = QtWidgets.QComboBox()
        self.modified_dropdown.setContentsMargins(10, 10, 10, 10)
        self.modified_dropdown.insertItems(0, ['Modified', 'Original'])
        self.modified_dropdown.setObjectName('modifiedDropdown')
        self.modified_dropdown.currentIndexChanged.connect(self.show_modified_change)

        self.ui.requestTabs.setCornerWidget(self.modified_dropdown)
        self.show_modified = True

    @QtCore.Slot(int)
    def show_modified_change(self, index):
        if index == 0:  # Modified
            self.show_modified = True
        elif index == 1:  # Original
            self.show_modified = False

        self.show_request(self.request)

    def get_request_headers(self):
        return self.ui.requestHeaders.get_headers()

    def get_request_payload(self):
        return self.ui.requestPayload.get_value()

    def clear_request(self):
        # Request:
        self.ui.requestHeaders.set_header_line('')
        self.ui.requestHeaders.set_headers({})
        self.ui.requestPayload.set_value('')

        # Response:
        self.ui.responseRaw.set_value('')
        self.ui.responseRendered.set_value('')
        self.ui.responseBodyPreview.setHtml(None)

    def set_request(self, request):
        self.request = request
        self.set_modified_dropdown(request)
        self.show_request(self.request)

    def show_request(self, request):
        if self.show_modified:
            request = request.get_modified_request()

        # Request:
        self.ui.requestHeaders.set_header_line(request.get_request_header_line())
        self.ui.requestHeaders.set_headers(request.get_request_headers())
        self.ui.requestPayload.set_value(request.request_payload or '')
        # Response:
        self.set_response(request)

    def set_modified_dropdown(self, request):
        if self.modified_dropdown:
            if request.modified():
                self.modified_dropdown.setEnabled(True)
                self.modified_dropdown.setCurrentIndex(0)
            else:
                self.modified_dropdown.setEnabled(False)
                self.modified_dropdown.setCurrentIndex(1)

    def set_response(self, request):
        self.ui.responseHeaders.set_header_line(request.get_response_header_line())
        self.ui.responseHeaders.set_headers(request.get_response_headers())
        self.ui.responseRaw.set_value(request.response_body or '')
        if self.show_rendered:
            self.ui.responseRendered.set_value(request.response_body_rendered or '')

        self.ui.responseBodyPreview.setHtml(request.response_body_for_preview(), baseUrl=request.get_url())

    @QtCore.Slot()
    def show_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.loaderWidget)

    @QtCore.Slot()
    def hide_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.responseTabs)
