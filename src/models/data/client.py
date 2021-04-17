from orator import Model
from lib.process_manager import ProcessManager
from lib.browser_launcher.command_options import get_command_line_options

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

    def launch(self, client_info):
        print(f"Launching client:")
        print(client_info)
        process_manager = ProcessManager.get_instance()
        process_manager.launch_proxy(self)

        browser_command = client_info.get('command')
        if browser_command:
            options = get_command_line_options(self)
            print(options)
            process_manager.launch_browser(self, browser_command, options)

        self.open = True
        self.save()

    def close(self):
        process_manager = ProcessManager.get_instance()
        process_manager.close_proxy(self)
        self.open = False
        self.save()
