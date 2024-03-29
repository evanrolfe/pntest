from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from entities.browser import Browser
from entities.model import Model
from entities.process import Process
from entities.container import Container

PROXY_PORT = 8080

@dataclass(kw_only=True)
class Client(Model):
    # Columns
    id: int = field(init=False, default=0)
    created_at: int = field(init=False, default=0)

    proxy_port: int
    container_id: Optional[str] = field(default=None)
    launched_at: Optional[int] = field(default=None)
    title: str
    type: str
    open: bool = field(default=False)

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": [],
        "do_not_save_keys": ["browser", "proxy", "intercepted_container", "proxy_container"],
    }

    # Ephemeral properties
    browser: Optional[Browser] = field(default=None)
    proxy: Optional[Process] = field(default=None)
    intercepted_container: Optional[Container] = field(default=None)
    proxy_container: Optional[Container] = field(default=None)

    # Constants
    PROXY_PORT = 8080

    def open_text(self) -> str:
        if (self.open):
            return 'Open'
        else:
            return 'Closed'

    def is_browser(self):
        return self.type in ['chromium', 'chrome', 'firefox']
