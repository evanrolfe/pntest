from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from entities.client import Client
from entities.http_request import HttpRequest
from entities.http_response import HttpResponse
from entities.model import Model
from entities.websocket_message import WebsocketMessage
from lib.background_worker import WorkerSignals
from lib.http_request import HttpRequest as HttpRequestLib
from mitmproxy.common_types import ProxyRequest


@dataclass(kw_only=True)
class HttpFlow(Model):
    # Columns
    id: int = field(init=False, default=0)
    created_at: int = field(init=False, default=0)

    uuid: Optional[str] = None
    source_id: Optional[str] = None
    source_type: Optional[str] = None
    type: str
    title: Optional[str] = None
    request_id: int = 0 # TODO: Maybe this should be handled in the same way that id is handled?
    original_request_id: Optional[int] = None
    response_id: Optional[int] = None
    original_response_id: Optional[int] = None
    http_flow_id: Optional[int] = None

    # Relations
    client: Optional[Client] = None
    request: HttpRequest
    original_request: Optional[HttpRequest] = None
    response: Optional[HttpResponse] = None
    original_response: Optional[HttpResponse] = None
    websocket_messages: list[WebsocketMessage] = field(default_factory=lambda: [])
    examples: list[HttpFlow] = field(default_factory=lambda: [])

    # Ephemeral properties
    intercept_websocket_message: bool = False

    meta = {
        "relationship_keys": [
            "client",
            "request",
            "original_request",
            "response",
            "original_response",
            "websocket_messages",
            "examples",
        ],
        "json_columns": [],
        "do_not_save_keys": ["intercept_websocket_message"],
    }

    TYPE_PROXY = 'proxy'
    TYPE_EDITOR = 'editor'
    TYPE_EDITOR_EXAMPLE = 'editor_example'
    TYPE_EDITOR_FUZZ = 'editor_fuzz'

    SOURCE_TYPE_CLIENT = 'client'
    SOURCE_TYPE_IP = 'ip'

    @classmethod
    def build_blank_for_editor(cls, type: str):
        request = HttpRequest.build_blank_for_editor()

        return HttpFlow(
            type=type,
            request=request,
        )

    @classmethod
    def from_proxy_request(cls, proxy_request: ProxyRequest):
        request = HttpRequest.from_state(proxy_request)

        if proxy_request['client_id'] > 0:
            source_id = str(proxy_request['client_id'])
            source_type = cls.SOURCE_TYPE_CLIENT

            print("--------> source id:", source_id)
        else:
            source_id = proxy_request['source_ip']
            source_type = cls.SOURCE_TYPE_IP

        return HttpFlow(
            uuid = proxy_request['flow_uuid'],
            source_id = source_id,
            source_type = source_type,
            request_id = request.id,
            type = HttpFlow.TYPE_PROXY,
            request = request,
        )

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

    def add_ws_message(self, ws_message: WebsocketMessage):
        ws_message.http_flow_id = self.id
        self.websocket_messages.append(ws_message)

    def is_example(self) -> bool:
        return self.http_flow_id is not None

    def request_modified(self):
        return self.original_request_id is not None

    def response_modified(self):
        return self.original_response_id is not None

    def modified(self):
        return self.request_modified() or self.response_modified()

    def has_request(self) -> bool:
        return self.request_id is not None

    def has_response(self) -> bool:
        return self.response_id is not None

    def is_type_proxy(self) -> bool:
        return self.type == HttpFlow.TYPE_PROXY

    def is_type_editor(self) -> bool:
        return self.type == HttpFlow.TYPE_EDITOR

    def is_type_editor_example(self) -> bool:
        return self.type == HttpFlow.TYPE_EDITOR_EXAMPLE

    def is_type_editor_fuzz(self) -> bool:
        return self.type == HttpFlow.TYPE_EDITOR_FUZZ

    def values_for_table(self) -> list[Any]:
        if self.request is None:
            return ['', '', '', '', '', '', '', '']

        if self.response is not None:
            status_code = self.response.status_code
        else:
            status_code = None

        if self.client is not None:
            client_col = self.client.title
        else:
            client_col = self.source_id

        return [
            self.id,
            client_col,
            self.request.scheme,
            self.request.method,
            self.request.host,
            self.request.path,
            status_code,
            self.modified()
        ]

    # This is used by the intercept/proxy when forwarding requests/responses
    def serialize(self):
        serialized_dict = super().serialize()
        serialized_dict['request'] = self.request.serialize()

        if self.response is not None:
            serialized_dict['response'] = self.response.serialize()

        serialized_dict['websocket_messages'] = [ws.serialize() for ws in self.websocket_messages]

        return serialized_dict

    def duplicate_for_editor(self):
        new_request = self.request.duplicate()
        new_request.overwrite_calculated_headers()

        return HttpFlow(
            type = HttpFlow.TYPE_EDITOR,
            title =  f'{self.title} (Copy)',
            request = new_request,
        )

    def duplicate_for_fuzz(self):
        new_request = self.request.duplicate()
        new_request.overwrite_calculated_headers()

        return HttpFlow(
            type = HttpFlow.TYPE_EDITOR_FUZZ,
            title =  f'{self.title}',
            request = new_request,
        )

    def build_example(self, response) -> HttpFlow:
        example_flow = HttpFlow(
            type = HttpFlow.TYPE_EDITOR_EXAMPLE,
            title = f'Example 123 TODO', # #{self.examples.count() + 1}
            http_flow_id = self.id,
            request = self.request.duplicate(),
            response = response,
        )
        self.examples.append(example_flow)

        return example_flow

    def build_example_for_fuzz(self, num) -> HttpFlow:
        example_flow = HttpFlow(
            type = HttpFlow.TYPE_EDITOR_EXAMPLE,
            title = f'Example #{num}',
            http_flow_id = self.id,
            request = self.request.duplicate(),
        )
        self.examples.append(example_flow)

        return example_flow

    # TODO
    def reload(self):
        pass
        # return HttpFlow.with_('request', 'response', 'websocket_messages', 'examples').find(self.id)

    def get_host_and_port(self, host):
        if ':' in host:
            return host.split(':')
        else:
            return [host, None]

    def is_editable(self):
        return True

    def make_request(self, signals: Optional[WorkerSignals] = None) -> HttpResponse:
        method = self.request.method
        url = self.request.get_url()
        headers = self.request.get_headers() or {}
        content = self.request.content
        req = HttpRequestLib(method, url, headers, content)

        raw_response = req.send()
        return HttpResponse.from_requests_response(raw_response)

    # When a flow is received from the proxy, we save it to the db, and then clear the body, so
    # as to not use up too much memory.
    # When you click a request in the network table, the body is once again loaded from the db.
    def clear_extra_data(self):
        if self.response is None:
            return
        self.response.clear_extra_data()
