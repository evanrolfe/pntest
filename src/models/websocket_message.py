from dataclasses import dataclass
from dataclasses import field
from typing import Optional

@dataclass(kw_only=True)
class WebsocketMessage():
    # Columns
    id: int = field(init=False)
    http_flow_id: int
    direction: str
    content: str
    content_original: Optional[str]
    created_at: int

    # Relations
