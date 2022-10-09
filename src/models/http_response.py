from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from models.model import Model

@dataclass(kw_only=True)
class HttpResponse(Model):
    # Columns
    id: int = field(init=False, default=0)
    http_version: str
    headers: str
    content: Optional[str]
    timestamp_start: float
    timestamp_end: float
    status_code: int
    reason: Optional[str]
    created_at: int

    # Relations

    meta = {
        "relationship_keys": []
    }
