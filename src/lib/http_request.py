from typing import Optional
from requests import Request, Response, Session
from lib.types import Headers
from constants import CALCULATED_TEXT

class HttpRequest:
    method: str
    url: str
    headers: Headers
    body: Optional[str]

    def __init__(self, method: str, url: str, headers: Headers, body: Optional[str]):
        self.method = method
        self.url = url
        self.headers = headers
        if body:
            self.body = body

    def send(self) -> Response:
        print(f'Requesting {self.method} {self.url}')
        session = Session()
        body = getattr(self, 'body', None)
        request = Request(self.method, self.url, headers=self.parsed_headers(), data=body)
        prepped_request = session.prepare_request(request)

        self.response = session.send(prepped_request, timeout=30, verify=False, allow_redirects=False)
        return self.response

    def parsed_headers(self) -> Headers:
        parsed_headers = {}

        for key, value in self.headers.items():
            if value != CALCULATED_TEXT:
                parsed_headers[key] = value

        return parsed_headers

