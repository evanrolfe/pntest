from PySide2 import QtWidgets
from PySide2 import QtCore

from views._compiled.shared.ui_request_view import Ui_RequestView

# TODO: Rename this to FlowView
# TODO: Split this into two components, one for request, one for response

class RequestView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(RequestView, self).__init__(*args, **kwargs)
        self.ui = Ui_RequestView()
        self.ui.setupUi(self)
        self.request_modified_dropdown = None
        self.response_modified_dropdown = None
        self.show_modified_request = False
        self.show_modified_response = False

    def set_show_rendered(self, show_rendered):
        if show_rendered is False:
            self.ui.responseTabs.removeTab(2)

        self.show_rendered = show_rendered

    def show_modified_dropdown(self):
        self.request_modified_dropdown = QtWidgets.QComboBox()
        self.request_modified_dropdown.setContentsMargins(10, 10, 10, 10)
        self.request_modified_dropdown.insertItems(0, ['Modified', 'Original'])
        self.request_modified_dropdown.setObjectName('modifiedDropdown')
        self.request_modified_dropdown.currentIndexChanged.connect(self.show_modified_request_change)

        self.response_modified_dropdown = QtWidgets.QComboBox()
        self.response_modified_dropdown.setContentsMargins(10, 10, 10, 10)
        self.response_modified_dropdown.insertItems(0, ['Modified', 'Original'])
        self.response_modified_dropdown.setObjectName('modifiedDropdown')
        self.response_modified_dropdown.currentIndexChanged.connect(self.show_modified_response_change)

        self.ui.requestTabs.setCornerWidget(self.request_modified_dropdown)
        self.ui.responseTabs.setCornerWidget(self.response_modified_dropdown)
        self.show_modified_request = True
        self.show_modified_response = True

    @QtCore.Slot(int)
    def show_modified_request_change(self, index):
        if index == 0:  # Modified
            self.show_modified_request = True
        elif index == 1:  # Original
            self.show_modified_request = False

        self.set_request(self.flow)

    @QtCore.Slot(int)
    def show_modified_response_change(self, index):
        if index == 0:  # Modified
            self.show_modified_response = True
        elif index == 1:  # Original
            self.show_modified_response = False

        self.set_response(self.flow)

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

    def set_flow(self, flow):
        self.flow = flow
        self.set_modified_dropdown(flow)
        self.set_request(self.flow)
        self.set_response(flow)

    def set_request(self, flow):
        if self.show_modified_request:
            request = flow.request
        else:
            request = flow.original_request

        self.ui.requestHeaders.set_header_line(request.get_header_line())
        self.ui.requestHeaders.set_headers(request.get_headers())
        self.ui.requestPayload.set_value(request.content or '')

    def set_response(self, flow):
        if self.show_modified_response:
            response = flow.response
        else:
            response = flow.original_response

        self.ui.responseHeaders.set_header_line(response.get_header_line())
        self.ui.responseHeaders.set_headers(response.get_headers())
        self.ui.responseRaw.set_value(response.content or '')
        # if self.show_rendered:
        #     self.ui.responseRendered.set_value(response_body_rendered or '')

        self.ui.responseBodyPreview.setHtml(response.content_for_preview(), baseUrl=flow.request.get_url())

    def set_modified_dropdown(self, flow):
        if self.request_modified_dropdown:
            if flow.request_modified():
                self.request_modified_dropdown.setEnabled(True)
                self.request_modified_dropdown.setCurrentIndex(0)
            else:
                self.request_modified_dropdown.setEnabled(False)
                self.request_modified_dropdown.setCurrentIndex(1)

    @QtCore.Slot()
    def show_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.loaderWidget)

    @QtCore.Slot()
    def hide_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.responseTabs)
