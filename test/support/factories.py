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

@factory.define_as(NetworkRequest, 'with_response')
def network_request_factory_with_response(faker):
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
        'response_body_rendered': '<h1>Hello world</h1>',
        'response_http_version': '1.1',
        'response_status': 200,
        'response_status_message': 'OK',
        'response_headers': '{"server":"nginx","date":"Sun, 31 Jan 2021 11:48:32 GMT","content-type":"text/html","content-length":"20","via":"1.1 google","age":"7074","cache-control":"public, must-revalidate, max-age=0, s-maxage=86400"}', # noqa
        'response_body': '<h1>Hello world</h1>',
        'response_body_length': 0,
        'response_modified': 0,
    }
    #   modified_response_status INTEGER,
    #   modified_response_status_message TEXT,
    #   modified_response_headers TEXT,
    #   modified_response_body TEXT,
    #   modified_response_body_length INTEGER,
    #   modified_response_http_version TEXT,
