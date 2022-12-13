import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field


from models.editor_item import EditorItem
from models.http_flow import HttpFlow
from repos.base_repo import BaseRepo
from repos.http_flow_repo import HttpFlowRepo

# Given a list of EditorItems, set the children property for each item recursively
class LoadChildrenOnEditorItems:
    editor_items: list[EditorItem]

    def __init__(self, editor_items: list[EditorItem]):
        self.editor_items = editor_items

    def run(self):
        root_items = [item for item in self.editor_items if item.parent_id is None]

        self.__add_children_to_items(root_items)

    def __add_children_to_items(self, editor_items: list[EditorItem]):
        for editor_item in editor_items:
            children = [item for item in self.editor_items if item.parent_id == editor_item.id]
            editor_item.children = children

            self.__add_children_to_items(children)

class EditorItemRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('editor_items')

    def find(self, id: int) -> Optional[EditorItem]:
        query = Query.from_(self.table).select('*').where(self.table.id == id)
        results = self.__find_by_query(query.get_sql())

        if len(results) == 0:
            return None
        return results[0]

    def find_all_with_children(self) -> list[EditorItem]:
        # TODO: Order by item_type, name
        query = Query.from_(self.table).select('*')
        editor_items = self.__find_by_query(query.get_sql())

        LoadChildrenOnEditorItems(editor_items).run()

        return editor_items

    def load_children_to_editor_item(self, editor_item: EditorItem):
        return

    def save(self, editor_item: EditorItem):
        # Set original_request_id from associated HttpRequest object and save if its not persisted
        if editor_item.item is not None:
            if editor_item.item.id == 0 and editor_item.item_is_flow():
                HttpFlowRepo().save(editor_item.item)
            editor_item.item_id = editor_item.item.id

        if editor_item.id > 0:
            self.generic_update(editor_item, self.table)
        else:
            self.generic_insert(editor_item, self.table)

    # Delete the EditorItem and all of its children, its childrens' children etc...
    def delete(self, editor_item: EditorItem):
        # TODO: Put all these operations in a transaction and rollback if any fail
        self.generic_delete(editor_item, self.table)

        for child in editor_item.children:
            self.generic_delete(child, self.table)

    def __find_by_query(self, sql_query: str) -> list[EditorItem]:
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        rows: list[sqlite3.Row] = cursor.fetchall()

        # Pre-load the associated HttpFlows from db in a single query
        http_flow_ids = [r['item_id'] for r in rows if r['item_id'] is not None and r['item_type'] in [EditorItem.TYPE_HTTP_FLOW, EditorItem.TYPE_FUZZ]]

        http_flows = HttpFlowRepo().find_by_ids(http_flow_ids)
        http_flows_by_id: dict[int, HttpFlow] = self.index_models_by_id(http_flows)

        # Instantiate the editor_items with their associated objects
        editor_items: list[EditorItem] = []
        for row in rows:
            row_values = self.row_to_dict(row)

            # Load Original Request
            if row_values['item_id'] is not None:
                row_values['item'] = http_flows_by_id[row_values['item_id']]

            editor_item = EditorItem(**row_values)
            editor_item.id = row['id']
            editor_item.created_at = row['created_at']
            editor_items.append(editor_item)

        return editor_items