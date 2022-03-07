from lib.fuzz_http_requests import FuzzHttpRequests
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from lib.background_worker import WorkerSignals
from support.factories import factory

class TestFuzzHttpRequests:
    def test_start(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'fuzz').create()

        # Hack: in order to call set_form_data
        http_request.reset_form_data()
        http_request.save()

        http_flow = factory(HttpFlow, 'editor_fuzz').create(request_id=http_request.id)

        signals = WorkerSignals()
        fuzzer = FuzzHttpRequests(http_flow)
        fuzzer.start(signals)

        http_flow = http_flow.reload()
        examples = http_flow.examples

        assert examples[0].request.content == '{ "username": "pntest", "password": "password1" }'
        assert examples[1].request.content == '{ "username": "alice", "password": "Password1" }'
        assert examples[2].request.content == '{ "username": "bob", "password": "password123" }'
        assert examples[3].request.content == '{ "username": "evan", "password": "Password1#" }'

        assert examples[0].response.status_code == 404
        assert examples[1].response.status_code == 404
        assert examples[2].response.status_code == 404
        assert examples[3].response.status_code == 404

        print([e.title for e in examples])
