import factory

from models.http_request import FormData, HttpRequest

def generate_form_data(request: HttpRequest) -> FormData:
    return {
        "method": request.method,
        "url": request.scheme + "://" + request.host + request.path,
        "headers": {"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"},
        "content": '{ "username": "${payload:usernames}", "password": "${payload:passwords}" }',
        "fuzz_data": None,
    }

class HttpRequestFactory(factory.Factory):
    class Meta:
        model = HttpRequest

    http_version="HTTP/2.0"
    headers={}
    host="synack.com"
    port=80
    method="GET"
    scheme="http"
    path="/ORIGINAL"
    form_data=factory.LazyAttribute(generate_form_data)
    created_at=1

