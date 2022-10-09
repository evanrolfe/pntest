import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order


from models.client import Client
from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from repos.base_repo import BaseRepo
from repos.http_request_repo import HttpRequestRepo
from repos.http_response_repo import HttpResponseRepo

class HttpFlowRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('http_flows')

    def find(self, id: int) -> Optional[HttpFlow]:
        row = self.generic_find(id, self.table)
        if row is None:
            return

        flow = HttpFlow(**self.row_to_dict(row))
        flow.id = row['id']
        return flow

    def save(self, flow: HttpFlow):
        # Set client_id from associated Client object
        if flow.client is not None:
            flow.client_id = flow.client.id

        # Set request_id from associated HttpRequest object and save if its not persisted
        if flow.request is not None:
            if flow.request.id == 0:
                self.generic_insert(flow.request, Table('http_requests'))
            flow.request_id = flow.request.id

        # Set original_request_id from associated HttpRequest object and save if its not persisted
        if flow.original_request is not None:
            if flow.original_request.id == 0:
                self.generic_insert(flow.original_request, Table('http_requests'))
            flow.original_request_id = flow.original_request.id

        # Set request_id from associated HttpRequest object and save if its not persisted
        if flow.response is not None:
            if flow.response.id == 0:
                self.generic_insert(flow.response, Table('http_responses'))
            flow.response_id = flow.response.id

        # Set original_response_id from associated HttpResponse object and save if its not persisted
        if flow.original_response is not None:
            if flow.original_response.id == 0:
                self.generic_insert(flow.original_response, Table('http_responses'))
            flow.original_response_id = flow.original_response.id

        # Save the websocket messages
        for ws_message in flow.websocket_messages:
            if ws_message.id == 0:
                self.generic_insert(ws_message, Table('websocket_messages'))

        # Update or insert the HttpFlow
        if flow.id > 0:
            self.generic_update(flow, self.table)
        else:
            self.generic_insert(flow, self.table)

    def find_for_table(self, search_text: str) -> list[HttpFlow]:
        # TODO: These needs to apply host filters from Settings

        query = Query.from_(self.table).select('*').where(self.table.type == HttpFlow.TYPE_PROXY).orderby(self.table.id, order=Order.desc)
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql())
        rows: list[sqlite3.Row] = cursor.fetchall()

        flows: list[HttpFlow] = []
        for row in rows:
            flow = HttpFlow(**self.row_to_dict(row))
            flow.id = row['id']
            flows.append(flow)

        # Fetch the associated requests from db in a single query
        request_ids = [f.request_id for f in flows if f.request_id is not None] + \
            [f.original_request_id for f in flows if f.original_request_id is not None]

        http_request_repo = HttpRequestRepo()
        requests = http_request_repo.find_by_ids(request_ids)
        requests_by_id: dict[int, HttpRequest] = self.index_models_by_id(requests)

        # Fetch the associated responses from db in a single query
        response_ids = [f.response_id for f in flows if f.response_id is not None] + \
            [f.original_response_id for f in flows if f.original_response_id is not None]

        http_response_repo = HttpResponseRepo()
        responses = http_response_repo.find_by_ids(response_ids)
        responses_by_id: dict[int, HttpResponse] = self.index_models_by_id(responses)

        # Set the associated objects on the flows
        for flow in flows:
            if flow.request_id is not None:
                flow.request = requests_by_id[flow.request_id]

            if flow.original_request_id is not None:
                flow.original_request = requests_by_id[flow.original_request_id]

            if flow.response_id is not None:
                flow.response = responses_by_id[flow.response_id]

            if flow.original_response_id is not None:
                flow.original_response = responses_by_id[flow.original_response_id]

        return flows
