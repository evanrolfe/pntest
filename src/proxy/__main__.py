# import rpyc
import asyncio
import zmq.asyncio
import threading
import simplejson as json
from proxy import Proxy

#
# Intercept PoC: start the proxy with: python src/proxy then make a few requests i.e.
# curl http://wonderbill.com --proxy http://127.0.0.1:8080
# curl http://ais.at --proxy http://127.0.0.1:8080
#
# then hit the "open file" menu button to forward a request
#

class ProxyEvents:
    def set_proxy(self, proxy):
        self.proxy = proxy
        self.intercepted_flows = []

    def set_socket(self, socket):
        self.socket = socket

    def send_message(self, message):
        self.socket.send_string(json.dumps(message))
        self.socket.recv_string()

    def resume_flow(self):
        print('[Proxy] resuming')
        flow = self.intercepted_flows.pop(0)
        flow.resume()

    def request(self, flow):
        print('[Proxy] request')
        # Convert bytes to strings:
        request_state = flow.request.get_state()
        request_state['flow_uuid'] = flow.id
        request_state['type'] = 'request'
        self.send_message(request_state)
        # flow.intercept()
        # self.intercepted_flows.append(flow)

    def response(self, flow):
        print('[Proxy] response received')
        response_state = flow.response.get_state()
        response_state['flow_uuid'] = flow.id
        response_state['type'] = 'response'
        response_state['content'] = flow.response.text
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

proxy_events = ProxyEvents()
# rpc_client = rpyc.connect("localhost", 18861, config={"allow_all_attrs": True})

print('Proxy server starting..')
proxy = Proxy(proxy_events, 8080)
loop = asyncio.get_event_loop()
proxy_thread = threading.Thread(target=proxy.run_in_thread, args=(loop, proxy.master))
proxy_thread.start()

print('connecting ZMQ Server...')
queue = asyncio.Queue()
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % 5556)
proxy_events.set_socket(socket)

proxy_thread.join()
