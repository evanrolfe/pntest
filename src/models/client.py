from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from models.model import Model

@dataclass(kw_only=True)
class Client(Model):
    # Columns
    id: int = field(init=False)
    proxy_port: int
    browser_port: Optional[int] = field(default=None)
    launched_at: Optional[int] = field(default=None)
    title: str
    type: str
    open: bool = field(default=False)
    created_at: int = field(default=1) # TODO

    # Relations
