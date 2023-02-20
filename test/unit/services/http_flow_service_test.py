from asyncio import create_task
import sqlite3
import uuid
from venv import create
from lib.database import Database
from models.client import Client
from models.http_flow import HttpFlow
from models.http_request import FormData, HttpRequest
from models.http_response import HttpResponse
from models.websocket_message import WebsocketMessage
from repos.http_flow_repo import HttpFlowRepo
from repos.client_repo import ClientRepo
from lib.database import Database
from lib.database_schema import SCHEMA_SQL, NUM_TABLES
from services.http_flow_service import HttpFlowService
from support.factories.client_factory import ClientFactory
from support.factories.http_request_factory import HttpRequestFactory
from support.factories.http_response_factory import HttpResponseFactory
from support.factories.websocket_message_factory import WebsocketMessageFactory

def create_multiple_flows() -> list[HttpFlow]:
    client = Client(title="test client!", type="browser", proxy_port=8080)
    ClientRepo().save(client)
    client2 = Client(title="test client2", type="browser", proxy_port=8080)
    ClientRepo().save(client2)

    flow1 = HttpFlow(
        uuid=str(uuid.uuid4()),
        type="proxy",
        client=client,
        request=HttpRequestFactory.build(path="/modified1"),
        original_request=HttpRequestFactory.build(path="/original1"),
        response=HttpResponseFactory.build(status_code=404, content="not found"),
        original_response=HttpResponseFactory.build(status_code=200, content="original"),
    )
    flow2 = HttpFlow(
        uuid=str(uuid.uuid4()),
        type="proxy",
        client=client2,
        request=HttpRequestFactory.build(path="/modified2"),
        original_request= HttpRequestFactory.build(path="/original2"),
        response=HttpResponseFactory.build(status_code=200, content="<html>hello world</html>"),
        original_response=HttpResponseFactory.build(status_code=200, content="<html>original</html>"),
    )
    HttpFlowService().save(flow1)
    HttpFlowService().save(flow2)

    return [flow1, flow2]

def create_multiple_editor_flows_with_examples() -> list[HttpFlow]:
    flow1 = HttpFlow(
        type="editor",
        request=HttpRequestFactory.build(path="/one"),
    )
    flow2 = HttpFlow(
        type="editor",
        request=HttpRequestFactory.build(path="/two"),
    )
    HttpFlowService().save(flow1)
    HttpFlowService().save(flow2)

    response1: HttpResponse = HttpResponseFactory.build()
    flow1.build_example(response1)
    HttpFlowService().save(flow1)

    response2: HttpResponse = HttpResponseFactory.build()
    flow1.build_example(response2)
    HttpFlowService().save(flow1)

    return [flow1, flow2]

class TestHttpFlowService:
    def test_finding_a_flow_that_doesnt_exist(self, database, cleanup_database):
        result = HttpFlowService().find(0)
        assert result is None

    def test_find_by_uuid(self, database, cleanup_database):
        _, flow2 = create_multiple_flows()
        if flow2.uuid is None:
            assert False

        result = HttpFlowService().find_by_uuid(flow2.uuid)

        assert result is not None
        assert result.id == flow2.id
        assert result.request is not None
        assert result.original_request is not None
        assert result.response is not None
        assert result.original_response is not None

        assert result.request.id > 0
        assert result.original_request.id > 0
        assert result.response.id > 0
        assert result.original_response.id > 0

    def test_find_by_ids(self, database, cleanup_database):
        flow1, flow2 = create_multiple_editor_flows_with_examples()

        results = HttpFlowService().find_by_ids([flow1.id, flow2.id], load_examples = True)

        assert len(results) == 2
        assert results[0].id == flow1.id
        assert results[1].id == flow2.id

        assert results[0].request is not None
        assert results[1].request is not None
        assert results[0].request.id > 0
        assert results[1].request.id > 0

        assert len(results[0].examples) == 2
        assert len(results[1].examples) == 0

        assert results[0].examples[0].id > 0
        assert results[0].examples[1].id > 0

    def test_find_for_table(self, database, cleanup_database):
        flow1, flow2 = create_multiple_flows()

        results = HttpFlowService().find_for_table("")

        assert len(results) == 2
        assert results[0].id == flow2.id
        assert results[1].id == flow1.id

        assert results[0].request is not None
        assert results[1].request is not None
        assert results[0].request.id > 0
        assert results[1].request.id > 0

        assert results[0].original_request is not None
        assert results[1].original_request is not None
        assert results[0].original_request.id > 0
        assert results[1].original_request.id > 0

        assert results[0].response is not None
        assert results[1].response is not None
        assert results[0].response.id > 0
        assert results[1].response.id > 0
        assert results[0].response.content is None
        assert results[1].response.content is None

        assert results[0].original_response is not None
        assert results[1].original_response is not None
        assert results[0].original_response.id > 0
        assert results[1].original_response.id > 0
        assert results[0].original_response.content is None
        assert results[1].original_response.content is None

        assert results[0].client is not None
        assert results[1].client is not None
        assert results[0].client.id > 0
        assert results[1].client.id > 0

    def test_find_for_table_with_search_term(self, database, cleanup_database):
        flow1 = HttpFlow(
            type="proxy",
            request=HttpRequestFactory.build(host="google.com", path="/one"),
            response=HttpResponseFactory.build()
        )
        flow2 = HttpFlow(
            type="proxy",
            request=HttpRequestFactory.build(host="google.com", path="/two"),
            response=HttpResponseFactory.build()
        )
        flow3 = HttpFlow(
            type="proxy",
            request=HttpRequestFactory.build(host="pntest.com", path="/index.html"),
            response=HttpResponseFactory.build()
        )
        flow4 = HttpFlow(
            type="editor",
            request=HttpRequestFactory.build(host="pntest.com", path="/editor.html"),
            response=HttpResponseFactory.build()
        )

        HttpFlowService().save(flow1)
        HttpFlowService().save(flow2)
        HttpFlowService().save(flow3)
        HttpFlowService().save(flow4)

        assert flow1.id is not None

        results = HttpFlowService().find_for_table('pntest')
        assert len(results) == 1
        assert results[0].id == flow3.id

    def test_saving_a_flow_and_response(self, database, cleanup_database):
        request = HttpRequestFactory.build(path="/")
        response: HttpResponse = HttpResponseFactory.build()

        flow = HttpFlow(type="editor", request=request, response=response)
        HttpFlowService().save(flow)

        assert flow.id is not None

    def test_saving_a_flow_and_modifying_the_request(self, database, cleanup_database):
        # 1. Create a Client, HttpFlow with HttpRequest
        client_repo = ClientRepo()

        client: Client = ClientFactory.build()
        client_repo.save(client)

        orig_request: HttpRequest = HttpRequestFactory.build(path="/original")

        flow = HttpFlow(type="proxy", client=client, request=orig_request)
        HttpFlowService().save(flow)

        assert flow.id is not None
        assert flow.request is not None
        assert flow.request.id is not None
        assert orig_request.id is not None
        assert flow.request_id == orig_request.id

        # 2. Add a modified request
        modified_request = orig_request.duplicate()
        modified_request.modify("GET", "/modified", {}, "")
        flow.add_modified_request(modified_request)
        HttpFlowService().save(flow)
        assert flow.request is not None
        assert flow.original_request is not None

        assert flow.request == modified_request
        assert flow.original_request == orig_request

        assert flow.request.id is not None
        assert flow.original_request.id is not None

        assert flow.request_id == modified_request.id
        assert flow.original_request_id == orig_request.id

    def test_adding_a_response_to_a_flow_and_adding_a_modified_response(self, database, cleanup_database):
        # 1. Create a Client, HttpFlow with HttpRequest
        client = Client(title="test client!", type="browser", proxy_port=8080)
        ClientRepo().save(client)
        request = HttpRequestFactory.build(path="/")

        flow = HttpFlow(type="proxy", client=client, request=request)
        HttpFlowService().save(flow)

        # 2. Add a response and save
        orig_response = HttpResponseFactory.build(status_code=200, content="original")
        flow.response = orig_response
        HttpFlowService().save(flow)

        assert flow.response is not None
        assert flow.response.id is not None
        assert orig_response.id is not None
        assert flow.response_id == orig_response.id

        # 3. Modify the response and save
        modified_response = HttpResponseFactory.build(status_code=404, content="modified!")

        flow.add_modified_response(modified_response)
        HttpFlowService().save(flow)
        assert flow.response is not None
        assert flow.original_response is not None

        assert flow.response == modified_response
        assert flow.original_response == orig_response

        assert flow.response.id is not None
        assert flow.original_response.id is not None

        assert flow.response_id == modified_response.id
        assert flow.original_response_id == orig_response.id

    def test_saving_a_flow_and_adding_a_websocket_message(self, database, cleanup_database):
        # 1. Create a Client, HttpFlow with HttpRequest
        client_repo = ClientRepo()

        client = Client(title="test client!", type="browser", proxy_port=8080)
        client_repo.save(client)
        request = HttpRequestFactory.build(path="/")

        flow = HttpFlow(type="proxy", client=client, request=request)
        HttpFlowService().save(flow)

        ws_message = WebsocketMessageFactory.build(direction="incoming", content="hello world")
        flow.add_ws_message(ws_message)
        HttpFlowService().save(flow)

        assert len(flow.websocket_messages) == 1
        assert flow.websocket_messages[0] == ws_message
        assert ws_message.id > 0
        assert ws_message.http_flow_id == flow.id

    def test_saving_a_flow_and_adding_an_example(self, database, cleanup_database):
        # 1. Create a Client, HttpFlow with HttpRequest
        request = HttpRequestFactory.build(path="/")

        flow = HttpFlow(type="editor", request=request)
        HttpFlowService().save(flow)

        response: HttpResponse = HttpResponseFactory.build()
        flow.build_example(response)
        HttpFlowService().save(flow)

        assert len(flow.examples) == 1
        example = flow.examples[0]

        assert example.response == response
        assert example.id > 0
        assert example.request.id > 0
        assert example.response is not None
        assert example.response.id > 0
        assert example.http_flow_id == flow.id

        flow2 = HttpFlowService().find(flow.id)
        assert flow2 is not None
        assert flow2.id == flow.id
        assert len(flow2.examples) == 1
        assert flow2.examples[0].id > 0

    def test_delete(self, database, cleanup_database):
        _, flow2 = create_multiple_flows()

        HttpFlowService().delete(flow2)

        results = HttpFlowService().find_for_table("")
        assert len(results) == 1
