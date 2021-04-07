import simplejson as json

INTERCPT_REQUESTS = True
INTERCPT_RESPONSES = False

class ProxyEvents:
    def __init__(self, client_id):
        self.client_id = client_id

    def set_proxy(self, proxy):
        self.proxy = proxy
        self.intercepted_flows = []

    def set_socket(self, socket):
        self.socket = socket

    def send_message(self, message):
        self.socket.send_string(json.dumps(message))

    def forward_flow(self, modified_flow):
        print(f'[Proxy] forwarding flow {modified_flow["uuid"]}')
        flow = self.intercepted_flows.pop(0)

        flow.request.path = modified_flow['request']['path']
        flow.request.method = modified_flow['request']['method']
        flow.request.host = modified_flow['request']['host']
        flow.request.port = modified_flow['request']['port']
        flow.request.content = modified_flow['request']['content'].encode()

        flow.resume()

    def intercept_flow(self, flow):
        flow.intercept()
        self.intercepted_flows.append(flow)

    def request(self, flow):
        print('[Proxy] request')
        # Convert bytes to strings:
        request_state = flow.request.get_state()
        request_state['flow_uuid'] = flow.id
        request_state['type'] = 'request'
        request_state['client_id'] = self.client_id
        request_state['intercepted'] = INTERCPT_REQUESTS
        self.send_message(request_state)

        if request_state['intercepted']:
            self.intercept_flow(flow)

    def response(self, flow):
        print('[Proxy] response received')
        response_state = flow.response.get_state()
        response_state['flow_uuid'] = flow.id
        response_state['type'] = 'response'
        response_state['content'] = flow.response.text
        response_state['intercepted'] = INTERCPT_RESPONSES
        self.send_message(response_state)

    def websocket_start(self, flow):
        print('-------> websocket_start')

    def websocket_message(self, flow):
        message = flow.websocket.messages[-1]
        direction = 'outgoing' if message.from_client else 'incoming'
        message_state = {
            'type': 'websocket_message',
            'flow_uuid': flow.id,
            'direction': direction,
            'content': message.content
        }
        print('-------> websocket_message')
        self.send_message(message_state)
