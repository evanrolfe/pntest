from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from models.model import Model

@dataclass(kw_only=True)
class HttpRequest(Model):
    # Columns
    id: int = field(init=False, default=0)
    http_version: str
    headers: str
    content: Optional[str] = None
    trailers: Optional[str] = None
    timestamp_start: Optional[float] = None
    timestamp_end: Optional[float] = None
    host: str
    port: int
    method: str
    scheme: str
    authority: Optional[str] = None
    path: str
    form_data: str
    created_at: int

    # Relations

    meta = {
        "relationship_keys": []
    }
