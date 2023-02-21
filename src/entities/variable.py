from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from entities.model import Model

@dataclass(kw_only=True)
class Variable(Model):
    # Columns
    id: int = field(init=False, default=0)
    created_at: int = field(init=False, default=0)

    key: str
    value: str
    description: Optional[str] = None
    source_type: str
    source_id: Optional[int] = None

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": [],
        "do_not_save_keys": [],
    }

    # Constants
    SOURCE_TYPE_GLOBAL = 'global'
    SOURCE_TYPE_REQUEST = 'http_request'

    @classmethod
    def build_blank_global(cls):
        return Variable(
            key = '',
            value = '',
            source_type = cls.SOURCE_TYPE_GLOBAL,
        )

    def is_blank(self):
        return (self.key == '' and self.value == '')
