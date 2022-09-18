from typing import Optional
from models.data.orator_model import OratorModel

class WebsocketMessage(OratorModel):
    id: int
    http_flow_id: int
    direction: str
    content: str
    content_original: Optional[str]
    created_at: int

    __table__ = 'websocket_messages'
    __fillable__ = ['*']
    __timestamps__ = False

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
