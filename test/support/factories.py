from orator.orm import Factory
from models.data.client import Client
from models.data.editor_item import EditorItem
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from models.data.variable import Variable

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

@factory.define_as(EditorItem, 'request')
def editor_item_factory_request(faker):
    return {
        'name': 'Login request',
        'item_type': EditorItem.TYPE_HTTP_FLOW,
        'item_id': 1
    }

@factory.define_as(EditorItem, 'dir')
def editor_item_factory_dir(faker):
    return {
        'name': 'My requests',
        'item_type': EditorItem.TYPE_DIR
    }

@factory.define_as(HttpFlow, 'proxy')
def http_flow_proxy(faker):
    return {
        'type': HttpFlow.TYPE_PROXY,
    }

@factory.define_as(HttpFlow, 'editor')
def http_flow_editor(faker):
    return {
        'type': HttpFlow.TYPE_EDITOR,
    }

@factory.define_as(HttpRequest, 'proxy')
def http_request_proxy(faker):
    return {
        'http_version': 'HTTP/1.1',
        'headers': '{"Host": "wonderbill.com", "User-Agent": "curl/7.68.0", "Accept": "*/*", "Proxy-Connection": "Keep-Alive"}',
        'timestamp_start': 1641555291.54401,
        'timestamp_end': 1641555291.54628,
        'host': 'wonderbill.com',
        'port': 80,
        'method': 'GET',
        'scheme': 'http',
        'path': '/',
        'form_data': {"method": "GET", "url": "http://wonderbill.com/", "headers": {"Host": "wonderbill.com", "User-Agent": "curl/7.68.0", "Accept": "*/*", "Proxy-Connection": "Keep-Alive"}, "body": ""}
    }

@factory.define_as(HttpRequest, 'editor')
def http_request_editor(faker):
    return {
        'http_version': 'HTTP/1.1',
        'headers': '{"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"}',
        'timestamp_start': 1641555291.54401,
        'timestamp_end': 1641555291.54628,
        'host': 'wonderbill.com',
        'port': 80,
        'method': 'GET',
        'scheme': 'http',
        'path': '/',
        'form_data': {"method": "GET", "url": "http://wonderbill.com/", "headers": {"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"}, "body": ""}
    }

@factory.define_as(HttpResponse, 'http_response')
def http_response(faker):
    return {
        'http_version': 'HTTP/1.1',
        'headers': '{"Cache-Control": "no-cache, no-store", "Content-Length": "57", "Content-Type": "application/json", "MS-CV": "Fi5N4PgVHUS1BTxUimu7kA.0", "X-Content-Type-Options": "nosniff", "Date": "Fri, 07 Jan 2022 14:58:33 GMT", "Connection": "close"}',
        'content': '{"ipv":false,"pvm":null,"rej":0,"bln":0,"acc":1,"efi":[]}',
        'timestamp_start': 1641567513.68341,
        'timestamp_end': 1641567513.6862,
        'status_code': 200,
        'reason': 'OK',
    }

@factory.define_as(Variable, 'global')
def variable_factory_global(faker):
    return {
        'key': 'host',
        'value': 'localhost',
        'source_type': Variable.SOURCE_TYPE_GLOBAL,
        'description': 'just a variable for testing'
    }
