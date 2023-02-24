import json
import sqlite3
from typing import Optional
from pypika import QmarkParameter, Query, Table

from entities.http_request import HttpRequest
from repos.base_repo import BaseRepo

# NOTE: This repo should not be accessed directly, only via the HttpFlowRepo
class HttpRequestRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('http_requests')

    def find(self, id: int) -> Optional[HttpRequest]:
        row = self.generic_find(id, self.table)
        if row is None:
            return

        request = HttpRequest(**self.row_to_dict(row))
        request.id = row['id']
        request.created_at = row['created_at']
        request.form_data = json.loads(row['form_data'])
        request.headers = json.loads(row['headers'])
        return request

    def save(self, request: HttpRequest):
        # NOTE: Proxy Requests should only ever be inserted, never updated.
        # Editor requests can be updated.
        if request.id > 0:
            self.generic_update(request, self.table)
        else:
            self.generic_insert(request, self.table)

    def delete(self, request: HttpRequest):
        self.generic_delete(request, self.table)

    def find_by_ids(self, ids: list[int]) -> list[HttpRequest]:
        qmark_values = [QmarkParameter() for _ in ids]

        query = Query.from_(self.table).select('*').where(self.table.id.isin(qmark_values))
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql(), ids)
        rows: list[sqlite3.Row] = cursor.fetchall()

        requests = []
        for row in rows:
            request = HttpRequest(**self.row_to_dict(row))
            request.id = row['id']
            request.created_at = row['created_at']
            request.form_data = json.loads(row['form_data'])
            request.headers = json.loads(row['headers'])
            requests.append(request)

        return requests
