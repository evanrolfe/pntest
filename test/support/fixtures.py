from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse

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

def load_fixtures():
    create_http_flow()
    create_http_flow()