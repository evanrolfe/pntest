from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from models.model import Model

@dataclass(kw_only=True)
class WebsocketMessage(Model):
    # Columns
    id: int = field(init=False, default=0)
    http_flow_id: int
    direction: str
    content: str
    content_original: Optional[str]
    created_at: int

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": [],
    }
