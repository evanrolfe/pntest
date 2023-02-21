import json
import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order, QmarkParameter

from entities.http_response import HttpResponse
from repos.base_repo import BaseRepo

# NOTE: This repo should not be accessed directly, only via the HttpFlowRepo
class HttpResponseRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('http_responses')

    def find_by_ids(self, ids: list[int], load_minimal_data = False) -> list[HttpResponse]:
        qmark_values = [QmarkParameter() for _ in ids]

        if load_minimal_data:
            # Load all the columns except for content
            columns = ['id','http_version','headers','timestamp_start','timestamp_end','status_code','reason','created_at']
        else:
            columns = '*'

        query = Query.from_(self.table).select(*columns).where(self.table.id.isin(qmark_values))
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql(), ids)
        rows: list[sqlite3.Row] = cursor.fetchall()

        responses = []
        for row in rows:
            response_values = self.row_to_dict(row)
            if load_minimal_data:
                response_values['content'] = None

            response = HttpResponse(**response_values)
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
