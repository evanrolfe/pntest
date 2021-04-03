# import rpyc
import asyncio
import zmq.asyncio
import threading
# import simplejson as json

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

    def resume_flow(self):
        print('[Proxy] resuming')
        flow = self.intercepted_flows.pop(0)
        flow.resume()

    def request(self, flow):
        self.socket.send_string(f'Intercepted request: {flow.request.method}  {flow.request.url}')
        # flow.intercept()
        # self.intercepted_flows.append(flow)

    def response(self, flow):
        print('response')

proxy_events = ProxyEvents()
# rpc_client = rpyc.connect("localhost", 18861, config={"allow_all_attrs": True})

print('Proxy server starting..')
proxy = Proxy(proxy_events, 8080)
loop = asyncio.get_event_loop()
proxy_thread = threading.Thread(target=proxy.run_in_thread, args=(loop, proxy.master))
proxy_thread.start()

print('connecting ZMQ...')
queue = asyncio.Queue()
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % 5556)
socket.send_string('[Proxy] connected')
proxy_events.set_socket(socket)

while True:
    msg = socket.recv().decode("utf-8")
    print(f'Received: {msg}')
    if msg == 'resume':
        proxy_events.resume_flow()
        socket.send_string('ok')

proxy_thread.join()
