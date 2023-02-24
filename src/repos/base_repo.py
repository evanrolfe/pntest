import json
import time
import sqlite3
from typing import Any, Optional
from pypika import QmarkParameter, Query, Table
from entities.model import Model

from lib.database import Database

class BaseRepo:
    conn: sqlite3.Connection

    def __init__(self):
        self.conn = Database.get_instance().conn

    def row_to_dict(self, row: sqlite3.Row):
        d = {}
        for key in row.keys():
            if key not in ['id', 'created_at']:
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
        # Add the created_at timestamp
        model.created_at = int(time.time())

        columns = self.model_columns(model)
        values = [v for v in self.model_values(model)]
        qmark_values = [QmarkParameter() for _ in values]

        query = Query.into(table).columns(*columns).insert(*qmark_values)
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql(), values)
        self.conn.commit()

        if cursor.lastrowid is not None:
            model.id = cursor.lastrowid

    def generic_find(self, id: int, table: Table) -> Optional[sqlite3.Row]:
        query = Query.from_(table).select('*').where(table.id == QmarkParameter())
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql(), [id])
        row: sqlite3.Row = cursor.fetchone()
        return row

    def generic_update(self, model: Model, table: Table):
        columns = [c for c in self.model_columns(model)]
        values = [v for v in self.model_values(model)]
        qmark_values = [QmarkParameter() for _ in values]

        query = Query.update(table).where(table.id == model.id)
        for i in range(len(columns)):
            query = query.set(columns[i], qmark_values[i])

        cursor = self.conn.cursor()
        cursor.execute(query.get_sql(), values)
        self.conn.commit()

    def generic_delete(self, model: Model, table: Table):
        if model.id == 0:
            raise Exception("cannot delete a row which isn't saved")

        query = Query.from_(table).delete().where(table.id == QmarkParameter())
        self.conn.execute(query.get_sql(), [model.id])
        self.conn.commit()

    # TODO: This should be moved to the Model class
    def __model_row_dict(self, model: Model) -> dict[str, Any]:
        raw_table_values = {}
        for key, value in model.__dict__.items():
            if  key in model.meta['json_columns']:
                raw_table_values[key] = json.dumps(value)
            elif key not in model.meta['relationship_keys']+ model.meta['do_not_save_keys']:
                raw_table_values[key] = value

        return raw_table_values
