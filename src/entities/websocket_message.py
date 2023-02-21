from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from entities.model import Model
from mitmproxy.common_types import ProxyWebsocketMessage

@dataclass(kw_only=True)
class WebsocketMessage(Model):
    # Columns
    id: int = field(init=False, default=0)
    created_at: int = field(init=False, default=0)

    http_flow_id: int
    direction: str
    content: str
    content_original: Optional[str]

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": [],
        "do_not_save_keys": [],
    }

    @classmethod
    def from_state(cls, state: ProxyWebsocketMessage):
        message = WebsocketMessage(
            http_flow_id=0,
            direction=state['direction'],
            content=state['content'],
            content_original=None,
        )

        return message

    def modified(self):
        content_original = getattr(self, 'content_original', None)

        if content_original is not None:
            return 'Yes'
        else:
            return ''
