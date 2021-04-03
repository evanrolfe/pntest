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

    @has_one('id', 'response_id')
    def response(self):
        return HttpResponse

    def modified(self):
        return False

    @classmethod
    def find_for_table(cls):
        return cls.with_('request', 'response').order_by('id', 'desc').get()
