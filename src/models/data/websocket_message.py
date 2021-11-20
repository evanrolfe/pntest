from orator import Model

class WebsocketMessage(Model):
    __table__ = 'websocket_messages'
    __fillable__ = ['*']

    @classmethod
    def from_state(cls, state):
        message = WebsocketMessage()

        message.direction = state['direction']
        message.content = state['content']

        return message

    def modified(self):
        content_original = getattr(self, 'content_original', None)

        if content_original is not None:
            return 'Yes'
        else:
            return ''
