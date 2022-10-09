from dataclasses import dataclass
from dataclasses import field

from typing import Any, Optional
from models.client import Client
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from models.websocket_message import WebsocketMessage
from models.model import Model

@dataclass(kw_only=True)
class HttpFlow(Model):
    # Columns
    id: int = field(init=False, default=0)
    uuid: Optional[str] = None
    client_id: Optional[int] = None
    type: str
    title: Optional[str] = None
    request_id: Optional[int] = None
    original_request_id: Optional[int] = None
    response_id: Optional[int] = None
    original_response_id: Optional[int] = None
    http_flow_id: Optional[int] = None
    created_at: int

    # Relations
    client: Optional[Client] = None
    request: Optional[HttpRequest] = None
    original_request: Optional[HttpRequest] = None
    response: Optional[HttpResponse] = None
    original_response: Optional[HttpResponse] = None
    websocket_messages: list[WebsocketMessage] = field(default_factory=lambda: [])

    meta = {
        "relationship_keys": ["client", "request", "original_request", "response", "original_response", "websocket_messages"]
    }

    TYPE_PROXY = 'proxy'
    TYPE_EDITOR = 'editor'
    TYPE_EDITOR_EXAMPLE = 'editor_example'
    TYPE_EDITOR_FUZZ = 'editor_fuzz'

    def add_modified_request(self, modified_request: HttpRequest):
        if self.request_id is None:
            raise Exception("cannot call add_modified_request() on a flow which has request_id = None")

        self.original_request = self.request
        self.request = modified_request

    def add_response(self, response: HttpResponse):
        self.response = response

    def add_modified_response(self, modified_response: HttpResponse):
        if self.response_id is None:
            raise Exception("cannot call add_modified_response() on a flow which has response_id = None")

        self.original_response = self.response
        self.response = modified_response
