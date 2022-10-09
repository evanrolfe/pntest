import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field
from models.model import Model

from lib.database import Database

class BaseRepo:
    conn: sqlite3.Connection

    def __init__(self):
        self.conn = Database.get_instance().conn

    def row_to_dict(self, row: sqlite3.Row):
        d = {}
        for key in row.keys():
            if key != 'id':
                d[key] = row[key]

        return d

    def generic_insert(self, model: Model, table: Table):
        query = Query.into(table).columns(*model.__dict__.keys()).insert(*model.__dict__.values())
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql())
        self.conn.commit()

        if cursor.lastrowid is not None:
            model.id = cursor.lastrowid

    def generic_find(self, id: int, table: Table) -> Optional[sqlite3.Row]:
        query = Query.from_(table).select('*').where(table.id == id)
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql())
        row: sqlite3.Row = cursor.fetchone()
        return row
