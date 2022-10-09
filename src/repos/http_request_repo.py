import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order

from models.http_request import HttpRequest
from repos.base_repo import BaseRepo

# NOTE: This repo should not be accessed directly, only via the HttpFlowRepo
class HttpRequestRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('http_requests')

    def find_by_ids(self, ids: list[int]) -> list[HttpRequest]:
        query = Query.from_(self.table).select('*').where(self.table.id.isin(ids))
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql())
        rows: list[sqlite3.Row] = cursor.fetchall()

        requests = []
        for row in rows:
            request = HttpRequest(**self.row_to_dict(row))
            request.id = row['id']
            requests.append(request)

        return requests
