import json
import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order, QmarkParameter

from models.variable import Variable
from repos.base_repo import BaseRepo

class VariableRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('variables')

    def find_by_key(self, key: str) -> Optional[Variable]:
        query = Query.from_(self.table).select('*').where(self.table.key == QmarkParameter())
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql(), [key])
        row: sqlite3.Row = cursor.fetchone()
        if row is None:
            return

        variable = Variable(**self.row_to_dict(row))
        variable.id = row['id']
        return variable

    def find_all_global(self) -> list[Variable]:
        query = Query.from_(self.table) \
            .select('*') \
            .where(self.table.source_type == Variable.SOURCE_TYPE_GLOBAL) \
            .orderby(self.table.id, order=Order.asc)

        return self.__find_by_query(query.get_sql())

    def save(self, variable: Variable):
        if variable.id > 0:
            self.generic_update(variable, self.table)
        else:
            self.generic_insert(variable, self.table)

    def __find_by_query(self, sql_query: str) -> list[Variable]:
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        rows: list[sqlite3.Row] = cursor.fetchall()

        variables: list[Variable] = []
        for row in rows:
            variable = Variable(**self.row_to_dict(row))
            variable.id = row['id']
            variable.created_at = row['created_at']
            variables.append(variable)

        return variables
