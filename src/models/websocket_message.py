from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from models.model import Model
from proxy.common_types import ProxyWebsocketMessage

@dataclass(kw_only=True)
class WebsocketMessage(Model):
    # Columns
    id: int = field(init=False, default=0)
    http_flow_id: int
    direction: str
    content: str
    content_original: Optional[str]
    created_at: int

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": [],
    }

    @classmethod
    def from_state(cls, state: ProxyWebsocketMessage):
        message = WebsocketMessage(
            http_flow_id=0,
            direction=state['direction'],
            content=state['content'],
            content_original=None,
            created_at=1,
        )

        return message

    def modified(self):
        content_original = getattr(self, 'content_original', None)

        if content_original is not None:
            return 'Yes'
        else:
            return ''
