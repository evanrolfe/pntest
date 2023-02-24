from entities.client import Client
from entities.http_flow import HttpFlow
from entities.http_request import FormData, HttpRequest
from entities.websocket_message import WebsocketMessage
from services.http_flow_service import HttpFlowService
from repos.ws_message_repo import WsMessageRepo
from repos.client_repo import ClientRepo

example_form_data: FormData = {
    "method": "GET",
    "url": "http://www.synack.com/login.php",
    "headers": {"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"},
    "content": '{ "username": "${payload:usernames}", "password": "${payload:passwords}" }',
    "fuzz_data": None,
}

class TestWsMessageRepo:
    def test_fetching_all_messages(self, database, cleanup_database):
        ws_message_repo = WsMessageRepo()

        # 1. Create a Client, HttpFlow with HttpRequest and WebsocketMessage
        http_flow_repo = HttpFlowService()
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
        )
        flow = HttpFlow(type="proxy", client=client, request=request)
        http_flow_repo.save(flow)

        ws_message1 = WebsocketMessage(
            http_flow_id=0,
            direction="incoming",
            content="hello world",
            content_original=None,
        )
        ws_message2 = WebsocketMessage(
            http_flow_id=0,
            direction="outgoing",
            content="hello, back at you",
            content_original=None,
        )
        flow.add_ws_message(ws_message1)
        flow.add_ws_message(ws_message2)
        http_flow_repo.save(flow)

        # 2. Find all WebsocketMessages
        result = ws_message_repo.find_for_table('')

        assert len(result) == 2
