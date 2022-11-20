from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from models.http_flow import HttpFlow
from models.model import Model

@dataclass(kw_only=True)
class EditorItem(Model):
    # Columns
    id: int = field(init=False, default=0)
    created_at: int = field(init=False, default=0)

    parent_id: Optional[int] = field(default=None)
    name: str
    item_type: str
    item_id: Optional[int] = field(default=None)

    # Relations
    item: Optional[HttpFlow] = None
    children: list[EditorItem] = field(default_factory=lambda: [])

    meta = {
        "relationship_keys": ["item", "children"],
        "json_columns": [],
        "do_not_save_keys": [],
    }

    TYPE_HTTP_FLOW = 'http_flow'
    TYPE_DIR = 'dir'
    TYPE_FUZZ = 'fuzz'

    # When creating an EditorItem, if the type is a flow or fuzz, then we automatically create
    # a blank HttpFlow+Request for the editor tab to use
    def build_blank_http_flow(self):
        if self.item_is_flow() and self.item_id is None:
            if self.item_type == self.TYPE_FUZZ:
                type = HttpFlow.TYPE_EDITOR_FUZZ
            else:
                type = HttpFlow.TYPE_EDITOR

            self.item = HttpFlow.build_blank_for_editor(type)

    @classmethod
    def build_for_http_flow(cls, flow: HttpFlow):
        return EditorItem(
            name = 'new request',
            item_type = cls.TYPE_HTTP_FLOW,
            item_id = flow.id,
            item = flow
        )

    def item_is_flow(self) -> bool:
        return self.item_type in [self.TYPE_HTTP_FLOW, self.TYPE_FUZZ]

    def duplicate(self) -> Optional[EditorItem]:
        if self.item_type != self.TYPE_HTTP_FLOW:
            print('WARNING - cannot duplicate editor items which arent http_flows')
            return

        original_flow = self.item
        if original_flow is None:
            return

        flow = original_flow.duplicate_for_editor()

        return EditorItem(
            name = self.name,
            item_type = self.item_type,
            item = flow
        )
