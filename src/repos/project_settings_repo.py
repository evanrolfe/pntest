import json
import sqlite3
import time
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order, QmarkParameter

from entities.project_settings import ProjectSettings, get_default_project_settings
from repos.base_repo import BaseRepo

class ProjectSettingsRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('settings')

    def get(self) -> ProjectSettings:
        id = 1
        row = self.generic_find(id, self.table)
        if row is None:
            return get_default_project_settings()

        settings: ProjectSettings = json.loads(row['json'])
        return settings

    def save(self, settings: ProjectSettings):
        id = 1
        row = self.generic_find(id, self.table)
        json_str = json.dumps(settings)

        if row is None:
            # Insert
            sql = 'INSERT INTO settings (id, json, created_at) VALUES (?,?,?)'
            values = [1, json_str, int(time.time())]
            cursor = self.conn.cursor()
            cursor.execute(sql, values)
            self.conn.commit()
        else:
            # Update
            cursor = self.conn.cursor()
            sql = 'UPDATE settings SET json=? WHERE id=1'
            cursor.execute(sql, [json_str])
            self.conn.commit()
