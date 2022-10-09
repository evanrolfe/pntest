from dataclasses import dataclass
from dataclasses import field
from typing import Optional

@dataclass(kw_only=True)
class HttpResponse():
    # Columns
    id: int = field(init=False)
    http_version: str
    headers: str
    content: Optional[str]
    timestamp_start: float
    timestamp_end: float
    status_code: int
    reason: Optional[str]
    created_at: int

    # Relations
