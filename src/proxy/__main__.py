import rpyc
import asyncio
import threading
import simplejson as json

from proxy import Proxy

class ProxyEvents:
    def __init__(self, rpc_client):
        self.rcp_client = rpc_client

    def set_proxy(self, proxy):
        self.proxy = proxy

    def request(self, flow):
        print('request')
        self.rcp_client.root.signals.emit_request(json.dumps(flow.get_state()))

    def response(self, flow):
        print('response')
        self.rcp_client.root.signals.emit_response(json.dumps(flow.get_state()))

print('Connecting to ProxyEvents service...')
rpc_client = rpyc.connect("localhost", 18861, config={"allow_all_attrs": True})

print('Proxy server starting..')
proxy_events = ProxyEvents(rpc_client)
proxy = Proxy(proxy_events, 8080)

loop = asyncio.get_event_loop()
proxy_thread = threading.Thread(target=proxy.run_in_thread, args=(loop, proxy.master))
proxy_thread.start()
proxy_thread.join()
