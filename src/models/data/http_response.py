import json
from orator import Model

class HttpResponse(Model):
    __table__ = 'http_responses'
    __fillable__ = ['*']

    @classmethod
    def from_state(cls, state):
        response = HttpResponse()

        response.http_version = state['http_version']
        response.headers = json.dumps(dict(state['headers']))
        response.content = state['content']
        response.timestamp_start = state['timestamp_start']
        response.timestamp_end = state['timestamp_end']
        response.status_code = state['status_code']
        response.reason = state['reason']

        return response

    @classmethod
    def from_requests_response(cls, requests_response):
        response_model = HttpResponse()
        response_model.content = requests_response.text
        response_model.status_code = requests_response.status_code
        response_model.reason = requests_response.reason
        response_model.set_headers(dict(requests_response.headers))

        if requests_response.raw.version == 11:
            response_model.http_version = 'HTTP/1.1'
        elif requests_response.raw.version == 10:
            response_model.http_version = 'HTTP/1.0'

        return response_model

    def get_state(self):
        attributes = self.serialize()
        attributes['headers'] = json.loads(attributes['headers'])
        return attributes

    def set_headers(self, headers):
        self.headers = json.dumps(headers)

    def get_headers(self):
        if self.headers is None:
            return None
        return json.loads(self.headers)

    def get_header_line(self):
        return f'{self.http_version} {self.status_code} {self.reason}'

    def get_header_line_no_http_version(self):
        return f'{self.status_code} {self.reason}'

    def content_for_preview(self):
        return self.content
