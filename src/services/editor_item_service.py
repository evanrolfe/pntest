from __future__ import annotations
from typing import Any, Optional
from entities.client import Client
from entities.editor_item import EditorItem
from entities.http_flow import HttpFlow
from entities.http_request import HttpRequest
from entities.http_response import HttpResponse
from repos.client_repo import ClientRepo
from repos.editor_item_repo import EditorItemRepo
from repos.http_flow_repo import HttpFlowRepo
from repos.http_request_repo import HttpRequestRepo
from repos.http_response_repo import HttpResponseRepo
from repos.ws_message_repo import WsMessageRepo
from services.http_flow_service import HttpFlowService

class EditorItemService():
    def __init__(self):
        super().__init__()

    def find(self, id: int) -> Optional[EditorItem]:
        editor_item = EditorItemRepo().find(id)
        if editor_item is None:
            return None

        self.__load_associations([editor_item])
        return editor_item

    def find_all_with_children(self) -> list[EditorItem]:
        editor_items = EditorItemRepo().find_all_with_children()

        self.__load_associations(editor_items)
        return editor_items

    def save(self, editor_item: EditorItem):
        # Set original_request_id from associated HttpRequest object and save if its not persisted
        if editor_item.item is not None:
            if editor_item.item.id == 0 and editor_item.item_is_flow():
                HttpFlowService().save(editor_item.item)
            editor_item.item_id = editor_item.item.id

        EditorItemRepo().save(editor_item)

    # Delete the EditorItem and all of its children, its childrens' children etc...
    def delete(self, editor_item: EditorItem):
        # TODO: THIS SHOULD ALSO DELETE ITS HTTP_FLOW/REQUEST/RESPONSES!!!
        EditorItemRepo().delete(editor_item)

    def __load_associations(self,
        editor_items: list[EditorItem],
        *,
        load_examples = False,
        load_minimal_response_data = True
    ):
        # Pre-load the associated HttpFlows from db in a single query
        http_flow_ids = [item.item_id for item in editor_items if item.item_id is not None and item.item_type in [EditorItem.TYPE_HTTP_FLOW, EditorItem.TYPE_FUZZ]]
        http_flows = HttpFlowService().find_by_ids(http_flow_ids)
        http_flows_by_id: dict[int, HttpFlow] = self.__index_models_by_id(http_flows)

        for editor_item in editor_items:
            if editor_item.item_id is not None:
                editor_item.item = http_flows_by_id.get(editor_item.item_id)

    def __index_models_by_id(self, models: list[Any]) -> dict[int, Any]:
        indexed_models = {}
        for model in models:
            indexed_models[model.id] = model

        return indexed_models
