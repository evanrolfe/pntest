from typing import Optional
from models.data.orator_model import OratorModel
from lib.process_manager import ProcessManager
from proxy.common_types import SettingsJson

PROXY_PORT = 8080
BROWSER_PORT = 9222

class Client(OratorModel):
    id: int
    title: Optional[str]
    cookies: Optional[str]
    pages: Optional[str]
    type: str
    proxy_port: Optional[int]
    browser_port: Optional[int]
    open: bool
    created_at: Optional[int]
    updated_at: Optional[int]

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

    # TODO: Client should not have ProcessManager as a dependency
    def launch(self, client_info, settings: SettingsJson):
        print(f"Launching client:")
        print(client_info)
        process_manager = ProcessManager.get_instance()
        process_manager.launch_proxy(self, settings)

        browser_command = client_info.get('command')
        if browser_command:
            process_manager.launch_browser(self, browser_command)

        self.open = True
        self.save()

    def close(self):
        process_manager = ProcessManager.get_instance()

        if self.type != 'anything':
            process_manager.close_browser(self)
        else:
            process_manager.close_proxy(self)

        self.open = False
        self.save()
