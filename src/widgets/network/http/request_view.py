from PySide2 import QtCore, QtWidgets, QtWebChannel

from views._compiled.network.http.ui_request_view import Ui_RequestView
from widgets.shared.request_body_form import RequestBodyForm
from widgets.shared.request_headers_form import RequestHeadersForm

class RequestView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(RequestView, self).__init__(*args, **kwargs)
        self.ui = Ui_RequestView()
        self.ui.setupUi(self)

        self.request_headers_form = RequestHeadersForm('', {})
        self.request_body_form = RequestBodyForm('')

        show_modified_dropwon = QtWidgets.QComboBox()
        show_modified_dropwon.setContentsMargins(10, 10, 10, 10)
        show_modified_dropwon.insertItems(0, ['Modified', 'Original'])
        show_modified_dropwon.setObjectName('modifiedDropdown')
        self.ui.requestTabs.setCornerWidget(show_modified_dropwon)

    def clear_request(self):
        # self.ui.requestHeadersText.setPlainText('')
        self.ui.responseHeadersText.setPlainText('')

        self.ui.responseRaw.set_value('')
        self.ui.responseBodyModifiedText.setPlainText('')
        self.ui.responseBodyParsedText.setPlainText('')

        self.ui.responseBodyPreview.setHtml(None)

        # self.ui.headerTabs.setTabEnabled(3, False)
        self.ui.bodyTabs.setTabEnabled(1, False)

    def set_request(self, request):
        # Request Headers and body
        # self.request_headers_form = RequestHeadersForm(self.editor_item)
        self.ui.responseRaw.set_value(request.response_body)

        self.request_headers_form.set_header_line(request.get_request_header_line())
        self.request_headers_form.set_headers(request.get_request_headers())
        self.request_body_form.set_body(request.request_payload)

        self.ui.requestTabs.insertTab(0, self.request_headers_form, 'Request')
        self.ui.requestTabs.insertTab(1, self.request_body_form, 'Payload')

        try:
            if request.response_body is not None:
                self.ui.responseRaw.set_value(request.response_body)

            if request.response_body_rendered is not None:
                self.ui.responseBodyParsedText.setPlainText(request.response_body_rendered)

            self.ui.responseBodyPreview.setHtml(request.response_body_for_preview(), baseUrl=request.url())

        except ValueError:
            print(f'Warning: could not render response_body for request {request.id}')
            # self.ui.responseBodyRawCode.setHtml('')
            self.ui.responseBodyParsedText.setPlainText('')
            self.ui.responseBodyPreview.setHtml('', baseUrl=request.url())
