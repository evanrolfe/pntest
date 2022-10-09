import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field

from lib.database import Database

from models.client import Client
from models.model import Model
from models.http_flow import HttpFlow

class ClientRepo:
    conn: sqlite3.Connection
    table: Table

    def __init__(self):
        self.conn = Database.get_instance().conn
        self.table = Table('clients')

    def find(self, id: int) -> Optional[Client]:
        row = self.__generic_find(id, self.table)
        if row is None:
            return

        client = Client(**self.__row_to_dict(row))
        client.id = row['id']
        return client

    def save(self, client: Client):
        self.__generic_insert(client, self.table)

    def __row_to_dict(self, row: sqlite3.Row):
        d = {}
        for key in row.keys():
            if key != 'id':
                d[key] = row[key]

        return d

    def __generic_insert(self, model: Model, table: Table):
        query = Query.into(table).columns(*model.__dict__.keys()).insert(*model.__dict__.values())
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql())
        self.conn.commit()

        if cursor.lastrowid is not None:
            model.id = cursor.lastrowid

    def __generic_find(self, id: int, table: Table) -> Optional[sqlite3.Row]:
        query = Query.from_(table).select('*').where(table.id == id)
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql())
        row: sqlite3.Row = cursor.fetchone()
        return row
