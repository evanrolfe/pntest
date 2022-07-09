from __future__ import annotations
from typing import Optional

from PyQt6 import QtGui
from models.data.orator_model import OratorModel
from models.data.http_flow import HttpFlow

class EditorItem(OratorModel):
    # Database columns:
    id: int
    parent_id: Optional[int]
    name: str
    item_type: str
    item_id: Optional[int]
    created_at: Optional[int]
    updated_at: Optional[int]

    # Associations:

    # Constants:
    TYPE_HTTP_FLOW: str
    TYPE_DIR: str
    TYPE_FUZZ: str

    def icon(self) -> Optional[QtGui.QIcon]:
        pass

    def children(self) -> list[EditorItem]:
        pass

    def duplicate(self) -> Optional[EditorItem]:
        pass

    def delete_everything(self) -> None:
        pass

    def delete_resursive(self) -> None:
        pass

    def item(self) -> Optional[HttpFlow]:
        pass

    def save(self, *args, **kwargs):
        pass

    @classmethod
    def create_for_http_flow(cls, flow):
        pass
