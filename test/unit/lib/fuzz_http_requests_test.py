from pytest_httpserver import HTTPServer

from lib.fuzz_http_requests import FuzzHttpRequests
from models.http_flow import HttpFlow
from models.http_request import HttpRequest, FormData
from lib.background_worker import WorkerSignals
from services.http_flow_service import HttpFlowService
from support.factories.http_request_factory import HttpRequestFactory
from support.factories.http_response_factory import HttpResponseFactory
from support.factories.websocket_message_factory import WebsocketMessageFactory

class TestFuzzHttpRequests:
    def test_fuzzing_one_to_one(self, database, cleanup_database, httpserver: HTTPServer):
        httpserver.expect_request("/login.php", "POST").respond_with_data("{}")

        http_request = HttpRequestFactory.build(
            http_version = 'HTTP/1.1',
            timestamp_start = 1641555291.54401,
            timestamp_end = 1641555291.54628,
        )
        http_request.set_form_data({
            "method": "POST",
            "url": httpserver.url_for("/login.php"),
            "headers": {"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"},
            "content": '{ "username": "${payload:usernames}", "password": "${payload:passwords}" }',
            "fuzz_data": {
                "payload_files": [
                    {'file_path': './test/support/usernames.txt', 'key': 'usernames', 'num_items': 2, 'description': ''},
                    {'file_path': './test/support/passwords.txt', 'key': 'passwords', 'num_items': 2, 'description': ''}
                ],
                "fuzz_type": HttpRequest.FUZZ_TYPE_KEYS[0],
                "delay_type": "disabled",
                "delay_secs": None,
                "delay_secs_min": None,
                "delay_secs_max": None,
            }
        })

        http_flow = HttpFlow(
            type=HttpFlow.TYPE_EDITOR_FUZZ,
            request=http_request,
        )
        HttpFlowService().save(http_flow)

        signals = WorkerSignals()
        fuzzer = FuzzHttpRequests(http_flow)
        fuzzer.start(signals)

        examples = http_flow.examples

        assert examples[0].request.content == '{ "username": "alice", "password": "password1" }'
        assert examples[1].request.content == '{ "username": "bob", "password": "Password1" }'

        assert examples[0].response is not None
        assert examples[0].response.status_code == 200
        assert examples[1].response is not None
        assert examples[1].response.status_code == 200

    def test_fuzzing_cartesian(self, database, cleanup_database, httpserver: HTTPServer):
        httpserver.expect_request("/login.php", "POST").respond_with_data("{}")

        http_request = HttpRequestFactory.build(
            http_version = 'HTTP/1.1',
            timestamp_start = 1641555291.54401,
            timestamp_end = 1641555291.54628,
        )
        http_request.set_form_data({
            "method": "POST",
            "url": httpserver.url_for("/login.php"),
            "headers": {"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"},
            "content": '{ "username": "${payload:usernames}", "password": "${payload:passwords}" }',
            "fuzz_data": {
                "payload_files": [
                    {'file_path': './test/support/usernames.txt', 'key': 'usernames', 'num_items': 2, 'description': ''},
                    {'file_path': './test/support/passwords.txt', 'key': 'passwords', 'num_items': 2, 'description': ''}
                ],
                "fuzz_type": HttpRequest.FUZZ_TYPE_KEYS[1],
                "delay_type": "disabled",
                "delay_secs": None,
                "delay_secs_min": None,
                "delay_secs_max": None,
            }
        })

        http_flow = HttpFlow(
            type=HttpFlow.TYPE_EDITOR_FUZZ,
            request=http_request,
        )
        HttpFlowService().save(http_flow)

        signals = WorkerSignals()
        fuzzer = FuzzHttpRequests(http_flow)
        fuzzer.start(signals)

        examples = http_flow.examples

        assert examples[0].request.content == '{ "username": "alice", "password": "password1" }'
        assert examples[1].request.content == '{ "username": "alice", "password": "Password1" }'
        assert examples[2].request.content == '{ "username": "alice", "password": "" }'

        assert examples[3].request.content == '{ "username": "bob", "password": "password1" }'
        assert examples[4].request.content == '{ "username": "bob", "password": "Password1" }'
        assert examples[5].request.content == '{ "username": "bob", "password": "" }'

        assert examples[6].request.content == '{ "username": "", "password": "password1" }'
        assert examples[7].request.content == '{ "username": "", "password": "Password1" }'
        assert examples[8].request.content == '{ "username": "", "password": "" }'

        print([e.title for e in examples])
