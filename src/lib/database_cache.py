from __future__ import annotations
from typing import Any, Optional

class DatabaseCache():
    # Singleton method stuff:
    __instance = None
    cached_records: dict[str, dict[int, Any]]

    @staticmethod
    def get_instance() -> DatabaseCache:
        # Static access method.
        if DatabaseCache.__instance is None:
            return DatabaseCache()
        return DatabaseCache.__instance

    def __init__(self):
        self.cached_records = {}
        # Virtually private constructor.
        if DatabaseCache.__instance is not None:
            raise Exception("DatabaseCache class is a singleton!")
        else:
            DatabaseCache.__instance = self
    # /Singleton method stuff

    def cache_record(self, table_name: str, id: int, record: Any) -> None:
        if not self.cached_records.get(table_name):
            self.cached_records[table_name] = {}

        self.cached_records[table_name][id] = record

    def get_record(self, table_name: str, id: int) -> Optional[Any]:
        if not self.cached_records.get(table_name):
            return None

        return self.cached_records[table_name].get(id, None)

    def clear(self):
        self.cached_records = {}
