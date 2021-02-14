from orator.orm import Factory
from models.data.client import Client
from models.data.crawl import Crawl
from models.data.editor_item import EditorItem
from models.data.editor_request import EditorRequest
from models.data.network_request import NetworkRequest

factory = Factory()

@factory.define(Client)
def client_factory(faker):
    return {
        'title': 'Browser #1',
        'type': 'chromium',
        'pages': '[]',
        'cookies': '[]',
        'proxy_port': 8080,
        'browser_port': 9222,
        'open': 0
    }

@factory.define(Crawl)
def crawl_factory(faker):
    return {
        'config': '{}',
        'status': 'finished',
    }

@factory.define_as(EditorItem, 'request')
def editor_item_factory_request(faker):
    return {
        'name': 'Login request',
        'item_type': 'request',
        'item_id': 1
    }

@factory.define_as(EditorItem, 'dir')
def editor_item_factory_dir(faker):
    return {
        'name': 'My requests',
        'item_type': 'dir'
    }

@factory.define(EditorRequest)
def editor_request_factory(faker):
    return {
        'method': 'GET',
        'url': 'http://example.com',
        'request_headers': '{"host": "example.com", "content-length": 123, "accept": "*/*", "accept-encoding": "gzip, deflate", "connection": "keep-alive"}', # noqa
        'request_payload': None
    }

@factory.define(NetworkRequest)
def network_request_factory(faker):
    return {
        'client_id': 1,
        'method': 'GET',
        'host': 'example.com',
        'path': '/',
        'encrypted': 0,
        'http_version': '1.1',
        'request_headers': '{"host": "example.com", "content-length": 123, "accept": "*/*", "accept-encoding": "gzip, deflate", "connection": "keep-alive"}', # noqa
        'request_payload': None,
        'request_type': 'http',
    }
