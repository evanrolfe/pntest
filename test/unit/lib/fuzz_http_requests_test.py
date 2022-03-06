from lib.fuzz_http_requests import FuzzHttpRequests
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from support.factories import factory

class TestFuzzHttpRequests:
    def test_start(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'fuzz').create()

        # Hack: in order to call set_form_data
        http_request.reset_form_data()
        http_request.save()

        http_flow = factory(HttpFlow, 'editor_fuzz').create(request_id=http_request.id)

        fuzzer = FuzzHttpRequests(http_flow)
        fuzzer.start()

        assert 1 == 1
