from typing import Optional
from models.data.orator_model import OratorModel
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
