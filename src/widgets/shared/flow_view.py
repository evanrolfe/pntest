import json
# from html5print import HTMLBeautifier
from bs4 import BeautifulSoup
from PyQt6 import QtWidgets
from PyQt6 import QtCore

from views._compiled.shared.flow_view import Ui_FlowView
from lib.types import Headers
from widgets.shared.code_editor import CodeEditor

class FlowView(QtWidgets.QWidget):
    save_example_clicked = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(FlowView, self).__init__(*args, **kwargs)
        self.ui = Ui_FlowView()
        self.ui.setupUi(self)
        self.request_modified_dropdown = None
        self.response_modified_dropdown = None
        self.show_modified_request = False
        self.show_modified_response = False
        self.editable = False
        self.selected_format = CodeEditor.FORMATS[len(CodeEditor.FORMATS) - 1]

        # Setup Request Corner Widget:
        self.request_modified_dropdown = QtWidgets.QComboBox()
        self.request_modified_dropdown.setContentsMargins(10, 10, 10, 10)
        self.request_modified_dropdown.insertItems(0, ['Modified', 'Original'])
        self.request_modified_dropdown.setObjectName('modifiedDropdown')
        self.request_modified_dropdown.currentIndexChanged.connect(self.show_modified_request_change)

        self.ui.requestTabs.setCornerWidget(self.request_modified_dropdown)

        # Setup Response Corner Widget:
        self.response_modified_dropdown = QtWidgets.QComboBox()
        self.response_modified_dropdown.setContentsMargins(10, 10, 10, 10)
        self.response_modified_dropdown.insertItems(0, ['Modified', 'Original'])
        self.response_modified_dropdown.setObjectName('responseModifiedDropdown')
        self.response_modified_dropdown.setCurrentIndex(0)
        self.response_modified_dropdown.currentIndexChanged.connect(self.show_modified_response_change)

        self.response_format_dropdown = QtWidgets.QComboBox()
        self.response_format_dropdown.setContentsMargins(10, 10, 10, 10)
        self.response_format_dropdown.insertItems(0, CodeEditor.FORMATS)
        self.response_format_dropdown.setObjectName('responseFormatDropdown')
        self.response_format_dropdown.setCurrentIndex(len(CodeEditor.FORMATS) - 1)
        self.response_format_dropdown.currentIndexChanged.connect(self.change_response_body_format)

        self.save_example_button = QtWidgets.QPushButton('Save as Example')
        self.save_example_button.setObjectName('saveAsExample')
        self.save_example_button.setEnabled(False)

        self.response_corner_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(self.response_corner_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.response_format_dropdown)
        layout.addWidget(self.response_modified_dropdown)
        layout.addWidget(self.save_example_button)

        self.ui.responseTabs.setCornerWidget(self.response_corner_widget)

    def set_editable(self, editable):
        self.editable = editable
        self.ui.requestHeaders.set_editable(editable)

    def set_show_rendered(self, show_rendered):
        if show_rendered is False:
            self.ui.responseTabs.removeTab(2)

        self.show_rendered = show_rendered

    def show_modified_dropdown(self):
        self.show_modified_request = True
        self.show_modified_response = True

    def set_save_as_example_visible(self, visible):
        self.save_example_button.setVisible(visible)

    def set_save_as_example_enabled(self, enabled):
        self.save_example_button.setEnabled(enabled)

    def show_modified_request_change(self, index):
        if index == 0:  # Modified
            self.show_modified_request = True
        elif index == 1:  # Original
            self.show_modified_request = False

        self.set_request(self.flow)

    def show_modified_response_change(self, index):
        if index == 0:  # Modified
            self.show_modified_response = True
        elif index == 1:  # Original
            self.show_modified_response = False

        self.set_response(self.flow)

    def get_request_headers(self) -> Headers:
        return self.ui.requestHeaders.get_headers()

    def get_request_payload(self) -> str:
        return self.ui.requestBody.get_value()

    def clear_request(self):
        # Request:
        self.ui.requestHeaders.set_header_line('')
        self.ui.requestHeaders.set_headers({})
        self.ui.requestBody.set_value('')

        # Response:
        self.ui.responseRaw.set_value('')
        self.ui.responseRendered.set_value('')
        # self.ui.responseBodyPreview.setHtml('')

    def set_flow(self, flow):
        self.flow = flow
        self.set_modified_dropdown(flow)
        self.set_request(flow)
        self.set_response(flow)

    def set_request(self, flow):
        if self.show_modified_request and flow.request_modified():
            request = flow.request
        elif not self.show_modified_request and flow.request_modified():
            request = flow.original_request
        else:
            request = flow.request

        self.ui.requestHeaders.set_header_line(request.get_header_line())
        if request.form_data['headers']:
            self.ui.requestHeaders.set_headers(request.form_data['headers'])
        else:
            self.ui.requestHeaders.set_default_headers()
        self.ui.requestBody.set_value(request.form_data['content'] or '')

    # Requires the flow,request and response to be saved to the DB (used by the network page)
    def set_response(self, flow):
        if self.show_modified_response and flow.response_modified():
            response = flow.response
        elif not self.show_modified_response and flow.response_modified():
            response = flow.original_response
        else:
            response = flow.response

        if not response:
            self.ui.responseHeaders.set_header_line('')
            self.ui.responseHeaders.set_headers(None)
            self.ui.responseRaw.set_value('')
            # self.ui.responseBodyPreview.setHtml('')
            return

        self.ui.responseHeaders.set_header_line(response.get_header_line())
        self.ui.responseHeaders.set_headers(response.get_headers())

        self.set_format_from_headers(response.get_headers())
        formatted_content = self.format_text(response.content)
        self.ui.responseRaw.set_value(formatted_content or '', self.selected_format)
        # if self.show_rendered:
        #     self.ui.responseRendered.set_value(response_body_rendered or '')
        headers = flow.response.get_headers()
        content_type = headers.get('Content-Type', '')
        mime_type = content_type.split(';')[0]
        print(f"--------------> mime type received is: {mime_type}")
        # if 'html' in content_type:
        #     self.ui.responseBodyPreview.setHtml(response.content_for_preview(), baseUrl=flow.request.get_url())
        # else:
        #     self.ui.responseBodyPreview.setHtml('')

    def show_real_request(self):
        request = self.flow.request

        self.ui.requestHeaders.set_header_line(request.get_header_line())
        headers = request.get_headers()

        if headers:
            self.ui.requestHeaders.set_headers(request.get_headers())

        self.ui.requestBody.set_value(request.content or '')

    # This method does not need the response to be saved to the DB:
    def set_response_from_editor(self, response):
        self.editor_response = response
        self.ui.responseHeaders.set_header_line(response.get_header_line())
        self.ui.responseHeaders.set_headers(response.get_headers())

        self.set_format_from_headers(response.get_headers())
        formatted_content = self.format_text(response.content)
        self.ui.responseRaw.set_value(formatted_content or '', self.selected_format)

        headers = response.get_headers()
        content_type = headers.get('Content-Type', '')
        # mime_type = content_type.split(';')[0]

        # if 'html' in content_type:
        #     self.ui.responseBodyPreview.setHtml(response.content_for_preview(), baseUrl=self.flow.request.get_url())
        # else:
        #     self.ui.responseBodyPreview.setHtml('')

    def set_modified_dropdown(self, flow):
        if self.request_modified_dropdown is None:
            return

        self.request_modified_dropdown.setCurrentIndex(0)
        self.request_modified_dropdown.setVisible(flow.request_modified())

        if self.response_modified_dropdown is None:
            return

        self.response_modified_dropdown.setCurrentIndex(0)
        self.response_modified_dropdown.setVisible(flow.response_modified())

    def show_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.loaderWidget)

    def hide_loader(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.responseTabs)

    def change_response_body_format(self, index):
        self.selected_format = CodeEditor.FORMATS[index]

        if self.flow.response:
            content = self.flow.response.content
        else:
            content = self.editor_response.content

        formatted_content = self.format_text(content)
        self.ui.responseRaw.set_value(formatted_content, self.selected_format)

    def format_text(self, text):
        # TODO: Format javascript
        if self.selected_format == 'JSON':
            try:
                formatted_content = json.dumps(json.loads(text), indent=2)
            except json.decoder.JSONDecodeError:
                formatted_content = text
        elif self.selected_format == 'XML':
            formatted_content = BeautifulSoup(text, 'xml.parser').prettify()
        elif self.selected_format == 'HTML':
            formatted_content = BeautifulSoup(text, 'html.parser').prettify()
        else:
            formatted_content = text

        return formatted_content

    def set_format_from_headers(self, headers):
        lower_case_headers = {k.lower(): v for k, v in headers.items()}
        content_type = lower_case_headers.get('content-type')

        if content_type is None:
            self.selected_format = 'Unformatted'
        elif 'json' in content_type:
            self.selected_format = 'JSON'
        elif 'xml' in content_type:
            self.selected_format = 'XML'
        elif 'html' in content_type:
            self.selected_format = 'HTML'
        elif 'javascript' in content_type:
            self.selected_format = 'Javascript'
        else:
            self.selected_format = 'Unformatted'

        index = CodeEditor.FORMATS.index(self.selected_format)
        self.response_format_dropdown.setCurrentIndex(index)
