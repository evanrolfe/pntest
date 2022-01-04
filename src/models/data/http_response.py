from __future__ import annotations
import json
from typing import Optional, Any
from orator import Model

Headers = dict[str, str]

class HttpResponse(Model):
    __table__ = 'http_responses'
    __fillable__ = ['*']

    id: int
    http_version: str
    headers: str
    content: Optional[str]
    timestamp_start: float
    timestamp_end: float
    status_code: int
    reason: Optional[str]
    created_at: int
    updated_at: Optional[int]

    @classmethod
    def from_state(cls, state) -> HttpResponse:
        response = HttpResponse()

        response.http_version = state['http_version']
        response.headers = json.dumps(dict(state['headers']))
        response.content = state['content']
        response.timestamp_start = state['timestamp_start']
        response.timestamp_end = state['timestamp_end']
        response.status_code = state['status_code']
        response.reason = state['reason']

        return response

    @classmethod
    # TODO: Set the requests_response type to one from the proxy package
    def from_requests_response(cls, requests_response: Any) -> HttpResponse:
        response_model = HttpResponse()
        response_model.content = requests_response.text
        response_model.status_code = requests_response.status_code
        response_model.reason = requests_response.reason
        response_model.set_headers(dict(requests_response.headers))

        if requests_response.raw.version == 11:
            response_model.http_version = 'HTTP/1.1'
        elif requests_response.raw.version == 10:
            response_model.http_version = 'HTTP/1.0'

        return response_model

    def duplicate(self) -> HttpResponse:
        new_response = HttpResponse()

        new_response.http_version = self.http_version
        new_response.headers = self.headers
        new_response.content = self.content
        new_response.status_code = self.status_code
        new_response.reason = self.reason

        return new_response

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

    def get_header_line(self) -> str:
        return f'{self.http_version} {self.status_code} {self.reason}'

    def get_header_line_no_http_version(self) -> str:
        return f'{self.status_code} {self.reason}'

    def content_for_preview(self) -> str:
        return self.content or ''
