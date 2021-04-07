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

    def get_state(self):
        attributes = self.serialize()
        attributes['headers'] = json.loads(attributes['headers'])
        return attributes

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
