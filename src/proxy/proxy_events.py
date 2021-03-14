class ProxyEvents:
    def __init__(self):
        self.num = 0

    def set_proxy(self, proxy):
        self.proxy = proxy

    def request(self, flow):
        print(f"----> Request [{self.proxy.opts.listen_port}]: {flow.request.method} {flow.request.url}")
        # import code; code.interact(local=dict(globals(), **locals()))
        # flow.intercept()
        # flow_original = flow.copy()
        # flow.request.path = '/api/posts/2.json'
        # flow.resume()

    def response(self, flow):
        print(f"----> Response [{self.proxy.opts.listen_port}]: {flow.response.status_code}")

    def websocket_start(self, flow):
        print("-----------> websocket_start")
        print(flow)
        flow.inject_message(flow.client_conn, f'This is the injected message!')

    def websocket_message(self, flow):
        print("-----------> websocket_message")
        print(flow)
