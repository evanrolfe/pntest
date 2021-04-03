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
