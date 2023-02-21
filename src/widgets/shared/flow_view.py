import json
from typing import Optional
# from html5print import HTMLBeautifier
from bs4 import BeautifulSoup
from PyQt6 import QtWidgets
from PyQt6 import QtCore, QtGui
from entities.http_flow import HttpFlow
from entities.http_response import HttpResponse

from views._compiled.shared.flow_view import Ui_FlowView
from lib.types import Headers, get_content_type
from lib.utils import get_status_colour, get_status_colour_bright
from widgets.shared.code_editor import CodeEditor
from constants import HTTP_STATUS_CODE_DESCRIPTIONS

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

        # Setup Request Corner Widget:
        self.request_modified_dropdown = QtWidgets.QComboBox()
        self.request_modified_dropdown.setContentsMargins(10, 10, 10, 10)
        self.request_modified_dropdown.insertItems(0, ['Modified', 'Original'])
        self.request_modified_dropdown.setObjectName('modifiedDropdown')
        self.request_modified_dropdown.currentIndexChanged.connect(self.show_modified_request_change)

        self.ui.requestTabs.setCornerWidget(self.request_modified_dropdown)
        self.ui.requestTabs.removeTab(2)

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

        self.response_status_label = QtWidgets.QLabel()
        self.response_status_label.setObjectName("responseStatusLabel")

        self.response_corner_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(self.response_corner_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.response_status_label)
        layout.addWidget(self.response_format_dropdown)
        layout.addWidget(self.response_modified_dropdown)
        layout.addWidget(self.save_example_button)

        self.ui.responseTabs.setCornerWidget(self.response_corner_widget)

        # Headers
        self.ui.requestHeaders.headers_changed.connect(self.update_syntax_highlighting_for_request)
        self.ui.responseHeaders.set_editable(False)

    def set_request_editable(self, editable):
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

    def show_modified_request_change(self, index: int):
        if index == 0:  # Modified
            self.show_modified_request = True
        elif index == 1:  # Original
            self.show_modified_request = False

        self.set_request(self.flow)

    def show_modified_response_change(self, index: int):
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

    def set_flow(self, flow: HttpFlow):
        self.flow = flow
        self.set_modified_dropdown(flow)
        self.set_request(flow)
        self.set_response(flow)

        self.ui.requestBody.set_flow(flow)

    def set_request(self, flow: HttpFlow):
        request = flow.request

        if flow.request_modified() and not self.show_modified_request and flow.original_request is not None:
            request = flow.original_request

        self.ui.requestHeaders.set_header_line(request.get_header_line())
        if request.form_data['headers']:
            self.ui.requestHeaders.set_headers(request.form_data['headers'])
        else:
            self.ui.requestHeaders.set_default_headers()

        # Don't use a formatter if this is an editor request becuase the request body will have been written by the user
        self.set_request_format_from_headers(request.headers)
        self.ui.requestBody.set_auto_format_enabled(flow.is_type_proxy())
        self.ui.requestBody.set_value(request.form_data['content'] or '')

    # Automatically change the syntax highlighting based on the Content-Type header (request editor only)
    def update_syntax_highlighting_for_request(self):
        if self.flow.is_type_editor():
            self.set_request_format_from_headers(self.ui.requestHeaders.get_headers())
            # Hack to force CodeEditor and Scintilla to redraw itself and therefore show syntax highlighting
            self.ui.requestBody.set_value(self.ui.requestBody.get_value())

    # Requires the flow,request and response to be saved to the DB (used by the network page)
    def set_response(self, flow: HttpFlow):
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
            return

        self.ui.responseHeaders.set_header_line(response.get_header_line())
        self.ui.responseHeaders.set_headers(response.get_headers())
        self.__display_response_body(response, response.get_format())

    def __display_response_body(self, response: HttpResponse, format: Optional[str] = None):
        # Determine the format and update the dropdown
        if format is None:
            self.ui.responseRaw.clear_formatting()
            self.response_format_dropdown.setCurrentIndex(len(CodeEditor.FORMATS) - 1)
        else:
            self.ui.responseRaw.set_format(format)
            index = CodeEditor.FORMATS.index(format)
            self.response_format_dropdown.setCurrentIndex(index)

        # self.set_response_format_from_headers(response.get_headers() or Headers())
        self.ui.responseRaw.set_auto_format_enabled(True)
        self.set_response_status_label(response)

        # Set the response body value
        if format == 'Hex':
            content = response.content_hex()
            self.ui.responseRaw.set_value(content)
            self.ui.responseBodyStack.setCurrentIndex(0) # Show CodeEditor
        elif format == 'Image':
            if response.content is None:
                return
            self.ui.responseBodyStack.setCurrentIndex(1) # Show Image view

            qbytes = QtCore.QByteArray()
            qbytes.append(response.content)
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(qbytes)

            if pixmap.width() > 400 or pixmap.height() > 400:
                pixmap = pixmap.scaled(400, 400, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

            self.ui.responseImg.clear()
            self.ui.responseImg.setPixmap(pixmap)
            self.ui.responseImg.show()
        else:
            content = response.content_for_preview()
            self.ui.responseRaw.set_value(content)
            self.ui.responseBodyStack.setCurrentIndex(0) # Show CodeEditor

    def set_response_status_label(self, response: HttpResponse):
        status = str(response.status_code)

        if response.reason is None or response.reason == "":
            label_msg = " " + HTTP_STATUS_CODE_DESCRIPTIONS[status]
        else:
            label_msg = " " + response.reason

        bg_color = get_status_colour_bright(response.status_code)
        self.response_status_label.setStyleSheet(f"background-color: {bg_color};")
        self.response_status_label.setText(status + label_msg)

    # In the request editor the header line is based off of the url input + method dropdown, so when
    # those values change we need to update the header line too
    def refresh_header_line(self):
        request = self.flow.request
        self.ui.requestHeaders.set_header_line(request.get_header_line())

    def show_real_request(self):
        request = self.flow.request

        self.ui.requestHeaders.set_header_line(request.get_header_line())
        headers = request.get_headers()

        if headers:
            self.ui.requestHeaders.set_headers(request.get_headers())

        self.ui.requestBody.set_value(request.content or '')

    # This method does not need the response to be saved to the DB:
    def set_response_from_editor(self, response: HttpResponse):
        self.editor_response = response
        self.ui.responseHeaders.set_header_line(response.get_header_line())
        self.ui.responseHeaders.set_headers(response.get_headers())
        self.set_response_status_label(response)
        self.__display_response_body(response, response.get_format())

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
        self.ui.responseStackedWidget.setCurrentWidget(self.ui.loaderWidget)

    def hide_loader(self):
        self.ui.responseStackedWidget.setCurrentWidget(self.ui.responseTabs)

    def change_response_body_format(self, index):
        format = CodeEditor.FORMATS[index]
        self.ui.responseRaw.set_format(format)

        if self.flow.response:
            self.__display_response_body(self.flow.response, format)
        else:
            # TODO: The editor should just create an HttpResponse that isn't saved and pass it to FlowView
            self.__display_response_body(self.editor_response, format)

    def set_request_format_from_headers(self, headers: Headers):
        format = get_content_type(headers)
        if format is None:
            self.ui.requestBody.clear_formatting()
            return

        self.ui.requestBody.set_format(format)
