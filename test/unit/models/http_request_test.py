from models.data.http_request import HttpRequest, FormData, FuzzFormData
from models.data.payload_file import PayloadFileSerialised
from support.factories import factory
from support.fixtures import build_an_editor_request_with_payloads

class TestHttpRequest:
    def test_from_state_and_get_state(self, database, cleanup_database):
        state = {
            'http_version': 'HTTP/2.0',
            'headers': [['user-agent', 'curl/7.68.0'], ['accept', '*/*']],
            'content': '',
            'trailers': None,
            'timestamp_start': 1643967316.7360358,
            'timestamp_end': 1643967316.7370074,
            'host': 'synack.com',
            'port': 443,
            'method': 'GET',
            'scheme': 'https',
            'authority': 'synack.com',
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
            host='synack.com',
            port=80,
            path='/index.html',
            scheme='http'
        )
        http_request.save()

        assert http_request.get_url() == 'http://synack.com/index.html'

    def test_get_url_https(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'editor').make(
            host='synack.com',
            port=443,
            path='/index.html',
            scheme='https'
        )
        http_request.save()

        assert http_request.get_url() == 'https://synack.com/index.html'

    def test_get_url_weird_port(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'editor').make(
            host='synack.com',
            port=1234,
            path='/index.html',
            scheme='http'
        )
        http_request.save()

        assert http_request.get_url() == 'http://synack.com:1234/index.html'

    def test_overwrite_calculated_headers(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'proxy').make(
            headers='{"Content-Length": 1234, "Host": "synack.com", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"}'
        )
        http_request.overwrite_calculated_headers()

        assert http_request.headers == '{"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"}'

    def test_payload_files(self, database, cleanup_database):
        payload1: PayloadFileSerialised = {
            'key': 'username',
            'file_path': 'usernames.txt',
            'num_items': 100,
            'description': 'THe usernames',
        }
        payload2: PayloadFileSerialised = {
            'key': 'password',
            'file_path': 'passwords.txt',
            'num_items': 100,
            'description': 'THe passwords',
        }

        form_data: FormData = {
            'method': '',
            'url': '',
            'headers': {},
            'content': '',
            'fuzz_data': {
                'payload_files': [payload1, payload2],
                'fuzz_type': HttpRequest.FUZZ_TYPE_KEYS[0],
                'delay_type': HttpRequest.DELAY_TYPE_KEYS[1],
            },
        }
        state = {
            'http_version': 'HTTP/2.0',
            'headers': [['user-agent', 'curl/7.68.0'], ['accept', '*/*']],
            'content': '',
            'trailers': None,
            'timestamp_start': 1643967316.7360358,
            'timestamp_end': 1643967316.7370074,
            'host': 'synack.com',
            'port': 443,
            'method': 'GET',
            'scheme': 'https',
            'authority': 'synack.com',
            'path': '/',
            'flow_uuid': '9c5d6853-bec8-4997-9d2f-daa27ce597f4',
            'type': 'request',
            'client_id': 1,
            'intercepted': False,
        }

        request = HttpRequest.from_state(state)
        request.set_form_data(form_data)
        payload_files = request.payload_files()

        assert 2 == len(payload_files)
        assert 'username' == payload_files[0].key
        assert 'password' == payload_files[1].key

    def test_payload_keys(self, database, cleanup_database):
        request = build_an_editor_request_with_payloads()
        payload_keys = request.payload_keys()

        assert payload_keys == ['username', 'password']
