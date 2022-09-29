from dataclasses import dataclass
from dataclasses import field
from typing import Optional

@dataclass(kw_only=True)
class Client:
    # Columns
    id: int = field(init=False)
    proxy_port: int
    browser_port: Optional[int] = None
    launched_at: Optional[int] = None
    title: str
    type: str
    open: bool = False
    created_at: int = 1

    # Relations
