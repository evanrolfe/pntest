from asyncio import create_task
import sqlite3
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

example_form_data: FormData = {
    "method": "GET",
    "url": "http://www.synack.com/login.php",
    "headers": {"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"},
    "content": '{ "username": "${payload:usernames}", "password": "${payload:passwords}" }',
    "fuzz_data": None,
}

class TestHttpFlowRepo:
    def test_saving_and_retrieving_a_flow(self, database):
        http_flow_repo = HttpFlowRepo()
        client_repo = ClientRepo()

        client = Client(title="test client!", type="browser", proxy_port=8080)
        client_repo.save(client)

        flow = HttpFlow(
            type="proxy",
            created_at=1,
            client=client,
            request=HttpRequest(
                http_version="HTTP/2.0",
                headers={},
                host="synack.com",
                port=80,
                method="GET",
                scheme="http",
                path="/ORIGINAL",
                form_data=example_form_data,
                created_at=1
            )
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

    def test_updating_a_flow(self, database):
        http_flow_repo = HttpFlowRepo()
        client_repo = ClientRepo()

        client = Client(title="test client!", type="browser", proxy_port=8080)
        client_repo.save(client)

        flow = HttpFlow(
            type="proxy",
            created_at=1,
            client=client,
            request=HttpRequest(
                http_version="HTTP/2.0",
                headers={},
                host="synack.com",
                port=80,
                method="GET",
                scheme="http",
                path="/ORIGINAL",
                form_data=example_form_data,
                created_at=1
            )
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

        client = Client(title="test client!", type="browser", proxy_port=8080)
        client_repo.save(client)

        orig_request = HttpRequest(
            http_version="HTTP/2.0",
            headers={},
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/",
            form_data=example_form_data,
            created_at=1
        )

        flow = HttpFlow(type="proxy", created_at=1, client=client, request=orig_request)
        http_flow_repo.save(flow)

        assert flow.id is not None
        assert flow.request is not None
        assert flow.request.id is not None
        assert orig_request.id is not None
        assert flow.request_id == orig_request.id

        # 2. Add a modified request
        modified_request = HttpRequest(
            http_version="HTTP/2.0",
            headers={},
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/modified",
            form_data=example_form_data,
            created_at=1
        )
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
        request = HttpRequest(
            http_version="HTTP/2.0",
            headers={},
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/",
            form_data=example_form_data,
            created_at=1
        )
        flow = HttpFlow(type="proxy", created_at=1, client=client, request=request)
        http_flow_repo.save(flow)

        # 2. Add a response and save
        orig_response = HttpResponse(
            http_version="HTTP/2.0",
            headers="{}",
            content="<html></html>",
            timestamp_start=1.0,
            timestamp_end=2.0,
            status_code=200,
            reason=None,
            created_at=1,
        )
        flow.response = orig_response
        http_flow_repo.save(flow)

        assert flow.response is not None
        assert flow.response.id is not None
        assert orig_response.id is not None
        assert flow.response_id == orig_response.id

        # 3. Modify the response and save
        modified_response = HttpResponse(
            http_version="HTTP/2.0",
            headers="{}",
            content="this has been modified!",
            timestamp_start=1.0,
            timestamp_end=2.0,
            status_code=404,
            reason=None,
            created_at=1,
        )

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
        request = HttpRequest(
            http_version="HTTP/2.0",
            headers={},
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/",
            form_data=example_form_data,
            created_at=1
        )
        flow = HttpFlow(type="proxy", created_at=1, client=client, request=request)
        http_flow_repo.save(flow)

        ws_message = WebsocketMessage(
            http_flow_id=flow.id,
            direction="incoming",
            content="hello world",
            content_original=None,
            created_at=1
        )
        flow.websocket_messages.append(ws_message)
        http_flow_repo.save(flow)

        assert len(flow.websocket_messages) == 1
        assert flow.websocket_messages[0] == ws_message
        assert ws_message.id > 0

    # def test_find_for_table(self, database, cleanup_database):
    #         # 1. Create a Client, HttpFlow with HttpRequest
    #     http_flow_repo = HttpFlowRepo()
    #     client_repo = ClientRepo()

    #     client = Client(title="test client!", type="browser", proxy_port=8080)
    #     client_repo.save(client)
    #     flow1 = HttpFlow(
    #         type="proxy",
    #         created_at=1,
    #         client=client,
    #         request=HttpRequest(
    #             http_version="HTTP/2.0",
    #             headers="{}",
    #             host="synack.com",
    #             port=80,
    #             method="GET",
    #             scheme="http",
    #             path="/one",
    #             form_data=example_form_data,
    #             created_at=1
    #         ),
    #         original_request=HttpRequest(
    #             http_version="HTTP/2.0",
    #             headers="{}",
    #             host="synack.com",
    #             port=80,
    #             method="GET",
    #             scheme="http",
    #             path="/ORIGINAL",
    #             form_data=example_form_data,
    #             created_at=1
    #         ),
    #         response=HttpResponse(
    #             http_version="HTTP/2.0",
    #             headers="{}",
    #             content="not found",
    #             timestamp_start=1.0,
    #             timestamp_end=2.0,
    #             status_code=404,
    #             reason=None,
    #             created_at=1,
    #         ),
    #         original_response=HttpResponse(
    #             http_version="HTTP/2.0",
    #             headers="{}",
    #             content="ORIGINAL",
    #             timestamp_start=1.0,
    #             timestamp_end=2.0,
    #             status_code=200,
    #             reason=None,
    #             created_at=1,
    #         ),
    #     )
    #     flow2 = HttpFlow(
    #         type="proxy",
    #         created_at=1,
    #         client=client,
    #         request=HttpRequest(
    #             http_version="HTTP/2.0",
    #             headers="{}",
    #             host="synack.com",
    #             port=80,
    #             method="GET",
    #             scheme="http",
    #             path="/two",
    #             form_data=example_form_data,
    #             created_at=1
    #         ),
    #         original_request= HttpRequest(
    #             http_version="HTTP/2.0",
    #             headers="{}",
    #             host="synack.com",
    #             port=80,
    #             method="GET",
    #             scheme="http",
    #             path="/original",
    #             form_data=example_form_data,
    #             created_at=1
    #         ),
    #         response=HttpResponse(
    #             http_version="HTTP/2.0",
    #             headers="{}",
    #             content="<html>hello world</html>",
    #             timestamp_start=1.0,
    #             timestamp_end=2.0,
    #             status_code=200,
    #             reason=None,
    #             created_at=1,
    #         ),
    #         original_response=HttpResponse(
    #             http_version="HTTP/2.0",
    #             headers="{}",
    #             content="<html>orig</html>",
    #             timestamp_start=1.0,
    #             timestamp_end=2.0,
    #             status_code=200,
    #             reason=None,
    #             created_at=1,
    #         ),
    #     )
    #     http_flow_repo.save(flow1)
    #     http_flow_repo.save(flow2)

    #     results = http_flow_repo.find_for_table("")

    #     assert len(results) == 2
    #     assert results[0].id == flow2.id
    #     assert results[1].id == flow1.id

    #     assert results[0].request is not None
    #     assert results[1].request is not None
    #     assert results[0].request.id > 0
    #     assert results[1].request.id > 0

    #     assert results[0].original_request is not None
    #     assert results[1].original_request is not None
    #     assert results[0].original_request.id > 0
    #     assert results[1].original_request.id > 0

    #     assert results[0].response is not None
    #     assert results[1].response is not None
    #     assert results[0].response.id > 0
    #     assert results[1].response.id > 0

    #     assert results[0].original_response is not None
    #     assert results[1].original_response is not None
    #     assert results[0].original_response.id > 0
    #     assert results[1].original_response.id > 0
