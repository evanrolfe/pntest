import simplejson as json
from mitmproxy.http import Headers

class ProxyEvents:
    def __init__(self, client_id):
        self.client_id = client_id
        self.intercept_enabled = False
        self.intercepted_flows = []

    def set_proxy(self, proxy):
        self.proxy = proxy

    def set_socket(self, socket):
        self.socket = socket

    # ---------------------------------------------------------------------------
    # Actions:
    # ---------------------------------------------------------------------------
    def forward_flow(self, message):
        type = message['type']
        modified_flow = message['flow']

        print(f'[Proxy] {type} flow {modified_flow["uuid"]}')
        flow = self.intercepted_flows.pop(0)

        # Overwrite the MitmProxy flow with the values of the Pntest Flow:
        if flow.websocket:
            flow.websocket.messages[-1].content = modified_flow['websocket_messages'][-1]['content'].encode()

        elif flow.response:
            flow.response.status_code = modified_flow['response']['status_code']
            flow.response.headers = self.__convert_headers_for_mitm(modified_flow['response']['headers'])
            flow.response.content = modified_flow['response']['content'].encode()

        else:
            flow.request.path = modified_flow['request']['path']
            flow.request.method = modified_flow['request']['method']
            flow.request.host = modified_flow['request']['host']
            flow.request.port = modified_flow['request']['port']
            flow.request.headers = self.__convert_headers_for_mitm(modified_flow['request']['headers'])
            flow.request.content = modified_flow['request']['content'].encode()
            flow.intercept_response = (message['type'] == 'forward_and_intercept')

        flow.resume()

    def forward_all(self):
        for flow in self.intercepted_flows:
            print(f'[Proxy] forwarding flow {flow.id}')
            flow.intercept_response = False
            flow.resume()

    def drop_flow(self, message):
        type = message['type']
        modified_flow = message['flow']

        print(f'[Proxy] {type} flow {modified_flow["uuid"]}')
        flow = self.intercepted_flows.pop(0)
        flow.kill()

    def intercept_flow(self, flow):
        flow.intercept()
        self.intercepted_flows.append(flow)

    def set_intercept_enabled(self, enabled):
        self.intercept_enabled = enabled

    # ---------------------------------------------------------------------------
    # MitmProxy Events:
    # ---------------------------------------------------------------------------
    def request(self, flow):
        print('[Proxy] HTTP request')

        request_state = flow.request.get_state()
        request_state['flow_uuid'] = flow.id
        request_state['type'] = 'request'
        request_state['client_id'] = self.client_id
        request_state['intercepted'] = self.__should_intercept_request(flow)

        self.__send_message(request_state)

        if request_state['intercepted']:
            self.intercept_flow(flow)

    def response(self, flow):
        print('[Proxy] HTTP response')
        intercept_response = getattr(flow, 'intercept_response', False)

        response_state = flow.response.get_state()
        response_state['flow_uuid'] = flow.id
        response_state['type'] = 'response'
        response_state['content'] = flow.response.text
        response_state['intercepted'] = intercept_response
        self.__send_message(response_state)

        if intercept_response:
            self.intercept_flow(flow)

    def websocket_message(self, flow):
        print('[Proxy] websocket message')
        message = flow.websocket.messages[-1]
        direction = 'outgoing' if message.from_client else 'incoming'

        message_state = {
            'type': 'websocket_message',
            'flow_uuid': flow.id,
            'direction': direction,
            'content': message.content,
            'intercepted': self.__should_intercept_request(flow)
        }
        self.__send_message(message_state)

        if message_state['intercepted']:
            # import code; code.interact(local=dict(globals(), **locals()))
            flow.intercepted_message = message
            self.intercept_flow(flow)

    # ---------------------------------------------------------------------------
    # Private methods:
    # ---------------------------------------------------------------------------
    def __should_intercept_request(self, flow):
        return self.intercept_enabled

    def __convert_headers_for_mitm(self, headers):
        headers_obj = json.loads(headers)
        headers_list = []

        for key, value in headers_obj.items():
            header = (key.encode(), value.encode())
            headers_list.append(header)

        return Headers(headers_list)

    def __send_message(self, message):
        self.socket.send_string(json.dumps(message))
