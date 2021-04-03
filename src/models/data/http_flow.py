from orator import Model

class HttpFlow(Model):
    __table__ = 'http_flows'
    __fillable__ = ['*']
