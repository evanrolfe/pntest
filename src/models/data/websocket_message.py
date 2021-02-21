from orator import Model

class WebsocketMessage(Model):
    __table__ = 'websocket_messages'
    __fillable__ = ['*']
