import json
import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order

from models.http_response import HttpResponse
from repos.base_repo import BaseRepo

# NOTE: This repo should not be accessed directly, only via the HttpFlowRepo
class HttpResponseRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('http_responses')

    def find_by_ids(self, ids: list[int]) -> list[HttpResponse]:
        query = Query.from_(self.table).select('*').where(self.table.id.isin(ids))
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql())
        rows: list[sqlite3.Row] = cursor.fetchall()

        responses = []
        for row in rows:
            response = HttpResponse(**self.row_to_dict(row))
            response.id = row['id']
            response.created_at = row['created_at']
            response.headers = json.loads(row['headers'])
            responses.append(response)

        return responses

    def save(self, response: HttpResponse):
        # NOTE: Requests are only ever inserted, never updated.
        self.generic_insert(response, self.table)

    def delete(self, response: HttpResponse):
        self.generic_delete(response, self.table)
