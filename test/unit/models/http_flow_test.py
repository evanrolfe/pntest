from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from models.data.settings import Settings
from support.factories import factory
from proxy.common_types import ProxyResponse

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

    def test_find_for_table_host(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'proxy').make()
        http_request.save()

        http_flow = factory(HttpFlow, 'proxy').make(request_id=http_request.id, client_id=1)
        http_flow.save()

        Settings.create_defaults()
        settings = Settings.get()

        # Test including hosts
        settings.parsed()['display_filters']['host_list'] = ['synack.com']
        settings.parsed()['display_filters']['host_setting'] = 'include'
        settings.save()

        result = HttpFlow.find_for_table(None)
        assert len(result) == 1

        # Test excluding hosts
        settings.parsed()['display_filters']['host_list'] = ['synack.com']
        settings.parsed()['display_filters']['host_setting'] = 'exclude'
        settings.save()

        result = HttpFlow.find_for_table(None)
        assert len(result) == 0

    def test_update_from_proxy_response(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'proxy').make()
        http_request.save()

        http_flow = factory(HttpFlow, 'proxy').make(request_id=http_request.id, client_id=1, uuid='1234-abcd-1234-abcd')
        http_flow.save()

        proxy_response: ProxyResponse = {
            'http_version': 'HTTP/1.1',
            'headers': [('Date', 'Wed, 06 Jul 2022 08:19:18 GMT')],
            'content': b'<html>\r\n<head><title>301 Moved Permanently</title></head>\r\n<body>\r\n<center><h1>301 Moved Permanently</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n',
            'trailers': None,
            'timestamp_start': 1657095558.501397,
            'timestamp_end': 1657095558.502555,
            'status_code': 301,
            'reason': 'Moved Permanently',
            'flow_uuid': http_flow.uuid,
            'type': 'response',
            'intercepted': False
        }

        new_flow = HttpFlow.update_from_proxy_response(proxy_response)

        assert new_flow.id == http_flow.id
        # TODO: Write more assertions here
