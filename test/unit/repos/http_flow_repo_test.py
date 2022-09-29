from asyncio import create_task
from venv import create
from sqlalchemy.orm import scoped_session
from lib.database import Database
from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from models.websocket_message import WebsocketMessage
from models.client import Client
from repo.http_flow_repo import HttpFlowRepo
from repo.client_repo import ClientRepo

class TestHttpFlowRepo:
    def test_finding_a_flow_that_doesnt_exist(self, database, cleanup_database):
        session_factory = Database.get_instance().get_session_factory()
        http_flow_repo = HttpFlowRepo(session_factory)
        flow = http_flow_repo.find(0)

        assert flow is None

    def test_saving_a_flow_and_modifying_the_request(self, database, cleanup_database):
        session_factory = Database.get_instance().get_session_factory()
        http_flow_repo = HttpFlowRepo(session_factory)
        client_repo = ClientRepo(session_factory)

        # Create a Client
        client = Client(title="test client!", type="browser", proxy_port=8080, browser_port=None, launched_at=None)
        client_repo.save(client)

        # Set the flows request
        orig_request = HttpRequest(
            http_version="HTTP/2.0",
            headers="{}",
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/",
            form_data="{}",
            created_at=1
        )

        # Create a Flow with Request
        flow = HttpFlow(type="proxy", created_at=1, client=client, websocket_messages=[])
        http_flow_repo.save(flow, orig_request)

        modified_request = HttpRequest(
            http_version="HTTP/2.0",
            headers="{}",
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/modified",
            form_data="{}",
            created_at=1
        )
        http_flow_repo.add_modified_request(flow, modified_request)

        flow2 = http_flow_repo.find(flow.id)

        assert flow2 is not None
        assert flow2.request_id == modified_request.id
        assert flow2.original_request_id == orig_request.id
        assert flow2.client_id == client.id

    def test_adding_a_response_to_a_flow_and_adding_a_modified_response(self, database, cleanup_database):
        session_factory = Database.get_instance().get_session_factory()
        http_flow_repo = HttpFlowRepo(session_factory)

        client = Client(title="test client!", type="browser", proxy_port=8080, browser_port=None, launched_at=None)
        request = HttpRequest(
            http_version="HTTP/2.0",
            headers="{}",
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/",
            form_data="{}",
            created_at=1
        )

        # Create a Flow with Request
        flow = HttpFlow(type="proxy", created_at=1, client=client, websocket_messages=[])
        http_flow_repo.save(flow, request)

        # Add a response to the flow
        response = HttpResponse(
            http_version="HTTP/2.0",
            headers="{}",
            content="<html></html>",
            timestamp_start=1.0,
            timestamp_end=2.0,
            status_code=200,
            reason=None,
            created_at=1,
        )
        http_flow_repo.add_response(flow, response)

        flow2 = http_flow_repo.find(flow.id)
        assert flow2 is not None
        assert flow2.response_id is not None
        assert flow2.response_id == response.id

        # Add a modified response to the flow
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

        http_flow_repo.add_modified_response(flow, modified_response)

        flow3 = http_flow_repo.find(flow.id)
        assert flow3 is not None
        assert flow3.original_response_id is not None
        assert flow3.response_id is not None
        assert flow3.original_response_id == response.id
        assert flow3.response_id == modified_response.id

    def test_saving_a_flow_and_adding_a_websocket_message(self, database, cleanup_database):
        session_factory = Database.get_instance().get_session_factory()
        http_flow_repo = HttpFlowRepo(session_factory)

        # Create a Client
        client = Client(title="test client!", type="browser", proxy_port=8080, browser_port=None, launched_at=None)

        # Set the flows request
        request = HttpRequest(
            http_version="HTTP/2.0",
            headers="{}",
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/",
            form_data="{}",
            created_at=1
        )

        # Create a Flow with Request
        flow = HttpFlow(uuid="9c5d6853-bec8-4997-9d2f-daa27ce597f4", type="proxy", created_at=1, client=client, websocket_messages=[])
        http_flow_repo.save(flow, request)
        print("=================> FLOW ID ", flow.id)

        # Add a WebsocketMessage, THIS IS WHAT FAILS! http_flow.websocket_messages attribute doesnt work with sqlalchemy!
        ws_message = WebsocketMessage(http_flow_id=flow.id, direction="incoming", content="hello world", content_original=None, created_at=1)
        session = scoped_session(session_factory)
        session.add(ws_message)
        session.commit()
        session.refresh(ws_message)
        print("--> WS MESSAGE ID: ", ws_message.id)
        session.close()

        flow2 = http_flow_repo.find(flow.id)
        assert flow2 is not None

        print(flow.websocket_messages)
        # TODO
