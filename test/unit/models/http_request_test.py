from models.data.http_request import HttpRequest
from support.factories import factory

class TestHttpRequest:
    def test_from_state_and_get_state(self, database, cleanup_database):
        state = {
            'http_version': 'HTTP/2.0',
            'headers': [['user-agent', 'curl/7.68.0'], ['accept', '*/*']],
            'content': '',
            'trailers': None,
            'timestamp_start': 1643967316.7360358,
            'timestamp_end': 1643967316.7370074,
            'host': 'wonderbill.com',
            'port': 443,
            'method': 'GET',
            'scheme': 'https',
            'authority': 'wonderbill.com',
            'path': '/',
            'flow_uuid': '9c5d6853-bec8-4997-9d2f-daa27ce597f4',
            'type': 'request',
            'client_id': 1,
            'intercepted': False
        }

        request = HttpRequest.from_state(state)

        assert request.headers == '{"user-agent": "curl/7.68.0", "accept": "*/*"}'
        assert request.get_state()['headers'] == {'user-agent': 'curl/7.68.0', 'accept': '*/*'}

    def test_get_url_http(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'editor').make(
            host='wonderbill.com',
            port=80,
            path='/index.html',
            scheme='http'
        )
        http_request.save()

        assert http_request.get_url() == 'http://wonderbill.com/index.html'

    def test_get_url_https(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'editor').make(
            host='wonderbill.com',
            port=443,
            path='/index.html',
            scheme='https'
        )
        http_request.save()

        assert http_request.get_url() == 'https://wonderbill.com/index.html'

    def test_get_url_weird_port(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'editor').make(
            host='wonderbill.com',
            port=1234,
            path='/index.html',
            scheme='http'
        )
        http_request.save()

        assert http_request.get_url() == 'http://wonderbill.com:1234/index.html'

    def test_overwrite_calculated_headers(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'proxy').make(
            headers='{"Content-Length": 1234, "Host": "wonderbill.com", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"}'
        )
        http_request.overwrite_calculated_headers()

        assert http_request.headers == '{"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"}'
