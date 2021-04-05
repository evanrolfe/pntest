from orator import Model
from lib.process_manager import ProcessManager

PROXY_PORT = 8080
BROWSER_PORT = 9222

class Client(Model):
    @classmethod
    def get_next_port_available(cls):
        clients = Client.all()
        proxy_port = PROXY_PORT + len(clients)
        browser_port = BROWSER_PORT + len(clients)

        return {'proxy': proxy_port, 'browser': browser_port}

    def open_text(self):
        if (self.open):
            return 'Open'
        else:
            return 'Closed'

    def launch(self):
        process_manager = ProcessManager.get_instance()
        process_manager.launch_proxy(self)
        self.open = True
        self.save()

    def close(self):
        process_manager = ProcessManager.get_instance()
        process_manager.close_proxy(self)
        self.open = False
        self.save()
