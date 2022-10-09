import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field


from models.client import Client
from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from repos.base_repo import BaseRepo

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

    # TODO: This logic should go in the model
    def add_modified_request(self, flow: HttpFlow, modified_request: HttpRequest):
        if flow.request_id is None:
            raise Exception("cannot call add_modified_request() on a flow which has request_id = None")

        flow.original_request = flow.request
        flow.request = modified_request
        self.save(flow)

    # TODO: This logic should go in the model
    def add_modified_response(self, flow: HttpFlow, modified_response: HttpResponse):
        if flow.response_id is None:
            raise Exception("cannot call add_modified_response() on a flow which has response_id = None")

        flow.original_response = flow.response
        flow.response = modified_response
        self.save(flow)
