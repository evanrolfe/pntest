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
    def modify_request(self, modified_method: str, modified_path: str, modified_headers: Headers, modified_content: str):
        pass
        # original_request = self.request().first()
        # original_state = original_request.get_state()
        # request_unchanged = (
        #     original_state['method'] == modified_method and
        #     original_state['path'] == modified_path and
        #     original_state['headers'] == modified_headers and
        #     original_state['content'] == modified_content
        # )

        # if request_unchanged:
        #     return

        # original_state['method'] = modified_method
        # original_state['path'] = modified_path
        # original_state['headers'] = modified_headers
        # original_state['content'] = modified_content

        # if modified_headers.get('Host'):
        #     host, port = self.get_host_and_port(modified_headers['Host'])
        #     original_state['host'] = host
        #     if port:
        #         original_state['port'] = port

        # # TODO: What if the user types in host header lowercase?
        # # if modified_headers.get('host'):
        # #     original_state['host'] = modified_headers['host']

        # new_request = HttpRequest.from_state(original_state)
        # new_request.save()

        # # Awful hack, this ORM is total sh*te and the update does not even work, so I have to use a query
        # database = Database.get_instance()
        # database.db.table('http_flows').where('id', self.id).update(original_request_id=original_request.id, request_id=new_request.id)

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
