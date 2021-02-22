from orator import Model

class WebsocketMessage(Model):
    __table__ = 'websocket_messages'
    __fillable__ = ['*']

    def modified(self):
        if self.body_modified is not None:
            return 'Yes'
        else:
            return ''
