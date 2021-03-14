from mitmproxy import addons, master, options
from mitmproxy.addons import termlog, keepserving, readfile
import asyncio

from PySide2 import QtCore

class ErrorCheck:
    def __init__(self):
        self.has_errored = False

    def add_log(self, e):
        if e.level == "error":
            self.has_errored = True

class Proxy(QtCore.QRunnable):
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

    # def run(self):
    #     print("----------> Proxy.run()")
    #     try:
    #         self.master.run()
    #         print("----------> Proxy.started()")

    #         loop = asyncio.get_event_loop()
    #         try:
    #             loop.add_signal_handler(signal.SIGINT, getattr(self.master, "prompt_for_exit", self.master.shutdown))
    #             loop.add_signal_handler(signal.SIGTERM, self.master.shutdown)
    #         except NotImplementedError:
    #             # Not supported on Windows
    #             pass
    #     except exceptions.OptionsError as e:
    #         print("{}: {}".format(sys.argv[0], e), file=sys.stderr)
    #         sys.exit(1)
    #     except (KeyboardInterrupt, RuntimeError):
    #         pass
