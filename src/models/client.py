from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from models.model import Model

@dataclass(kw_only=True)
class Client(Model):
    # Columns
    id: int = field(init=False, default=0)
    created_at: int = field(init=False, default=0)

    proxy_port: int
    browser_port: Optional[int] = field(default=None)
    launched_at: Optional[int] = field(default=None)
    title: str
    type: str
    open: bool = field(default=False)

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": [],
        "do_not_save_keys": [],
    }
