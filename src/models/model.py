from dataclasses import dataclass
from dataclasses import field
from typing import TypedDict

class ModelMetaData(TypedDict):
    relationship_keys: list[str]
    json_columns: list[str]

class Model():
    id: int = field(init=False, default=0)

    meta: ModelMetaData

    pass
