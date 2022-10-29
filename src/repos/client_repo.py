import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field


from models.client import Client
from repos.base_repo import BaseRepo

class ClientRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('clients')

    def find(self, id: int) -> Optional[Client]:
        row = self.generic_find(id, self.table)
        if row is None:
            return

        client = Client(**self.row_to_dict(row))
        client.id = row['id']
        client.created_at = row['created_at']
        return client

    def save(self, client: Client):
        if client.id > 0:
            self.generic_update(client, self.table)
        else:
            self.generic_insert(client, self.table)
