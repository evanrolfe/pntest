import json
from typing import Optional
from orator import Model

from widgets.shared.headers_form import HeadersForm

class HttpRequest(Model):
    __table__ = 'http_requests'
    __fillable__ = ['*']

    id: int
    http_version: str
    headers: Optional[str]
    content: Optional[str]
    trailers: Optional[str]
    timestamp_start: float
    timestamp_end: float
    host: str
    port: int
    method: str
    scheme: str
    authority: Optional[str]
    path: str
    created_at: int
    updated_at: int

    @classmethod
    def from_state(cls, state):
        request = HttpRequest()
        request.http_version = state['http_version']
        request.headers = json.dumps(dict(state['headers']))
        request.content = state['content']
        request.trailers = state['trailers']
        request.timestamp_start = state['timestamp_start']
        request.timestamp_end = state['timestamp_end']
        request.host = state['host']
        request.port = state['port']
        request.method = state['method']
        request.scheme = state['scheme']
        request.authority = state['authority']
        request.path = state['path']

        return request

    def set_blank_values_for_editor(self):
        self.http_version = 'HTTP/1.1'
        self.headers = None
        self.host = ''
        self.port = 80
        self.method = 'GET'
        self.scheme = 'http'
        self.path = ''
        self.content = ''

    def get_state(self):
        attributes = self.serialize()
        attributes['headers'] = json.loads(attributes['headers'])
        return attributes

    def set_headers(self, headers):
        self.headers = json.dumps(headers)

    def get_headers(self):
        if self.headers is None:
            return None
        return json.loads(self.headers)

    def get_header_line_no_http_version(self):
        return f'{self.method} {self.path}'

    def get_header_line(self):
        return f'{self.method} {self.path} {self.http_version}'

    def get_url(self):
        if self.port not in [80, 443, None]:
            port = ':' + str(self.port)
        else:
            port = ''

        return f'{self.scheme}://{self.host}{port}{self.path}'

    def duplicate(self):
        new_request = HttpRequest()

        new_request.http_version = self.http_version
        new_request.headers = self.headers
        new_request.content = self.content
        new_request.trailers = self.trailers
        new_request.host = self.host
        new_request.port = self.port
        new_request.method = self.method
        new_request.scheme = self.scheme
        new_request.authority = self.authority
        new_request.path = self.path

        return new_request

    def overwrite_calculated_headers(self):
        calc_text = HeadersForm.CALCULATED_TEXT
        headers = self.get_headers()

        if headers.get('Host'):
            headers['Host'] = calc_text

        if headers.get('Content-Length'):
            headers['Content-Length'] = calc_text

        self.set_headers(headers)
