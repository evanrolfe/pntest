from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from support.factories import factory

class TestHttpFlow:
    def test_create_for_editor(self, database, cleanup_database):
        flow = HttpFlow.create_for_editor(HttpFlow.TYPE_EDITOR)

        assert flow.request is not None
        assert flow.type == HttpFlow.TYPE_EDITOR

    def test_values_for_table_no_response(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'proxy').make()
        http_request.save()

        http_flow = factory(HttpFlow, 'proxy').make(request_id=http_request.id, client_id=1)
        http_flow.save()

        result = http_flow.values_for_table()
        assert result == [http_flow.id, 1, 'http', 'GET', 'synack.com', '/', None, False]

    def test_duplicate_for_editor(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'proxy').make()
        http_request.save()

        http_flow = factory(HttpFlow, 'proxy').make(request_id=http_request.id, client_id=1)
        http_flow.save()

        new_flow = http_flow.duplicate_for_editor()

        assert new_flow.id != http_flow.id
        assert new_flow.id is not None
        assert new_flow.type == HttpFlow.TYPE_EDITOR
        assert new_flow.request_id != http_flow.request_id
        assert new_flow.request_id is not None

        assert new_flow.request.form_data['method'] == 'GET'
        assert new_flow.request.form_data['url'] == 'http://synack.com/'
        assert new_flow.request.form_data['headers'] == {"Host": "synack.com", "User-Agent": "curl/7.68.0", "Accept": "*/*", "Proxy-Connection": "Keep-Alive"}
        assert new_flow.request.form_data['content'] == ''

    def test_duplicate_for_example(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'editor').make()
        http_request.save()

        http_response = factory(HttpResponse, 'http_response').make()
        http_response.save()

        http_flow = factory(HttpFlow, 'editor').make(
            request_id=http_request.id,
            response_id=http_response.id,
            client_id=1
        )
        http_flow.save()

        new_flow = http_flow.duplicate_for_example(http_response)

        assert new_flow.type == HttpFlow.TYPE_EDITOR_EXAMPLE
        assert new_flow.request_id is not None
        assert new_flow.response_id == http_response.id
        assert new_flow.http_flow_id == http_flow.id

    def test_modify_request(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'editor').make()
        http_request.save()

        http_flow = factory(HttpFlow, 'editor').make(request_id=http_request.id, client_id=1)
        http_flow.modify_request('PATCH', '/modified', {"hello": "world"}, 'asdf')

        assert http_flow.original_request_id == http_request.id
        assert http_flow.request_id != http_request.id
        assert http_flow.request_id is not None

    def test_modify_response(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'editor').make()
        http_request.save()

        http_response = factory(HttpResponse, 'http_response').make()
        http_response.save()

        http_flow = factory(HttpFlow, 'editor').make(
            request_id=http_request.id,
            response_id=http_response.id,
            client_id=1
        )
        http_flow.modify_response(203, {"hello": "world"}, 'Somethings-changed')

        assert http_flow.original_response_id == http_response.id
        assert http_flow.response_id != http_response.id
        assert http_flow.response_id is not None

    def test_modify_latest_websocket_message(self, database, cleanup_database):
        # TODO:
        assert 1 == 1

