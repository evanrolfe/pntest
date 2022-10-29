from dataclasses import dataclass
from dataclasses import field

from typing import Any, Optional
from models.client import Client
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from models.websocket_message import WebsocketMessage
from models.model import Model
from lib.types import Headers
from lib.background_worker import WorkerSignals
from proxy.common_types import ProxyRequest, ProxyResponse

@dataclass(kw_only=True)
class HttpFlow(Model):
    # Columns
    id: int = field(init=False, default=0)
    created_at: int = field(init=False, default=0)

    uuid: Optional[str] = None
    client_id: Optional[int] = None
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

    # Ephemeral properties
    intercept_websocket_message: bool = False

    meta = {
        "relationship_keys": [
            "client",
            "request",
            "original_request",
            "response",
            "original_response",
            "websocket_messages"
        ],
        "json_columns": [],
        "do_not_save_keys": ["intercept_websocket_message"],
    }

    TYPE_PROXY = 'proxy'
    TYPE_EDITOR = 'editor'
    TYPE_EDITOR_EXAMPLE = 'editor_example'
    TYPE_EDITOR_FUZZ = 'editor_fuzz'

    @classmethod
    def create_for_editor(cls, type):
        pass
        # request = HttpRequest()
        # request.set_blank_values_for_editor()
        # request.save()

        # flow = HttpFlow()
        # flow.type = type
        # flow.request_id = request.id
        # flow.save()

        # return flow

    @classmethod
    # TODO: Type check the ProxyRequest
    def from_proxy_request(cls, proxy_request: ProxyRequest):
        request = HttpRequest.from_state(proxy_request)

        return HttpFlow(
            uuid = proxy_request['flow_uuid'],
            client_id = proxy_request['client_id'],
            request_id = request.id,
            type = HttpFlow.TYPE_PROXY,
            request = request,
        )

    @classmethod
    def update_from_proxy_response(cls, proxy_response: ProxyResponse):
        pass
        # flow = HttpFlow.where('uuid', '=', proxy_response['flow_uuid']).first()
        # if flow is None:
        #     return

        # response = HttpResponse.from_state(proxy_response)
        # response.save()

        # # Awful hack, this ORM is total sh*te and the update does not even work, so I have to use a query
        # database = Database.get_instance()
        # database.db.table('http_flows').where('id', flow.id).update(response_id=response.id)

        # flow2 = HttpFlow.find(flow.id)
        # return flow2

    @classmethod
    def create_from_proxy_websocket_message(cls, proxy_websocket_message):
        pass
        # http_flow = HttpFlow.where('uuid', '=', proxy_websocket_message['flow_uuid']).first()

        # websocket_message = WebsocketMessage.from_state(proxy_websocket_message)
        # websocket_message.http_flow_id = http_flow.id
        # websocket_message.save()

        # return http_flow, websocket_message

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

    def values_for_table(self):
        if self.request is None:
            return ['', '', '', '', '', '', '', '']

        if self.response is not None:
            status_code = self.response.status_code
        else:
            status_code = None

        return [
            self.id,
            self.client_id,
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

    # TODO
    def duplicate_for_editor(self):
        pass
        # new_request = self.request.duplicate()
        # new_request.overwrite_calculated_headers()
        # new_request.save()

        # new_flow = HttpFlow()
        # new_flow.type = HttpFlow.TYPE_EDITOR
        # new_flow.request_id = new_request.id
        # new_flow.save()

        # return new_flow

    # TODO
    def duplicate_for_example(self, response):
        pass
        # response.save()

        # new_request = self.request.duplicate()
        # new_request.save()

        # new_flow = HttpFlow()
        # new_flow.type = HttpFlow.TYPE_EDITOR_EXAMPLE
        # new_flow.title = f'Example #{self.examples.count() + 1}'
        # new_flow.request_id = new_request.id
        # new_flow.response_id = response.id
        # new_flow.http_flow_id = self.id
        # new_flow.save()

        # return new_flow

    # TODO
    def duplicate_for_fuzz_example(self, num):
        pass
        # new_request = self.request.duplicate()
        # new_request.save()

        # new_flow = HttpFlow()
        # new_flow.type = HttpFlow.TYPE_EDITOR_EXAMPLE
        # new_flow.title = f'Example #{num}'
        # new_flow.request_id = new_request.id
        # new_flow.http_flow_id = self.id
        # new_flow.save()

        # return new_flow

    # TODO
    def modify_response(self, modified_status_code: int, modified_headers: Headers, modified_content: str):
        pass
        # original_response = self.response().first()
        # original_state = original_response.get_state()

        # response_unchanged = (
        #     original_state['status_code'] == modified_status_code and
        #     original_state['headers'] == modified_headers and
        #     original_state['content'] == modified_content
        # )

        # if response_unchanged:
        #     return

        # original_state['status_code'] = modified_status_code
        # original_state['headers'] = modified_headers
        # original_state['content'] = modified_content

        # new_response = HttpResponse.from_state(original_state)
        # new_response.save()

        # # Awful hack, this ORM is total sh*te and the update does not even work, so I have to use a query
        # database = Database.get_instance()
        # database.db.table('http_flows').where('id', self.id).update(original_response_id=original_response.id, response_id=new_response.id)

    # TODO
    def modify_latest_websocket_message(self, modified_content):
        pass
        # websocket_messages = self.websocket_messages().get()
        # websocket_message = websocket_messages[-1]

        # if websocket_message.content == modified_content:
        #     return

        # websocket_message.content_original = websocket_message.content
        # websocket_message.content = modified_content
        # websocket_message.save()

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

    # TODO:
    def make_request(self, signals: Optional[WorkerSignals] = None):
        pass
        # method = self.request.method
        # url = self.request.get_url()
        # headers = self.request.get_headers() or {}
        # content = self.request.content
        # req = HttpRequestLib(method, url, headers, content)

        # raw_response = req.send()
        # http_response = HttpResponse.from_requests_response(raw_response)

        # return http_response

    # TODO:
    def make_request_and_save(self):
        pass
        # response = self.make_request()
        # response.save()

        # # Awful hack, this ORM is total sh*te and the update does not even work, so I have to use a query
        # database = Database.get_instance()
        # database.db.table('http_flows').where('id', self.id).update(response_id=response.id)
