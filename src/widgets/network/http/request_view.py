from PySide2 import QtWidgets

from views._compiled.network.http.ui_request_view import Ui_RequestView

class RequestView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(RequestView, self).__init__(*args, **kwargs)
        self.ui = Ui_RequestView()
        self.ui.setupUi(self)

        show_modified_dropwon = QtWidgets.QComboBox()
        show_modified_dropwon.setContentsMargins(10, 10, 10, 10)
        show_modified_dropwon.insertItems(0, ['Modified', 'Original'])
        show_modified_dropwon.setObjectName('modifiedDropdown')
        self.ui.requestTabs.setCornerWidget(show_modified_dropwon)

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
        # Request:
        self.ui.requestHeaders.set_header_line(request.get_request_header_line())
        self.ui.requestHeaders.set_headers(request.get_request_headers())
        self.ui.requestPayload.set_value(request.request_payload or '')

        # Response:
        self.ui.responseRaw.set_value(request.response_body or '')
        self.ui.responseRendered.set_value(request.response_body_rendered or '')
        self.ui.responseBodyPreview.setHtml(request.response_body_for_preview(), baseUrl=request.url())
