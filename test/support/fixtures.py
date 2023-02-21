from entities.client import Client
from entities.http_flow import HttpFlow
from entities.http_request import HttpRequest, FormData
from entities.http_response import HttpResponse
from entities.variable import Variable
from entities.payload_file import PayloadFileSerialised
from mitmproxy.common_types import ProxyRequest
from repos.client_repo import ClientRepo
from services.http_flow_service import HttpFlowService
from repos.variable_repo import VariableRepo
from support.factories.http_request_factory import HttpRequestFactory
from support.factories.http_response_factory import HttpResponseFactory

def create_http_flow():
    client = Client(title="test client!", type="browser", proxy_port=8080)
    ClientRepo().save(client)

    http_flow = HttpFlow(
        type=HttpFlow.TYPE_PROXY,
        request=HttpRequestFactory.build(),
        response=HttpResponseFactory.build(),
    )
    HttpFlowService().save(http_flow)

def create_variables():
    var1 = Variable(key='host', value='localhost', source_type=Variable.SOURCE_TYPE_GLOBAL)
    var2 = Variable(key='apiVersion', value='v2', source_type=Variable.SOURCE_TYPE_GLOBAL)
    var3 = Variable(key='account_name', value='MyAccount', source_type=Variable.SOURCE_TYPE_GLOBAL)
    var4 = Variable(key='apiToken', value='0123456789', source_type=Variable.SOURCE_TYPE_GLOBAL)

    VariableRepo().save(var1)
    VariableRepo().save(var2)
    VariableRepo().save(var3)
    VariableRepo().save(var4)

def load_fixtures():
    create_http_flow()
    create_http_flow()
    create_variables()

def build_an_editor_flow_with_payloads() -> HttpFlow:
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
            'delay_secs': None,
            'delay_secs_min': None,
            'delay_secs_max': None,
        },
    }
    state: ProxyRequest = {
        'http_version': 'HTTP/2.0',
        'headers': [('user-agent', 'curl/7.68.0'), ('accept', '*/*')],
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

    http_flow = HttpFlow(type=HttpFlow.TYPE_EDITOR, request=request)

    return http_flow
