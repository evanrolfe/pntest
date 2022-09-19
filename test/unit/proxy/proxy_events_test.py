from mitmproxy import http
from proxy.proxy_events import ProxyEvents
from proxy.common_types import SettingsJson

def generate_flow_state(host: str, port: int, path: str):
    return {
        'id': 'e6cb9237-647f-43bc-b296-1476137e5813',
        'error': None,
        'client_conn': {
            'address': ('127.0.0.1', 51570), 'alpn': None, 'cipher_name': None, 'id': '328150f4-c5a3-4ee4-b0fc-1f07e8849cab', 'mitmcert': None, 'sni': None, 'timestamp_end': None, 'timestamp_start': 1663443487.916821, 'timestamp_tls_setup': None, 'tls_established': False, 'tls_extensions': [], 'tls_version': None, 'state': 3, 'sockname': ('127.0.0.1', 8083), 'error': None, 'tls': False, 'certificate_list': [], 'alpn_offers': (), 'cipher_list': ()
        },
        'server_conn': {'address': None, 'alpn': None, 'id': 'ec8188aa-8913-4a36-950e-188a1b7817e1', 'ip_address': None, 'sni': None, 'source_address': None, 'timestamp_end': None, 'timestamp_start': None, 'timestamp_tcp_setup': None, 'timestamp_tls_setup': None, 'tls_established': False, 'tls_version': None, 'via': None, 'state': 0, 'error': None, 'tls': False, 'certificate_list': [], 'alpn_offers': (), 'cipher_name': None, 'cipher_list': (), 'via2': None},
        'type': 'http',
        'intercepted': False,
        'is_replay': None,
        'marked': '',
        'metadata': {},
        'comment': '',
        'request': {
            'http_version': b'HTTP/1.1',
            'headers': ((b'Host', b'www.synack.com'), (b'User-Agent', b'curl/7.79.1'), (b'Accept', b'*/*'), (b'Proxy-Connection', b'Keep-Alive')),
            'content': b'', 'trailers': None,
            'timestamp_start': 1663443487.919672,
            'timestamp_end': 1663443487.920376,
            'host': host,
            'port': port,
            'method': b'GET',
            'scheme': b'http',
            'authority': b'',
            'path': path
        },
        'response': None,
        'websocket': None,
        'mode': 'regular',
        'version': 14
    }

def generate_settings(host: str, setting: str) -> SettingsJson:
    return {
        "display_filters": {
            "host_list": [],
            "host_setting": "",
            "path_list": [],
            "path_setting": "",
        },
        "capture_filters": {
            "host_list": [host],
            "host_setting": setting,
            "path_list": [],
            "path_setting": "",
        },
        "proxy": {"ports_available": [8000]},
    }

class TestProxyEvents:
    def test_should_request_be_captured(self):
        proxy_events = ProxyEvents(1, "/Users/evan/Code/pntest/include")

        test_cases = [
            { 'setting_host': 'localhost', 'setting': 'include', 'host': 'localhost', 'port': 8000, 'expected': True },
            #{ 'setting_host': 'localhost:8000', 'setting': 'include', 'host': 'localhost', 'port': 8000, 'expected': True },
            #{ 'setting_host': 'http://localhost', 'setting': 'include', 'host': 'localhost', 'port': 8000, 'expected': False },
        ]

        for test_case in test_cases:
            settings = generate_settings(test_case['setting_host'], test_case['setting'])
            proxy_events.set_settings(settings)

            state = generate_flow_state(test_case['host'], test_case['port'], '/')
            flow = http.HTTPFlow.from_state(state)
            result = proxy_events.should_request_be_captured(flow)

            assert result == test_case['expected']
