from PySide2 import QtWidgets

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

        # Disable modified tabs to start with:
        # self.ui.headerTabs.setTabEnabled(1, False)
        # self.ui.headerTabs.setTabEnabled(3, False)

        # self.highlighter = HtmlHighlighter(self.ui.responseBodyRawText.document())
        # self.ui.bodyTab.setCurrentWidget(self.ui.responseBodyWebview)

    def clear_request(self):
        # self.ui.requestHeadersText.setPlainText('')
        self.ui.responseHeadersText.setPlainText('')

        self.ui.responseBodyRawText.setPlainText('')
        self.ui.responseBodyModifiedText.setPlainText('')
        self.ui.responseBodyParsedText.setPlainText('')

        self.ui.responseBodyPreview.setHtml(None)

        # self.ui.headerTabs.setTabEnabled(3, False)
        self.ui.bodyTabs.setTabEnabled(1, False)

    def set_request(self, request):
        # Request Headers and body
        # self.request_headers_form = RequestHeadersForm(self.editor_item)
        self.request_headers_form.set_header_line(request.get_request_header_line())
        self.request_headers_form.set_headers(request.get_request_headers())
        self.request_body_form.set_body(request.request_payload)

        self.ui.requestTabs.insertTab(0, self.request_headers_form, 'Headers')
        self.ui.requestTabs.insertTab(1, self.request_body_form, 'Body')

        try:
            if request.response_body is not None:
                self.ui.responseBodyRawText.setPlainText(request.response_body)

            if request.modified_response_body is not None:
                self.ui.responseBodyModifiedText.setPlainText(request.modified_response_body)

            if request.response_body_rendered is not None:
                self.ui.responseBodyParsedText.setPlainText(request.response_body_rendered)

            self.ui.responseBodyPreview.setHtml(request.response_body_for_preview(), baseUrl=request.url())

        except ValueError:
            print(f'Warning: could not render response_body for request {request.id}')
            self.ui.responseBodyRawText.setPlainText('')
            self.ui.responseBodyModifiedText.setPlainText('')
            self.ui.responseBodyParsedText.setPlainText('')
            self.ui.responseBodyPreview.setHtml('', baseUrl=request.url())

        # Request modified tab:
        if request.request_modified is True:
            # self.ui.headerTabs.setTabEnabled(1, True)
            self.ui.requestHeadersModifiedText.setPlainText(request.request_headers_modified_parsed())
        # else:
            # self.ui.headerTabs.setTabEnabled(1, False)

        # Response modified tab:
        if request.response_modified is True:
            # self.ui.headerTabs.setTabEnabled(3, True)
            self.ui.bodyTabs.setTabEnabled(1, True)
            self.ui.responseHeadersModifiedText.setPlainText(request.response_headers_modified_parsed())
        else:
            # self.ui.headerTabs.setTabEnabled(3, False)
            self.ui.bodyTabs.setTabEnabled(1, False)
