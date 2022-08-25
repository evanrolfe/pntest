from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest, FormData
from models.data.http_response import HttpResponse
from models.data.variable import Variable
from models.data.payload_file import PayloadFileSerialised

from support.factories import factory

def create_http_flow():
    http_request = factory(HttpRequest, 'proxy').make()
    http_request.save()

    http_response = factory(HttpResponse, 'http_response').make()
    http_response.save()

    http_flow = factory(HttpFlow, 'proxy').make(
        request_id=http_request.id,
        response_id=http_response.id,
        client_id=1
    )
    http_flow.save()

def create_variables():
    factory(Variable, 'global').create(key='host', value='localhost')
    factory(Variable, 'global').create(key='apiVersion', value='v2')
    factory(Variable, 'global').create(key='account_name', value='MyAccount')
    factory(Variable, 'global').create(key='apiToken', value='0123456789')

def load_fixtures():
    create_http_flow()
    create_http_flow()
    create_variables()

def build_an_editor_request_with_payloads() -> HttpRequest:
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
    return request
