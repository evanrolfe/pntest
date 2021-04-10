from orator import Model
from orator.orm import has_one, has_many
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from models.data.websocket_message import WebsocketMessage

class HttpFlow(Model):
    __table__ = 'http_flows'
    __fillable__ = ['*']

    TYPE_PROXY = 'proxy'
    TYPE_EDITOR = 'editor'
    TYPE_EDITOR_EXAMPLE = 'editor_example'

    @classmethod
    def find_for_table(cls):
        return cls.with_('request', 'response').where('type', '=', cls.TYPE_PROXY).order_by('id', 'desc').get()

    @classmethod
    def create_for_editor(cls):
        request = HttpRequest()
        request.set_blank_values_for_editor()
        request.save()

        flow = HttpFlow()
        flow.type = HttpFlow.TYPE_EDITOR
        flow.request_id = request.id
        flow.save()

        return flow

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

    def request_modified(self):
        original_request_id = getattr(self, 'original_request_id', None)
        return original_request_id is not None

    def response_modified(self):
        original_response_id = getattr(self, 'original_response_id', None)
        return original_response_id is not None

    def modified(self):
        return self.request_modified() or self.response_modified()

    def has_response(self):
        return hasattr(self, 'response_id')

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
        new_request = self.request.duplicate()
        new_request.save()

        new_flow = HttpFlow()
        new_flow.type = HttpFlow.TYPE_EDITOR_EXAMPLE
        new_flow.request_id = new_request.id
        new_flow.response_id = response.id
        new_flow.http_flow_id = self.id
        new_flow.save()

        return new_flow

    def modify_request(self, modified_method, modified_path, modified_headers, modified_content):
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

    def modify_response(self, modified_status_code, modified_headers, modified_content):
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
        return HttpFlow.with_('request', 'response', 'websocket_messages').find(self.id)

    def get_host_and_port(self, host):
        if ':' in host:
            return host.split(':')
        else:
            return [host, None]

    def is_editable(self):
        # Note: this would be false for navigation requests, which we dont have at the moment
        return True

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
