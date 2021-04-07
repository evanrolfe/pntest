import json
from orator import Model

class HttpRequest(Model):
    __table__ = 'http_requests'
    __fillable__ = ['*']

    @classmethod
    def from_state(cls, state):
        request = HttpRequest()
        request.http_version = state['http_version']
        request.headers = json.dumps(dict(state['headers']))
        request.content = state['content']
        request.trailers = state['trailers']
        request.timestamp_start = state['timestamp_start']
        request.timestamp_end = state['timestamp_end']
        request.host = state['host']
        request.port = state['port']
        request.method = state['method']
        request.scheme = state['scheme']
        request.authority = state['authority']
        request.path = state['path']

        return request

    def get_state(self):
        attributes = self.serialize()
        attributes['headers'] = json.loads(attributes['headers'])
        return attributes

    def get_headers(self):
        if self.headers is None:
            return None
        return json.loads(self.headers)

    def get_method_path(self):
        return f'{self.method} {self.path}'

    def get_header_line(self):
        return f'{self.method} {self.path} {self.http_version}'

    def get_url(self):
        if self.port not in [80, 443]:
            port = ':' + str(self.port)
        else:
            port = ''

        return f'{self.scheme}://{self.host}{port}{self.path}'
