from dataclasses import dataclass
from dataclasses import field
from typing import Optional, TypedDict
from lib.types import Headers
from models.data.payload_file import PayloadFile, PayloadFileSerialised
from models.model import Model

class FuzzFormData(TypedDict):
    payload_files: list[PayloadFileSerialised]
    fuzz_type: str
    delay_type: str
    delay_secs: Optional[str]
    delay_secs_min: Optional[str]
    delay_secs_max: Optional[str]

class FormData(TypedDict):
    method: str
    url: str
    headers: Headers
    content: str
    fuzz_data: Optional[FuzzFormData]

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
    form_data: FormData
    created_at: int

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": ["form_data"]
    }


