from __future__ import annotations
from typing import Any, Optional
from entities.client import Client
from entities.http_flow import HttpFlow
from entities.http_request import HttpRequest
from entities.http_response import HttpResponse
from repos.client_repo import ClientRepo
from repos.http_flow_repo import HttpFlowRepo
from repos.http_request_repo import HttpRequestRepo
from repos.http_response_repo import HttpResponseRepo
from repos.ws_message_repo import WsMessageRepo

class HttpFlowService():
    def __init__(self):
        super().__init__()

    def find(self, id: int, **kwargs) -> Optional[HttpFlow]:
        http_flow = HttpFlowRepo().find(id)
        if http_flow is None:
            return None

        self.__load_associations([http_flow], **kwargs)
        return http_flow

    def find_by_uuid(self, uuid: str) -> Optional[HttpFlow]:
        http_flow = HttpFlowRepo().find_by_uuid(uuid)
        if http_flow is None:
            return None

        self.__load_associations([http_flow])
        return http_flow

    def find_for_table(self, search_term: str) -> list[HttpFlow]:
        http_flows = HttpFlowRepo().find_for_table(search_term)

        self.__load_associations(http_flows)
        return http_flows

    def find_by_ids(self, ids: list[int], **kwargs) -> list[HttpFlow]:
        http_flows = HttpFlowRepo().find_by_ids(ids)

        self.__load_associations(http_flows, **kwargs)
        return http_flows

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

        HttpFlowRepo().save(flow)

    def delete(self, flow: HttpFlow):
        # TODO: Put all these operations in a transaction and rollback if any fail
        HttpFlowRepo().delete(flow)

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

    def __load_associations(self,
        http_flows: list[HttpFlow],
        *,
        load_examples = False,
        load_minimal_response_data = True
    ):
        # Pre-load the associated requests from db in a single query
        request_ids = [flow.request_id for flow in http_flows] + \
            [flow.original_request_id for flow in http_flows if flow.original_request_id is not None]
        requests = HttpRequestRepo().find_by_ids(request_ids)
        requests_by_id: dict[int, HttpRequest] = self.__index_models_by_id(requests)

        # Pre-load the associated responses from db in a single query
        response_ids = [flow.response_id for flow in http_flows if flow.response_id is not None] + \
            [flow.original_response_id for flow in http_flows if flow.original_response_id is not None]

        responses = HttpResponseRepo().find_by_ids(response_ids, load_minimal_response_data)
        responses_by_id: dict[int, HttpResponse] = self.__index_models_by_id(responses)

        # Pre-load associated clients
        client_ids = [flow.client_id for flow in http_flows if flow.client_id is not None]
        client_ids_uniq = list(set(client_ids))
        clients = ClientRepo().find_by_ids(client_ids_uniq)
        clients_by_id: dict[int, Client] = self.__index_models_by_id(clients)

        # Pre-load the associated example HttpFlows from db in a single query
        example_flows_by_id: dict[int, list[HttpFlow]] = {}
        if load_examples:
            http_flow_ids = [flow.id for flow in http_flows]
            example_flows = HttpFlowRepo().find_by_http_flow_id(http_flow_ids)

            for example_flow in example_flows:
                if example_flow.http_flow_id is None:
                    continue
                if example_flows_by_id.get(example_flow.http_flow_id):
                    example_flows_by_id[example_flow.http_flow_id].append(example_flow)
                else:
                    example_flows_by_id[example_flow.http_flow_id] = [example_flow]

        for http_flow in http_flows:
            request = requests_by_id.get(http_flow.request_id)
            if request is None:
                raise Exception(f"no request found for http_flow id {http_flow.id}")

            http_flow.request = request

            if http_flow.original_request_id is not None:
                http_flow.original_request = requests_by_id.get(http_flow.original_request_id)

            if http_flow.response_id is not None:
                http_flow.response = responses_by_id.get(http_flow.response_id)

            if http_flow.original_response_id is not None:
                http_flow.original_response = responses_by_id.get(http_flow.original_response_id)

            if http_flow.client_id is not None:
                http_flow.client = clients_by_id.get(http_flow.client_id)

            examples = example_flows_by_id.get(http_flow.id)
            if examples:
                http_flow.examples = examples

    def __index_models_by_id(self, models: list[Any]) -> dict[int, Any]:
        indexed_models = {}
        for model in models:
            indexed_models[model.id] = model

        return indexed_models
