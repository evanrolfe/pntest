import re
from copy import deepcopy
from requests import Request, Response, Session
from widgets.shared.headers_form import HeadersForm, Headers
from models.data.variable import Variable

class HttpRequest:
    method: str
    url: str
    headers: Headers
    body: str

    def __init__(self, method: str, url: str, headers: Headers, body: str):
        self.method = self.replace_variables(method)
        self.url = self.replace_variables(url)
        self.headers = self.replace_variables_in_headers(headers)
        self.body = self.replace_variables(body)

    def send(self) -> Response:
        print(f'Requesting {self.method} {self.url}')
        session = Session()
        request = Request(self.method, self.url, headers=self.parsed_headers(), data=self.body)
        prepped_request = session.prepare_request(request)

        self.response = session.send(prepped_request, timeout=30)
        return self.response

    def parsed_headers(self) -> Headers:
        parsed_headers = {}

        for key, value in self.headers.items():
            if value != HeadersForm.CALCULATED_TEXT:
                parsed_headers[key] = value

        return parsed_headers

    def replace_variables_in_headers(self, headers: Headers) -> Headers:
        new_headers = deepcopy(headers)

        for key, value in new_headers.items():
            new_headers[key] = self.replace_variables(value)

        return new_headers

    def replace_variables(self, value: str) -> str:
        for match in re.finditer(r'\${var:(\w+)\}', value):
            key = match[1]
            var = Variable.find_by_key(key)

            if var:
                new_value = var.value
            else:
                new_value = ''

            value = value.replace(match[0], new_value)

        return value
