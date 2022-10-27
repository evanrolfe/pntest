from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from urllib.parse import urlsplit
import json
from typing import Any, Optional, TypedDict
from lib.types import Headers
from models.data.payload_file import PayloadFile, PayloadFileSerialised
from models.model import Model

from constants import CALCULATED_TEXT
from lib.types import Headers
from lib.input_parsing.text_wrapper import parse_text, parse_text_with_payload_values
from copy import deepcopy
from proxy.common_types import ProxyRequest

def escape_quotes(value: str) -> str:
    return value.replace('"', r'\"')

class FuzzFormData(TypedDict):
    payload_files: list[PayloadFileSerialised]
    fuzz_type: str
    delay_type: str
    delay_secs: Optional[str]
    delay_secs_min: Optional[str]
    delay_secs_max: Optional[str]

class FormData(TypedDict):
    method: str
    url: str
    headers: Headers
    content: str
    fuzz_data: Optional[FuzzFormData]

@dataclass(kw_only=True)
class HttpRequest(Model):
    # Columns
    id: int = field(init=False, default=0)
    http_version: str
    headers: Headers
    content: Optional[str] = None
    trailers: Optional[str] = None
    timestamp_start: Optional[float] = None
    timestamp_end: Optional[float] = None
    host: str
    port: int
    method: str
    scheme: str
    authority: Optional[str] = None
    path: str
    form_data: FormData
    created_at: int

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": ["headers", "form_data"]
    }

    # This is how requests are received from the proxy
    # TODO: Use a TypedDict instead of Any
    # TODO: Fix url value in form_data
    @classmethod
    def from_state(cls, state: ProxyRequest) -> HttpRequest:
        request = HttpRequest(
            http_version = state['http_version'],
            headers = dict(state['headers']),
            content = state['content'],
            trailers = state['trailers'],
            timestamp_start = state['timestamp_start'],
            timestamp_end = state['timestamp_end'],
            host = state['host'],
            port = state['port'],
            method = state['method'],
            scheme = state['scheme'],
            authority = state['authority'],
            path = state['path'],
            form_data = {'method': state['method'], 'url': 'TODO-URL', 'headers': dict(state['headers']), 'content': state['content'], 'fuzz_data': None},
            created_at= 1,
        )

        return request

    # TODO: Use a TypedDict instead of Any
    # TODO: Make this work
    def get_state(self) -> dict[str, Any]:
        # attributes = self.serialize()
        # attributes['headers'] = json.loads(attributes['headers'])
        return {}

    def set_blank_values_for_editor(self) -> None:
        self.http_version = 'HTTP/1.1'
        self.headers = {}
        self.host = ''
        self.port = 80
        self.method = 'GET'
        self.scheme = 'http'
        self.path = ''
        self.content = ''
        self.form_data = {'method': 'GET', 'url': 'http://', 'headers': {}, 'content': '', 'fuzz_data': None}

    def set_headers(self, headers: Headers) -> None:
        self.headers = headers

    def get_headers(self) -> Headers:
        return self.headers

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
        new_request = HttpRequest(
            http_version = self.http_version,
            headers = self.headers,
            content = self.content,
            trailers = self.trailers,
            host = self.host,
            port = self.port,
            method = self.method,
            scheme = self.scheme,
            authority = self.authority,
            path = self.path,
            form_data = self.form_data or self.generate_form_data(),
            created_at = 1,
        )

        return new_request

    def modify(self, modified_method: str, modified_path: str, modified_headers: Headers, modified_content: str):
        self.method = modified_method
        self.path = modified_path
        self.headers = modified_headers
        self.content = modified_content

        if modified_headers.get('Host'):
            host, port = self.__get_host_and_port(modified_headers['Host'])
            self.host = host
            if port:
                self.port = port
        elif modified_headers.get('host'):
            # TODO: DRY up this duplication
            host, port = self.__get_host_and_port(modified_headers['Host'])
            self.host = host
            if port:
                self.port = port

    def overwrite_calculated_headers(self) -> None:
        calc_text = CALCULATED_TEXT
        headers = self.get_headers()

        if headers is None:
            return

        if headers.get('Host'):
            headers['Host'] = calc_text

        if headers.get('Content-Length'):
            headers['Content-Length'] = calc_text

        self.set_headers(headers)

    def apply_payload_values(self, payload_values: dict[str, str]) -> None:
        method = parse_text_with_payload_values(str(self.form_data['method']), payload_values)
        url = parse_text_with_payload_values(str(self.form_data['url']), payload_values)
        content = parse_text_with_payload_values(str(self.form_data['content']), payload_values)

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
        parsed_url = parse_text(str(self.form_data['url']))
        url_data = urlsplit(parsed_url)
        if url_data.hostname:
            self.host = url_data.hostname

        if url_data.port:
            self.port = url_data.port
        else:
            if url_data.scheme == "https":
                self.port = 443
            else:
                self.port = 80

        self.scheme = url_data.scheme

        if url_data.query == '':
            self.path = url_data.path
        else:
            self.path = url_data.path + '?' + url_data.query

        # 3. Set content
        self.content = parse_text(str(form_data['content']))

        # 4. Set headers
        parsed_headers = deepcopy(form_data['headers'])
        for key, value in form_data['headers'].items():
            parsed_headers[key] = parse_text(value)

        self.set_headers(parsed_headers)

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

    def payload_keys(self) -> list[str]:
        fuzz_data = self.fuzz_data()

        if fuzz_data is None:
            return []

        return [p['key'] for p in fuzz_data['payload_files']]

    def get_curl_command(self) -> str:
        headers_dict = self.get_headers()
        headers = ""

        if headers_dict is not None:
            headers = ['"{0}: {1}"'.format(k, escape_quotes(v)) for k, v in headers_dict.items() if v != CALCULATED_TEXT]
            headers = " -H ".join(headers)

        content = getattr(self, 'content', None)
        if content is None or content == "":
            return f"curl -X {self.method} -H {headers} \"{self.get_url()}\""
        else:
            return f"curl -X {self.method} -H {headers} -d {content}' {self.get_url()}"

    def __eq__(self, other) -> bool:
        return (
            self.method == other.method and
            self.host == other.host and
            self.port == other.port and
            self.path == other.path and
            self.headers == other.headers and
            self.content == other.content
        )

    def __get_host_and_port(self, host: str) -> tuple[str, Optional[int]]:
        host_arr = host.split(':')
        if len(host_arr) == 2:
            return (host_arr[0], int(host_arr[1]))
        else:
            return [host_arr[0], None] # type: ignore
