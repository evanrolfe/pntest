from __future__ import annotations
from typing import Optional

from models.data.orator_model import OratorModel
from models.data.http_request import HttpRequest

class Variable(OratorModel):
    # Database columns:
    id: int
    key: str
    value: str
    description: Optional[str]
    source_type: str
    source_id: Optional[int]
    created_at: Optional[int]

    # Associations:

    # Constants:
    SOURCE_TYPE_GLOBAL: str
    SOURCE_TYPE_REQUEST: str

    def item(self) -> Optional[HttpRequest]:
        pass

    def is_blank(self) -> bool:
        pass

    def save(self, *args, **kwargs):
        pass

    @classmethod
    def all_global(cls) -> list[Variable]:
        pass

    @classmethod
    def find_by_key(cls, key: str) -> Optional[Variable]:
        pass
