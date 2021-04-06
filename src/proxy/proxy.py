from mitmproxy import addons, master, options
from mitmproxy.addons import termlog, keepserving, readfile
import asyncio

class ErrorCheck:
    def __init__(self):
        self.has_errored = False

    def add_log(self, e):
        if e.level == "error":
            self.has_errored = True

class Proxy():
    def __init__(self, proxy_events, listen_port):
        self.opts = options.Options()
        self.opts.listen_port = listen_port
        self.opts.confdir = '/home/evan/Code/mitmproxy/certs'

        self.master = master.Master(self.opts)
        proxy_events.set_proxy(self)
        self.master.addons.add(proxy_events)

        self.master.errorcheck = ErrorCheck()
        self.master.addons.add(termlog.TermLog())
        self.master.addons.add(*addons.default_addons())
        self.master.addons.add(
            keepserving.KeepServing(),
            readfile.ReadFileStdin(),
            self.master.errorcheck
        )

    def run_in_thread(self, loop, master):
        asyncio.set_event_loop(loop)
        self.master.run_loop(loop.run_forever)
