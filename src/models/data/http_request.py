from __future__ import annotations
import json
from urllib.parse import urlsplit
from typing import Optional, Any, TypedDict, cast
from orator import Model
from models.data.payload_file import PayloadFile, PayloadFileSerialised

from widgets.shared.headers_form import HeadersForm
from lib.types import Headers
from lib.input_parsing import parse_value, parse_headers, parse_payload_values

class FuzzFormData(TypedDict):
    payload_files: list[PayloadFileSerialised]
    fuzz_type: str
    delay_type: str

class FormData(TypedDict):
    method: str
    url: str
    headers: Headers
    content: str
    fuzz_data: Optional[FuzzFormData]

class HttpRequest(Model):
    __table__ = 'http_requests'
    __fillable__ = ['*']
    __casts__ = {'form_data': 'dict'}

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
    form_data: FormData

    FUZZ_TYPE_LABELS = ['One To One', 'Cartesian Product']
    FUZZ_TYPE_KEYS = ['one_to_one', 'cartesian']

    DELAY_TYPE_LABELS = ['Disabled', 'Fixed Time Delay', 'Random Time Delay']
    DELAY_TYPE_KEYS = ['disabled', 'fixed', 'random']

    # This is how requests are received from the proxy
    # TODO: Use a TypedDict instead of Any
    @classmethod
    def from_state(cls, state: dict[str, Any]) -> HttpRequest:
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

        url = request.get_url()
        request.form_data = {'method': request.method, 'url': url, 'headers': dict(state['headers']), 'content': request.content, 'fuzz_data': None}

        return request

    def set_blank_values_for_editor(self) -> None:
        self.http_version = 'HTTP/1.1'
        self.headers = None
        self.host = ''
        self.port = 80
        self.method = 'GET'
        self.scheme = 'http'
        self.path = ''
        self.content = ''
        self.form_data = {'method': 'GET', 'url': 'http://', 'headers': {}, 'content': '', 'fuzz_data': None}

    # TODO: Use a TypedDict instead of Any
    def get_state(self) -> dict[str, Any]:
        attributes = self.serialize()
        attributes['headers'] = json.loads(attributes['headers'])
        return attributes

    def set_headers(self, headers: Headers) -> None:
        self.headers = json.dumps(headers)

    def get_headers(self) -> Optional[Headers]:
        if self.headers is None:
            return None
        return json.loads(self.headers)

    def get_header_line_no_http_version(self) -> str:
        return f'{self.method} {self.path}'

    def get_header_line(self) -> str:
        return f'{self.method} {self.path} {self.http_version}'

    def get_url(self) -> str:
        if self.port not in [80, 443, None]:
            port = ':' + str(self.port)
        else:
            port = ''

        return f'{self.scheme}://{self.host}{port}{self.path}'

    def duplicate(self) -> HttpRequest:
        new_request = HttpRequest()

        new_request.http_version = self.http_version
        new_request.headers = self.headers
        new_request.content = getattr(self, 'content', None)
        new_request.trailers = getattr(self, 'trailers', None)
        new_request.host = self.host
        new_request.port = self.port
        new_request.method = self.method
        new_request.scheme = self.scheme
        new_request.authority = getattr(self, 'authority', None)
        new_request.path = self.path

        form_data = getattr(self, 'form_data', None)

        if form_data is None:
            new_request.form_data = self.generate_form_data()
        else:
            new_request.form_data = self.form_data

        return new_request

    def overwrite_calculated_headers(self) -> None:
        calc_text = HeadersForm.CALCULATED_TEXT
        headers = self.get_headers()

        if headers is None:
            return

        if headers.get('Host'):
            headers['Host'] = calc_text

        if headers.get('Content-Length'):
            headers['Content-Length'] = calc_text

        self.set_headers(headers)

    def apply_payload_values(self, payload_values: dict[str, str]) -> None:
        method = parse_payload_values(str(self.form_data['method']), payload_values)
        url = parse_payload_values(str(self.form_data['url']), payload_values)
        content = parse_payload_values(str(self.form_data['content']), payload_values)

        # TODO:
        headers = self.form_data['headers']

        self.set_form_data({
            'method': method,
            'url': url,
            'headers': headers,
            'content': content,
            'fuzz_data': None
        })
        return

    def reset_form_data(self) -> None:
        self.set_form_data(self.form_data)

    def set_form_data(self, form_data: FormData) -> None:
        self.form_data = form_data

        # 1. Set method
        self.method = str(self.form_data['method'])

        # 2. Set URL related attributes
        parsed_url = parse_value(str(self.form_data['url']))
        url_data = urlsplit(parsed_url)
        if url_data.hostname:
            self.host = url_data.hostname

        if url_data.port:
            self.port = url_data.port
        self.scheme = url_data.scheme

        if url_data.query == '':
            self.path = url_data.path
        else:
            self.path = url_data.path + '?' + url_data.query

        # 3. Set content
        self.content = parse_value(str(form_data['content']))

        # 4. Set headers
        parsed_headers = parse_headers(cast(Headers, form_data['headers']))
        self.set_headers(parsed_headers)

    def save(self, *args, **kwargs):
        return super(HttpRequest, self).save(*args, **kwargs)

    def generate_form_data(self) -> FormData:
        headers = self.get_headers() or {}
        content = self.content or ''

        return {
            'method': self.method,
            'url': self.get_url(),
            'headers': headers,
            'content': content,
            'fuzz_data': None
        }

    def fuzz_data(self) -> Optional[FuzzFormData]:
        return self.form_data.get('fuzz_data')

    def payload_files(self) -> list[PayloadFile]:
        fuzz_data = self.fuzz_data()

        if fuzz_data is None:
            return []

        return [PayloadFile.from_serialised(p) for p in fuzz_data['payload_files']]
