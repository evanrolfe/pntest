from __future__ import annotations
from typing import Optional
from PyQt6 import QtWidgets, QtGui
from models.editor_item import EditorItem
from services.editor_item_service import EditorItemService

class EditorTreeItem:
    label: str
    is_dir: bool
    editor_item: Optional[EditorItem]
    childItems: list[EditorTreeItem]
    parent: Optional[EditorTreeItem]

    def __init__(self, label: str, editor_item: Optional[EditorItem] = None, is_dir: bool = False):
        self.label = label
        self.is_dir = is_dir
        self.editor_item = editor_item
        self.childItems = []
        self.parent = None

    @classmethod
    def from_editor_item(cls, editor_item: EditorItem) -> EditorTreeItem:
        is_dir = (editor_item.item_type == 'dir')
        return cls(editor_item.name, editor_item, is_dir)

    def data(self) -> str:
        return self.label

    def child(self, row: int) -> Optional[EditorTreeItem]:
        try:
            return self.childItems[row]
        except IndexError:
            return None

    def childCount(self) -> int:
        return len(self.childItems)

    def childNumber(self) -> int:
        if self.parent is not None:
            return self.parent.childItems.index(self)

        return 0

    def childIndicatorPolicy(self):
        return QtWidgets.QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator

    def columnCount(self) -> int:
        return 1

    def sortChildren(self) -> None:
        self.childItems = sorted(self.childItems, key=lambda x: (not x.is_dir, x.label))

    def insertChild(self, child_item: EditorTreeItem) -> None:
        self.childItems.append(child_item)
        child_item.parent = self

        if child_item.editor_item is None:
            return

        if self.editor_item is not None:
            child_item.editor_item.parent_id = self.editor_item.id
        else:
            child_item.editor_item.parent_id = None

        EditorItemService().save(child_item.editor_item)

        self.sortChildren()

    def insertChildren(self, child_items: list[EditorTreeItem]) -> None:
        for item in child_items:
            self.insertChild(item)

    def removeChildren(self, position: int, count: int, delete: bool = False) -> bool:
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            removed_item = self.childItems.pop(position)
            if delete and removed_item.editor_item is not None:
                EditorItemService().delete(removed_item.editor_item)

        return True

    def setLabel(self, label: str) -> bool:
        if self.editor_item is None:
            return True
        # TODO: Remove *'s becuase they will mess with the modified indicator
        self.label = label
        self.editor_item.name = label
        return True

    def icon(self) -> Optional[QtGui.QIcon]:
        if self.is_dir or self.editor_item is None:
            return None

        if self.editor_item.item_type == EditorItem.TYPE_FUZZ:
            return QtGui.QIcon(f"assets:icons/dark/methods/fuzz.png")

        if self.editor_item.item_type == EditorItem.TYPE_HTTP_FLOW:
            icon_methods = ['get', 'put', 'patch', 'delete', 'post', 'options', 'head']

            item = self.editor_item.item
            if item is None:
                raise Exception("No item found for editor item")

            method = item.request.method.lower()
            if method not in icon_methods:
                method = 'other'

            return QtGui.QIcon(f"assets:icons/dark/methods/{method}.png")

        raise Exception("No item found for editor item")

