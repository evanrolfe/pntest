from models.data.http_response import HttpResponse

class TestHttpResponse:
    def test_from_state_and_get_state(self, database, cleanup_database):
        state = {
            'http_version': 'HTTP/2.0',
            'headers': [['server', 'openresty'], ['date', 'Fri, 04 Feb 2022 09:54:33 GMT'], ['content-type', 'text/html'], ['content-length', '166'], ['location', 'https://www.wonderbill.com/']],
            'content': 'Moved Permanently',
            'trailers': None,
            'timestamp_start': 1643968473.0213363,
            'timestamp_end': 1643968473.0232053,
            'status_code': 301,
            'reason': '',
            'flow_uuid': 'fde275df-b173-4ea2-b38e-11c084305a6e',
            'type': 'response',
            'intercepted': False}

        response = HttpResponse.from_state(state)

        assert response.headers == '{"server": "openresty", "date": "Fri, 04 Feb 2022 09:54:33 GMT", "content-type": "text/html", "content-length": "166", "location": "https://www.wonderbill.com/"}'
        assert response.get_state()['headers'] == {
            'content-length': '166',
            'content-type': 'text/html',
            'date': 'Fri, 04 Feb 2022 09:54:33 GMT',
            'location': 'https://www.wonderbill.com/',
            'server': 'openresty'
        }
