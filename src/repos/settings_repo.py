import json
import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order

from models.settings import Settings
from repos.base_repo import BaseRepo

class SettingsRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('settings')

    def get_settings(self) -> Settings:
        settings = self.find(1)
        if settings is not None:
            return settings

        default_settings = Settings.build_default()
        self.insert(default_settings)

        return default_settings

    def find(self, id: int) -> Optional[Settings]:
        row = self.generic_find(id, self.table)
        if row is None:
            return

        settings = Settings(**self.row_to_dict(row))
        settings.id = row['id']
        settings.created_at = row['created_at']
        settings.json = json.loads(row['json'])
        return settings

    def insert(self, settings: Settings):
        self.generic_insert(settings, self.table)

    def update(self, settings: Settings):
        self.generic_update(settings, self.table)
