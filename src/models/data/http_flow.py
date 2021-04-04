from orator import Model
from orator.orm import has_one
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse

class HttpFlow(Model):
    __table__ = 'http_flows'
    __fillable__ = ['*']

    @classmethod
    def find_for_table(cls):
        return cls.with_('request', 'response').order_by('id', 'desc').get()

    @has_one('id', 'request_id')
    def request(self):
        return HttpRequest

    @has_one('id', 'original_request_id')
    def original_request(self):
        return HttpRequest

    @has_one('id', 'response_id')
    def response(self):
        return HttpResponse

    @has_one('id', 'original_response_id')
    def original_response(self):
        return HttpResponse

    def request_modified(self):
        original_request_id = getattr(self, 'original_request_id', None)
        return original_request_id is not None

    def response_modified(self):
        original_response_id = getattr(self, 'original_response_id', None)
        return original_response_id is not None

    def modified(self):
        return self.request_modified() or self.response_modified()

    def values_for_table(self):
        if getattr(self, 'response_id', None):
            status_code = self.response.status_code
        else:
            status_code = None

        return [
            self.id,
            '',  # TODO: self.client_id,
            self.request.scheme,
            self.request.method,
            self.request.host,
            self.request.path,
            status_code,
            self.modified()
        ]
