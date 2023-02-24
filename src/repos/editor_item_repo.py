import sqlite3
from typing import Any, Optional
from pypika import QmarkParameter, Query, Table


from entities.editor_item import EditorItem, LoadChildrenOnEditorItems
from repos.base_repo import BaseRepo

class EditorItemRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('editor_items')

    def find(self, id: int) -> Optional[EditorItem]:
        query = Query.from_(self.table).select('*').where(self.table.id == QmarkParameter())
        results = self.__find_by_query(query.get_sql(), [id])

        if len(results) == 0:
            return None
        return results[0]

    def find_all_with_children(self) -> list[EditorItem]:
        # TODO: Order by item_type, name
        query = Query.from_(self.table).select('*')
        editor_items = self.__find_by_query(query.get_sql(), [])

        LoadChildrenOnEditorItems(editor_items).run()

        return editor_items

    def save(self, editor_item: EditorItem):
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

    def __find_by_query(self, sql_query: str, sql_params: list[Any]) -> list[EditorItem]:
        cursor = self.conn.cursor()
        cursor.execute(sql_query, sql_params)
        rows: list[sqlite3.Row] = cursor.fetchall()

        # Instantiate the editor items
        editor_items: list[EditorItem] = []
        for row in rows:
            row_values = self.row_to_dict(row)

            editor_item = EditorItem(**row_values)
            editor_item.id = row['id']
            editor_item.created_at = row['created_at']
            editor_items.append(editor_item)

        return editor_items
