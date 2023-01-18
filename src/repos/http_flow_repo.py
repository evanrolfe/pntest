import sqlite3
from typing import Any, Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order

from models.client import Client
from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from repos.base_repo import BaseRepo
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
        # Set client_id from associated Client object
        if flow.client is not None:
            flow.client_id = flow.client.id

        # Set request_id from associated HttpRequest object and save
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

        # Save the examples
        for example_flow in flow.examples:
            if example_flow.id == 0:
                self.save(example_flow)

        # Update or insert the HttpFlow
        if flow.id > 0:
            self.generic_update(flow, self.table)
        else:
            self.generic_insert(flow, self.table)

    def delete(self, flow: HttpFlow):
        # TODO: Put all these operations in a transaction and rollback if any fail
        self.generic_delete(flow, self.table)

        if flow.request.id > 0:
            HttpRequestRepo().delete(flow.request)

        if flow.original_request is not None:
            if flow.original_request.id == 0:
                HttpRequestRepo().delete(flow.original_request)

        if flow.response is not None:
            if flow.response.id == 0:
                HttpResponseRepo().delete(flow.response)

        if flow.original_response is not None:
            if flow.original_response.id == 0:
                HttpResponseRepo().delete(flow.original_response)

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
            return self.find_by_search(search_term)

        query = Query.from_(self.table).select('*').where(self.table.type == HttpFlow.TYPE_PROXY).orderby(self.table.id, order=Order.desc)
        return self.__find_by_query(query.get_sql(), [], False, True)

    def find_by_ids(self, ids: list[int]) -> list[HttpFlow]:
        query = Query.from_(self.table).select('*').where(self.table.id.isin(ids))
        return self.__find_by_query(query.get_sql(), [])

    # This is used to find all example flows for a set of flows
    def find_by_http_flow_id(self, http_flow_ids: list[int]) -> list[HttpFlow]:
        query = Query.from_(self.table).select('*').where(self.table.http_flow_id.isin(http_flow_ids))
        return self.__find_by_query(query.get_sql(), [], False)

    # See https://www.sqlite.org/fts5.html
    #
    # Example queries:
    # host:^"www.google.com"
    # host:"www.google.com" AND path:"complete"
    def find_by_search(self, search_term: str) -> list[HttpFlow]:
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
        return self.__find_by_query(query.get_sql(), [], False)

    def __find_by_query(self, sql_query: str, sql_params: list[Any], load_examples = True, load_minimal_data = False) -> list[HttpFlow]:
        cursor = self.conn.cursor()
        cursor.execute(sql_query, sql_params)
        rows: list[sqlite3.Row] = cursor.fetchall()

        # Pre-load the associated requests from db in a single query
        request_ids = [r['request_id'] for r in rows if r['request_id'] is not None] + \
            [r['original_request_id'] for r in rows if r['original_request_id'] is not None]

        requests = HttpRequestRepo().find_by_ids(request_ids)
        requests_by_id: dict[int, HttpRequest] = self.index_models_by_id(requests)

        # Pre-load the associated responses from db in a single query
        response_ids = [r['response_id'] for r in rows if r['response_id'] is not None] + \
            [r['original_response_id'] for r in rows if r['original_response_id'] is not None]

        responses = HttpResponseRepo().find_by_ids(response_ids, load_minimal_data)
        responses_by_id: dict[int, HttpResponse] = self.index_models_by_id(responses)

        #  Pre-load the associated example HttpFlows from db in a single query
        example_flows_by_id: dict[int, list[HttpFlow]] = {}
        if load_examples:
            http_flow_ids =  [r['id'] for r in rows]
            example_flows = self.find_by_http_flow_id(http_flow_ids)
            for example_flow in example_flows:
                if example_flow.http_flow_id is None:
                    continue
                if example_flows_by_id.get(example_flow.http_flow_id):
                    example_flows_by_id[example_flow.http_flow_id].append(example_flow)
                else:
                    example_flows_by_id[example_flow.http_flow_id] = [example_flow]

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

            # Load the Examples
            examples = example_flows_by_id.get(row['id'])
            if examples:
                row_values['examples'] = examples

            flow = HttpFlow(**row_values)
            flow.id = row['id']
            flow.created_at = row['created_at']
            flows.append(flow)

        return flows
