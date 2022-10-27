from asyncio import create_task
import sqlite3
import uuid
from venv import create
from lib.database import Database
from models.client import Client
from models.data import http_flow
from models.http_flow import HttpFlow
from models.http_request import FormData, HttpRequest
from models.http_response import HttpResponse
from models.websocket_message import WebsocketMessage
from repos.http_flow_repo import HttpFlowRepo
from repos.client_repo import ClientRepo
from lib.database import Database
from lib.database_schema import SCHEMA_SQL, NUM_TABLES
from support.factories.client_factory import ClientFactory
from support.factories.http_request_factory import HttpRequestFactory
from support.factories.http_response_factory import HttpResponseFactory
from support.factories.websocket_message_factory import WebsocketMessageFactory

example_form_data: FormData = {
    "method": "GET",
    "url": "http://www.synack.com/login.php",
    "headers": {"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"},
    "content": '{ "username": "${payload:usernames}", "password": "${payload:passwords}" }',
    "fuzz_data": None,
}

def create_multiple_flows() -> list[HttpFlow]:
    client = Client(title="test client!", type="browser", proxy_port=8080)
    ClientRepo().save(client)
    flow1 = HttpFlow(
        uuid=str(uuid.uuid4()),
        type="proxy",
        created_at=1,
        client=client,
        request=HttpRequestFactory.build(path="/modified1"),
        original_request=HttpRequestFactory.build(path="/original1"),
        response=HttpResponseFactory.build(status_code=404, content="not found"),
        original_response=HttpResponseFactory.build(status_code=200, content="original"),
    )
    flow2 = HttpFlow(
        uuid=str(uuid.uuid4()),
        type="proxy",
        created_at=1,
        client=client,
        request=HttpRequestFactory.build(path="/modified2"),
        original_request= HttpRequestFactory.build(path="/original2"),
        response=HttpResponseFactory.build(status_code=200, content="<html>hello world</html>"),
        original_response=HttpResponseFactory.build(status_code=200, content="<html>original</html>"),
    )
    HttpFlowRepo().save(flow1)
    HttpFlowRepo().save(flow2)

    return [flow1, flow2]

class TestHttpFlowRepo:
    def test_saving_and_retrieving_a_flow(self, database, cleanup_database):
        http_flow_repo = HttpFlowRepo()
        client_repo = ClientRepo()

        client: Client = ClientFactory.build()
        client_repo.save(client)

        flow = HttpFlow(
            type="proxy",
            created_at=1,
            client=client,
            request=HttpRequestFactory.build(path="/original")
        )
        http_flow_repo.save(flow)

        assert flow.id is not None
        assert flow.client_id == client.id
        assert flow.type == "proxy"
        assert client.created_at is not None

    def test_finding_a_flow_that_doesnt_exist(self, database, cleanup_database):
        http_flow_repo = HttpFlowRepo()
        result = http_flow_repo.find(0)

        assert result is None

    def test_updating_a_flow(self, database, cleanup_database):
        http_flow_repo = HttpFlowRepo()
        client_repo = ClientRepo()

        client: Client = ClientFactory.build()
        client_repo.save(client)

        flow = HttpFlow(
            type="proxy",
            created_at=1,
            client=client,
            request=HttpRequestFactory.build(path="/original")
        )
        http_flow_repo.save(flow)

        assert flow.id is not None

        flow.created_at = 2
        flow.type = 'editor'
        http_flow_repo.save(flow)

        flow2 = http_flow_repo.find(flow.id)
        assert flow2 is not None
        assert flow.id == flow.id
        assert flow.created_at == 2
        assert flow.type == 'editor'

    def test_saving_a_flow_and_modifying_the_request(self, database, cleanup_database):
        # 1. Create a Client, HttpFlow with HttpRequest
        http_flow_repo = HttpFlowRepo()
        client_repo = ClientRepo()

        client: Client = ClientFactory.build()
        client_repo.save(client)

        orig_request: HttpRequest = HttpRequestFactory.build(path="/original")

        flow = HttpFlow(type="proxy", created_at=1, client=client, request=orig_request)
        http_flow_repo.save(flow)

        assert flow.id is not None
        assert flow.request is not None
        assert flow.request.id is not None
        assert orig_request.id is not None
        assert flow.request_id == orig_request.id

        # 2. Add a modified request
        modified_request = orig_request.duplicate()
        modified_request.modify("GET", "/modified", {}, "")
        flow.add_modified_request(modified_request)
        http_flow_repo.save(flow)
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
        http_flow_repo = HttpFlowRepo()
        client_repo = ClientRepo()

        client = Client(title="test client!", type="browser", proxy_port=8080)
        client_repo.save(client)
        request = HttpRequestFactory.build(path="/")

        flow = HttpFlow(type="proxy", created_at=1, client=client, request=request)
        http_flow_repo.save(flow)

        # 2. Add a response and save
        orig_response = HttpResponseFactory.build(status_code=200, content="original")
        flow.response = orig_response
        http_flow_repo.save(flow)

        assert flow.response is not None
        assert flow.response.id is not None
        assert orig_response.id is not None
        assert flow.response_id == orig_response.id

        # 3. Modify the response and save
        modified_response = HttpResponseFactory.build(status_code=404, content="modified!")

        flow.add_modified_response(modified_response)
        http_flow_repo.save(flow)
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
        http_flow_repo = HttpFlowRepo()
        client_repo = ClientRepo()

        client = Client(title="test client!", type="browser", proxy_port=8080)
        client_repo.save(client)
        request = HttpRequestFactory.build(path="/")

        flow = HttpFlow(type="proxy", created_at=1, client=client, request=request)
        http_flow_repo.save(flow)

        ws_message = WebsocketMessageFactory.build(direction="incoming", content="hello world")
        flow.add_ws_message(ws_message)
        http_flow_repo.save(flow)

        assert len(flow.websocket_messages) == 1
        assert flow.websocket_messages[0] == ws_message
        assert ws_message.id > 0
        assert ws_message.http_flow_id == flow.id

    def test_find_for_table(self, database, cleanup_database):
        flow1, flow2 = create_multiple_flows()

        results = HttpFlowRepo().find_for_table("")

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

        assert results[0].original_response is not None
        assert results[1].original_response is not None
        assert results[0].original_response.id > 0
        assert results[1].original_response.id > 0

    def test_find_by_uuid(self, database, cleanup_database):
        _, flow2 = create_multiple_flows()
        if flow2.uuid is None:
            assert False

        result = HttpFlowRepo().find_by_uuid(flow2.uuid)

        assert result is not None
        assert result.id == flow2.id
