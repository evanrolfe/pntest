from __future__ import annotations
from typing import Optional
from lib.background_worker import WorkerSignals
from lib.database import Database
from models.data.orator_model import OratorModel
from orator.orm import has_one, has_many
from lib.http_request import HttpRequest as HttpRequestLib
from models.data.http_flow_search import HttpFlowSearch
from models.data.http_request import HttpRequest, Headers
from models.data.http_response import HttpResponse
from models.data.websocket_message import WebsocketMessage
from models.data.settings import Settings
from proxy.common_types import ProxyRequest, ProxyResponse

class HttpFlow(OratorModel):
    __table__ = 'http_flows'
    __fillable__ = ['*']
    __timestamps__ = ['created_at']

    TYPE_PROXY = 'proxy'
    TYPE_EDITOR = 'editor'
    TYPE_EDITOR_EXAMPLE = 'editor_example'
    TYPE_EDITOR_FUZZ = 'editor_fuzz'

    @classmethod
    def find_for_table(cls, search_text):
        settings = Settings.get_from_cache()
        filters = settings.parsed()['display_filters']

        query = cls \
            .with_('request', 'response') \
            .join('http_requests', 'http_flows.request_id', '=', 'http_requests.id') \
            .where('type', '=', cls.TYPE_PROXY) \
            .order_by('id', 'desc')

        if filters['host_setting'] == 'include':
            query.where_in('http_requests.host', filters['host_list'])
        elif filters['host_setting'] == 'exclude':
            query.where_not_in('http_requests.host', filters['host_list'])

        if search_text is not None and len(search_text) > 0:
            # NOTE: * is used to perform a partial text search rather than trying to match the whole word
            flow_ids = HttpFlowSearch.search(f'"{search_text}"*')
            query.where_in('http_flows.id', flow_ids)

        return query.get()

    @classmethod
    def find_by_ids(cls, flow_ids):
        query = cls \
            .with_('request', 'response') \
            .join('http_requests', 'http_flows.request_id', '=', 'http_requests.id') \
            .where('type', '=', cls.TYPE_PROXY) \
            .where_in('http_flows.id', flow_ids) \
            .order_by('http_flows.id', 'desc')

        return query.get()

    @classmethod
    def create_for_editor(cls, type):
        request = HttpRequest()
        request.set_blank_values_for_editor()
        request.save()

        flow = HttpFlow()
        flow.type = type
        flow.request_id = request.id
        flow.save()

        return flow

    @classmethod
    # TODO: Type check the ProxyRequest
    def create_from_proxy_request(cls, proxy_request):
        request = HttpRequest.from_state(proxy_request)
        request.save()

        flow = HttpFlow()
        flow.uuid = proxy_request['flow_uuid']
        flow.client_id = proxy_request['client_id']
        flow.request_id = request.id
        flow.type = HttpFlow.TYPE_PROXY
        flow.save()

        return flow

    @classmethod
    def update_from_proxy_response(cls, proxy_response: ProxyResponse):
        flow = HttpFlow.where('uuid', '=', proxy_response['flow_uuid']).first()
        if flow is None:
            return

        response = HttpResponse.from_state(proxy_response)
        response.save()

        # Awful hack, this ORM is total sh*te and the update does not even work, so I have to use a query
        database = Database.get_instance()
        database.db.table('http_flows').where('id', flow.id).update(response_id=response.id)

        flow2 = HttpFlow.find(flow.id)
        return flow2

    @classmethod
    def create_from_proxy_websocket_message(cls, proxy_websocket_message):
        http_flow = HttpFlow.where('uuid', '=', proxy_websocket_message['flow_uuid']).first()

        websocket_message = WebsocketMessage.from_state(proxy_websocket_message)
        websocket_message.http_flow_id = http_flow.id
        websocket_message.save()

        return http_flow, websocket_message

    @has_one('id', 'request_id')
    def request(self):
        return HttpRequest

    @has_one('id', 'original_request_id')
    def original_request(self):
        return HttpRequest

    @has_one('id', 'response_id')
    def response(self):
        return HttpResponse

    @has_one('id', 'original_response_id')
    def original_response(self):
        return HttpResponse

    @has_many('http_flow_id', 'id')
    def websocket_messages(self):
        return WebsocketMessage

    @has_many('http_flow_id', 'id')
    def examples(self):
        return HttpFlow

    def is_example(self) -> bool:
        return hasattr(self, 'http_flow_id') and self.http_flow_id is not None

    def request_modified(self):
        original_request_id = getattr(self, 'original_request_id', None)
        return original_request_id is not None

    def response_modified(self):
        original_response_id = getattr(self, 'original_response_id', None)
        return original_response_id is not None

    def modified(self):
        return self.request_modified() or self.response_modified()

    def has_response(self) -> bool:
        return hasattr(self, 'response_id')

    def is_type_proxy(self) -> bool:
        return self.type == HttpFlow.TYPE_PROXY

    def is_type_editor(self) -> bool:
        return self.type == HttpFlow.TYPE_EDITOR

    def is_type_editor_example(self) -> bool:
        return self.type == HttpFlow.TYPE_EDITOR_EXAMPLE

    def is_type_editor_fuzz(self) -> bool:
        return self.type == HttpFlow.TYPE_EDITOR_FUZZ

    def values_for_table(self):
        if getattr(self, 'response_id', None):
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

    def duplicate_for_editor(self):
        new_request = self.request.duplicate()
        new_request.overwrite_calculated_headers()
        new_request.save()

        new_flow = HttpFlow()
        new_flow.type = HttpFlow.TYPE_EDITOR
        new_flow.request_id = new_request.id
        new_flow.save()

        return new_flow

    def duplicate_for_example(self, response):
        response.save()

        new_request = self.request.duplicate()
        new_request.save()

        new_flow = HttpFlow()
        new_flow.type = HttpFlow.TYPE_EDITOR_EXAMPLE
        new_flow.title = f'Example #{self.examples.count() + 1}'
        new_flow.request_id = new_request.id
        new_flow.response_id = response.id
        new_flow.http_flow_id = self.id
        new_flow.save()

        return new_flow

    def duplicate_for_fuzz_example(self, num):
        new_request = self.request.duplicate()
        new_request.save()

        new_flow = HttpFlow()
        new_flow.type = HttpFlow.TYPE_EDITOR_EXAMPLE
        new_flow.title = f'Example #{num}'
        new_flow.request_id = new_request.id
        new_flow.http_flow_id = self.id
        new_flow.save()

        return new_flow

    def modify_request(self, modified_method: str, modified_path: str, modified_headers: Headers, modified_content: str):
        original_request = self.request().first()
        original_state = original_request.get_state()
        request_unchanged = (
            original_state['method'] == modified_method and
            original_state['path'] == modified_path and
            original_state['headers'] == modified_headers and
            original_state['content'] == modified_content
        )

        if request_unchanged:
            return

        original_state['method'] = modified_method
        original_state['path'] = modified_path
        original_state['headers'] = modified_headers
        original_state['content'] = modified_content

        if modified_headers.get('Host'):
            host, port = self.get_host_and_port(modified_headers['Host'])
            original_state['host'] = host
            if port:
                original_state['port'] = port

        # TODO: What if the user types in host header lowercase?
        # if modified_headers.get('host'):
        #     original_state['host'] = modified_headers['host']

        new_request = HttpRequest.from_state(original_state)
        new_request.save()

        self.original_request_id = original_request.id
        self.request_id = new_request.id
        self.save()

    def modify_response(self, modified_status_code: int, modified_headers: Headers, modified_content: str):
        original_response = self.response().first()
        original_state = original_response.get_state()

        response_unchanged = (
            original_state['status_code'] == modified_status_code and
            original_state['headers'] == modified_headers and
            original_state['content'] == modified_content
        )

        if response_unchanged:
            return

        original_state['status_code'] = modified_status_code
        original_state['headers'] = modified_headers
        original_state['content'] = modified_content

        new_response = HttpResponse.from_state(original_state)
        new_response.save()

        self.original_response_id = original_response.id
        self.response_id = new_response.id
        self.save()

    def modify_latest_websocket_message(self, modified_content):
        websocket_messages = self.websocket_messages().get()
        websocket_message = websocket_messages[-1]

        if websocket_message.content == modified_content:
            return

        websocket_message.content_original = websocket_message.content
        websocket_message.content = modified_content
        websocket_message.save()

    def reload(self):
        return HttpFlow.with_('request', 'response', 'websocket_messages', 'examples').find(self.id)

    def get_host_and_port(self, host):
        if ':' in host:
            return host.split(':')
        else:
            return [host, None]

    def is_editable(self):
        return True

    def make_request(self, signals: Optional[WorkerSignals] = None):
        method = self.request.method
        url = self.request.get_url()
        headers = self.request.get_headers() or {}
        content = self.request.content
        req = HttpRequestLib(method, url, headers, content)

        raw_response = req.send()
        http_response = HttpResponse.from_requests_response(raw_response)

        return http_response

    def make_request_and_save(self):
        response = self.make_request()
        response.save()

        # Awful hack, this ORM is total sh*te and the update does not even work, so I have to use a query
        database = Database.get_instance()
        database.db.table('http_flows').where('id', self.id).update(response_id=response.id)

class HttpFlowObserver:
    def deleted(self, flow):
        if flow.request:
            flow.request.delete()

        if flow.original_request:
            flow.original_request.delete()

        if flow.response:
            flow.response.delete()

        if flow.original_response:
            flow.original_response.delete()

HttpFlow.observe(HttpFlowObserver())
