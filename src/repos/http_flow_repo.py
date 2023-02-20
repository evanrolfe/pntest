import sqlite3
from typing import Any, Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order

from models.client import Client
from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from repos.base_repo import BaseRepo
from repos.client_repo import ClientRepo
# NOTE: This technically breaks SRP, we may want to refactor this in the future..
from repos.http_request_repo import HttpRequestRepo
from repos.http_response_repo import HttpResponseRepo
from repos.ws_message_repo import WsMessageRepo

class HttpFlowRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('http_flows')

    def save(self, flow: HttpFlow):
        # Update or insert the HttpFlow
        if flow.id > 0:
            self.generic_update(flow, self.table)
        else:
            self.generic_insert(flow, self.table)

    def delete(self, flow: HttpFlow):
        self.generic_delete(flow, self.table)

    def find(self, id: int) -> Optional[HttpFlow]:
        query = Query.from_(self.table).select('*').where(self.table.id == id)
        results = self.__find_by_query(query.get_sql(), [])

        if len(results) == 0:
            return None
        return results[0]

    def find_by_uuid(self, uuid: str) -> Optional[HttpFlow]:
        query = Query.from_(self.table).select('*').where(self.table.uuid == uuid)
        results = self.__find_by_query(query.get_sql(), [])

        if len(results) == 0:
            return None
        return results[0]

    def find_for_table(self, search_term: str) -> list[HttpFlow]:
        # TODO: These needs to apply host filters from Settings
        if len(search_term) > 0:
            return self.__find_by_search(search_term)

        query = Query.from_(self.table).select('*').where(self.table.type == HttpFlow.TYPE_PROXY).orderby(self.table.id, order=Order.desc)
        http_flows = self.__find_by_query(query.get_sql(), [])

        return http_flows

    def find_by_ids(self, ids: list[int]) -> list[HttpFlow]:
        query = Query.from_(self.table).select('*').where(self.table.id.isin(ids))
        return self.__find_by_query(query.get_sql(), [])

    # This is used to find all example flows for a set of flows
    def find_by_http_flow_id(self, http_flow_ids: list[int]) -> list[HttpFlow]:
        query = Query.from_(self.table).select('*').where(self.table.http_flow_id.isin(http_flow_ids))
        return self.__find_by_query(query.get_sql(), [])

    # See https://www.sqlite.org/fts5.html
    #
    # Example queries:
    # host:^"www.google.com"
    # host:"www.google.com" AND path:"complete"
    def __find_by_search(self, search_term: str) -> list[HttpFlow]:
        # Wrap quotes around search text if none provided
        # User may want to for more advanced search queries like:
        # host:"synack.com" path:"solutions/talent"
        if '"' not in search_term:
            search_term = f'"{search_term}"'

        query = "SELECT * FROM http_requests_fts WHERE http_requests_fts MATCH ? ORDER BY rank;"
        cursor = self.conn.cursor()
        cursor.execute(query, [search_term])
        rows: list[sqlite3.Row] = cursor.fetchall()

        request_ids = [r['id'] for r in rows]

        query = Query.from_(self.table).select('*').where(self.table.request_id.isin(request_ids)).where(self.table.type == HttpFlow.TYPE_PROXY).orderby(self.table.id, order=Order.desc)
        return self.__find_by_query(query.get_sql(), [])

    def __find_by_query(self, sql_query: str, sql_params: list[Any]) -> list[HttpFlow]:
        cursor = self.conn.cursor()
        cursor.execute(sql_query, sql_params)
        rows: list[sqlite3.Row] = cursor.fetchall()

        # Instantiate the flows with their associated objects
        flows: list[HttpFlow] = []
        for row in rows:
            row_values = self.row_to_dict(row)

            # Load Request
            row_values['request'] = HttpRequest.build_blank_placeholder()

            flow = HttpFlow(**row_values)
            flow.id = row['id']
            flow.created_at = row['created_at']
            flows.append(flow)

        return flows
