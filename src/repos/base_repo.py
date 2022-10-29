import json
from operator import index
import sqlite3
from typing import Any, Generic, Optional, Type, TypeVar
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

    def index_models_by_id(self, models: list[Any]) -> dict[int, Any]:
        indexed_models = {}
        for model in models:
            indexed_models[model.id] = model

        return indexed_models

    def model_columns(self, model: Model):
        return self.__model_row_dict(model).keys()

    def model_values(self, model: Model):
        return self.__model_row_dict(model).values()

    def generic_insert(self, model: Model, table: Table):
        columns = self.model_columns(model)
        values = self.model_values(model)

        query = Query.into(table).columns(*columns).insert(*values)
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

    def generic_update(self, model: Model, table: Table):
        query = Query.update(table)
        for key, value in self.__model_row_dict(model).items():
            query = query.set(key, value)
        query = query.where(table.id == model.id)
        self.conn.execute(query.get_sql())
        self.conn.commit()

    def generic_delete(self, model: Model, table: Table):
        if model.id == 0:
            raise Exception("cannot delete a row which isn't saved")

        query = Query.from_(table).delete().where(table.id == model.id)
        self.conn.execute(query.get_sql())
        self.conn.commit()

    def __model_row_dict(self, model: Model) -> dict[str, Any]:
        raw_table_values = {}
        for key, value in model.__dict__.items():
            if  key in model.meta['json_columns']:
                raw_table_values[key] = json.dumps(value)
            elif key not in model.meta['relationship_keys']+ model.meta['do_not_save_keys']:
                raw_table_values[key] = value

        return raw_table_values
