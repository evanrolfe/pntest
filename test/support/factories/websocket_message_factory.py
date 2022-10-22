import factory

from models.websocket_message import WebsocketMessage

class WebsocketMessageFactory(factory.Factory):
    class Meta:
        model = WebsocketMessage

    http_flow_id=0
    direction="incoming"
    content="hello world"
    content_original=None
    created_at=1
