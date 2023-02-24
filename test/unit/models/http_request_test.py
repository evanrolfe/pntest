import uuid
from entities.client import Client
from entities.http_flow import HttpFlow
from entities.http_request import FormData, HttpRequest
from services.http_flow_service import HttpFlowService
from repos.client_repo import ClientRepo
from support.factories.http_request_factory import HttpRequestFactory
from support.factories.http_response_factory import HttpResponseFactory

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
        client=client,
        request=HttpRequestFactory.build(path="/modified1"),
        original_request=HttpRequestFactory.build(path="/original1"),
        response=HttpResponseFactory.build(status_code=404, content="not found"),
        original_response=HttpResponseFactory.build(status_code=200, content="original"),
    )
    flow2 = HttpFlow(
        uuid=str(uuid.uuid4()),
        type="proxy",
        client=client,
        request=HttpRequestFactory.build(path="/modified2"),
        original_request= HttpRequestFactory.build(path="/original2"),
        response=HttpResponseFactory.build(status_code=200, content="<html>hello world</html>"),
        original_response=HttpResponseFactory.build(status_code=200, content="<html>original</html>"),
    )
    HttpFlowService().save(flow1)
    HttpFlowService().save(flow2)

    return [flow1, flow2]

class TestHttpRequest:
    def test_modify(self):
        request: HttpRequest = HttpRequestFactory.build(method="GET", path="/original", headers={"Host": "localhost"})
        request.modify("POST", "/modified", {"Host": "localhost:3000"}, "")

        assert request.method == "POST"
        assert request.path == "/modified"
        assert request.headers == {"Host": "localhost:3000"}
        assert request.content == ""
        assert request.host == "localhost"
        assert request.port == 3000

    def test_equality(self):
        request: HttpRequest = HttpRequestFactory.build(method="GET", path="/original", headers={"Host": "localhost"})
        request.id = 1
        new_request = request.duplicate()

        equal = new_request == request
        assert equal == True

        new_request.modify("GET", "/original", {"Host": "localhost:3000"}, "")
        equal = new_request == request
        assert equal == False
