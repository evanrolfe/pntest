from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from typing import Any, Optional
from requests import Response as RequestsResponse
from lib.types import Headers
from models.model import Model
from proxy.common_types import ProxyResponse
from lib.types import Headers

@dataclass(kw_only=True)
class HttpResponse(Model):
    # Columns
    id: int = field(init=False, default=0)
    created_at: int = field(init=False, default=0)

    http_version: str
    headers: Headers
    content: Optional[str]
    timestamp_start: float
    timestamp_end: float
    status_code: int
    reason: Optional[str]

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": ["headers"],
        "do_not_save_keys": [],
    }

    @classmethod
    def from_state(cls, state: ProxyResponse) -> HttpResponse:
        return HttpResponse(
            http_version = state['http_version'],
            headers = dict(state['headers']),
            content = state['content'],
            timestamp_start = state['timestamp_start'],
            timestamp_end = state['timestamp_end'],
            status_code = state['status_code'],
            reason = state['reason'],
        )
    @classmethod
    def from_requests_response(cls, response: RequestsResponse) -> HttpResponse:
        version = 'Unknown'
        if response.raw.version == 11:
            version = 'HTTP/1.1'
        elif response.raw.version == 10:
            version = 'HTTP/1.0'

        return HttpResponse(
            content = response.text,
            status_code = response.status_code,
            reason = response.reason,
            headers=dict(response.headers),
            http_version=version,
            timestamp_start=1.0,
            timestamp_end=2.0,
        )

    def duplicate(self) -> HttpResponse:
        return HttpResponse(
            http_version = self.http_version,
            headers = self.headers,
            content = self.content,
            status_code = self.status_code,
            reason = self.reason,
            timestamp_start=1.0,
            timestamp_end=2.0,
        )

    def modify(self, modified_status_code: int, modified_headers: Headers, modified_content: str):
        self.status_code = modified_status_code
        self.headers = modified_headers
        self.content = modified_content

    # TODO: Use a TypedDict instead of Any
    # TODO: Make this work
    def get_state(self) -> dict[str, Any]:
        # attributes = self.serialize()
        # attributes['headers'] = json.loads(attributes['headers'])
        return {}

    def set_headers(self, headers: Headers) -> None:
        self.headers = headers

    def get_headers(self) -> Headers:
        return self.headers

    def get_header_line(self) -> str:
        return f'{self.http_version} {self.status_code} {self.reason}'

    def get_header_line_no_http_version(self) -> str:
        return f'{self.status_code} {self.reason}'

    def content_for_preview(self) -> str:
        return self.content or ''

    def __eq__(self, other) -> bool:
        return (
            self.headers == other.headers and
            self.content == other.content and
            self.status_code == other.status_code
        )
