from dataclasses import dataclass
from dataclasses import field
import json
from typing import TypedDict

class ModelMetaData(TypedDict):
    relationship_keys: list[str]
    json_columns: list[str]

class Model():
    id: int = field(init=False, default=0)

    meta: ModelMetaData

    def serialize(self) -> dict:
        raw_table_values = {}
        for key, value in self.__dict__.items():
            if  key in self.meta['json_columns']:
                raw_table_values[key] = json.dumps(value)
            elif key not in self.meta['relationship_keys']:
                raw_table_values[key] = value

        return raw_table_values
