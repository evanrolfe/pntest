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
from repos.ws_message_repo import WsMessageRepo

class HttpFlowRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('http_flows')

    def find(self, id: int) -> Optional[HttpFlow]:
        query = Query.from_(self.table).select('*').where(self.table.id == id)
        results = self.__find_by_query(query.get_sql())

        if len(results) == 0:
            return None
        return results[0]

    # TODO: DRY this up with find()
    def find_by_uuid(self, uuid: str) -> Optional[HttpFlow]:
        query = Query.from_(self.table).select('*').where(self.table.uuid == uuid)
        results = self.__find_by_query(query.get_sql())

        if len(results) == 0:
            return None
        return results[0]

    def save(self, flow: HttpFlow):
        # Set client_id from associated Client object
        if flow.client is not None:
            flow.client_id = flow.client.id

        # Set request_id from associated HttpRequest object and save if its not persisted
        if flow.request.id == 0:
            HttpRequestRepo().save(flow.request)
        flow.request_id = flow.request.id

        # Set original_request_id from associated HttpRequest object and save if its not persisted
        if flow.original_request is not None:
            if flow.original_request.id == 0:
                HttpRequestRepo().save(flow.original_request)
            flow.original_request_id = flow.original_request.id

        # Set request_id from associated HttpRequest object and save if its not persisted
        if flow.response is not None:
            if flow.response.id == 0:
                HttpResponseRepo().save(flow.response)
            flow.response_id = flow.response.id

        # Set original_response_id from associated HttpResponse object and save if its not persisted
        if flow.original_response is not None:
            if flow.original_response.id == 0:
                HttpResponseRepo().save(flow.original_response)
            flow.original_response_id = flow.original_response.id

        # Save the websocket messages
        for ws_message in flow.websocket_messages:
            if ws_message.id == 0:
                WsMessageRepo().save(ws_message)

        # Update or insert the HttpFlow
        if flow.id > 0:
            self.generic_update(flow, self.table)
        else:
            self.generic_insert(flow, self.table)

    def find_for_table(self, search_text: str) -> list[HttpFlow]:
        # TODO: These needs to apply host filters from Settings

        query = Query.from_(self.table).select('*').where(self.table.type == HttpFlow.TYPE_PROXY).orderby(self.table.id, order=Order.desc)
        return self.__find_by_query(query.get_sql())

    def __find_by_query(self, sql_query: str) -> list[HttpFlow]:
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        rows: list[sqlite3.Row] = cursor.fetchall()

        # Pre-load the associated requests from db in a single query
        request_ids = [r['request_id'] for r in rows if r['request_id'] is not None] + \
            [r['original_request_id'] for r in rows if r['original_request_id'] is not None]

        http_request_repo = HttpRequestRepo()
        requests = http_request_repo.find_by_ids(request_ids)
        requests_by_id: dict[int, HttpRequest] = self.index_models_by_id(requests)

        # Pre-load the associated responses from db in a single query
        response_ids = [r['response_id'] for r in rows if r['response_id'] is not None] + \
            [r['original_response_id'] for r in rows if r['original_response_id'] is not None]

        http_response_repo = HttpResponseRepo()
        responses = http_response_repo.find_by_ids(response_ids)
        responses_by_id: dict[int, HttpResponse] = self.index_models_by_id(responses)

        # Instantiate the flows with their associated objects
        flows: list[HttpFlow] = []
        for row in rows:
            row_values = self.row_to_dict(row)

            # Load Request
            row_values['request'] = requests_by_id[row_values['request_id']]

            # Load Original Request
            if row_values['original_request_id'] is not None:
                row_values['original_request'] = requests_by_id[row_values['original_request_id']]

            # Load Response
            if row_values['response_id'] is not None:
                row_values['response'] = responses_by_id[row_values['response_id']]

            # Load Original Response
            if row_values['original_response_id'] is not None:
                row_values['original_response'] = responses_by_id[row_values['original_response_id']]

            flow = HttpFlow(**row_values)
            flow.id = row['id']
            flows.append(flow)

        return flows

# TODO:
# class HttpFlowObserver:
#     def deleted(self, flow):
#         if flow.request:
#             flow.request.delete()

#         if flow.original_request:
#             flow.original_request.delete()

#         if flow.response:
#             flow.response.delete()

#         if flow.original_response:
#             flow.original_response.delete()

# HttpFlow.observe(HttpFlowObserver())
