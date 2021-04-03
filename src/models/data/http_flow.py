from orator import Model
from orator.orm import has_one
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse

class HttpFlow(Model):
    __table__ = 'http_flows'
    __fillable__ = ['*']

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
        return self.original_request_id is not None

    def response_modified(self):
        return self.original_response_id is not None

    def modified(self):
        return self.request_modified() or self.response_modified()

    @classmethod
    def find_for_table(cls):
        return cls.with_('request', 'response').order_by('id', 'desc').get()
