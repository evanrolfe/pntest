from typing import cast, Optional, Any
from PySide2 import QtCore
import json

from models.data.editor_item import EditorItem
from models.qt.editor_tree_item import EditorTreeItem

class EditorTreeModel(QtCore.QAbstractItemModel):
    item_renamed = QtCore.Signal(EditorItem)
    change_selection = QtCore.Signal(QtCore.QModelIndex)
    layoutChanged: QtCore.SignalInstance

    def __init__(self, header, editor_items, parent=None):
        super(EditorTreeModel, self).__init__(parent)

        self.rootItem = EditorTreeItem(header, None, True)
        self.setup_model_data(editor_items, self.rootItem)

    def supportedDropActions(self) -> QtCore.Qt.DropActions:
        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction  # type: ignore

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return self.rootItem.columnCount()

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt) -> Any:
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole and role != QtCore.Qt.DecorationRole:
            return None

        item = self.getItem(index)

        if role == QtCore.Qt.DecorationRole:
            return item.icon()
        else:
            return item.data()

    def setData(self, index: QtCore.QModelIndex, value: str, role: QtCore.Qt = QtCore.Qt.EditRole) -> bool:
        if role == QtCore.Qt.EditRole:
            item = self.getItem(index)
            item.setLabel(value)

            if item.parent is not None:
                item.parent.sortChildren()
            new_selected_index = self.createIndex(item.childNumber(), 0, item)

            self.layoutChanged.emit()
            cast(QtCore.SignalInstance, self.change_selection).emit(new_selected_index)
            if not item.is_dir:
                cast(QtCore.SignalInstance, self.item_renamed).emit(item.editor_item)

            return True
        elif role == QtCore.Qt.DisplayRole:
            self.layoutChanged.emit()
            return True

        return False

    def mimeTypes(self) -> list[str]:
        return ['text/index-json-array']

    def mimeData(self, indexes: list[QtCore.QModelIndex]) -> QtCore.QMimeData:
        index_data = [{'internalId': i.internalId(
        ), 'row': i.row(), 'column': i.column()} for i in indexes]

        encoded_json = json.dumps(index_data).encode()
        mimeData = QtCore.QMimeData()
        mimeData.setData('text/index-json-array', QtCore.QByteArray(encoded_json))  # type: ignore
        return mimeData

    def canDropMimeData(
        self,
        data: QtCore.QMimeData,
        action: QtCore.Qt.DropAction,
        row: int,
        column: int,
        parent_index: QtCore.QModelIndex
    ) -> bool:
        if (action != QtCore.Qt.DropAction.MoveAction):
            return False

        item = self.getItem(parent_index)

        indexes, tree_items = self.decode_mime_data(data)

        if item.is_dir is False:
            return False

        item_parents = [i.parent for i in tree_items]
        items_are_not_dirs = [not i.is_dir for i in tree_items]
        items_share_same_parent = len(set(item_parents)) == 1

        return (all(items_are_not_dirs) and items_share_same_parent)

    def dropMimeData(
        self,
        data: QtCore.QMimeData,
        action: QtCore.Qt.DropAction,
        row: int,
        column: int,
        parent_index: QtCore.QModelIndex
    ) -> bool:
        if (action != QtCore.Qt.DropAction.MoveAction):
            return False

        indexes, tree_items = self.decode_mime_data(data)
        rows = sorted([i.row() for i in indexes])
        diff = rows[-1] - rows[0]

        self.removeRows(rows[0], diff + 1, indexes[0].parent())
        self.insertChildren(tree_items, parent_index)

        return True

    def decode_mime_data(self, mime_data: QtCore.QMimeData) -> tuple[list[QtCore.QModelIndex], list[EditorTreeItem]]:
        encoded_data = mime_data.data('text/index-json-array')
        index_data = json.loads(str(encoded_data, 'utf-8'))  # type: ignore

        indexes = [self.createIndex(
            i['row'], i['column'], i['internalId']) for i in index_data]
        tree_items = [self.getItem(i) for i in indexes]

        return (indexes, tree_items)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if not index.isValid():
            return QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsDropEnabled  # type: ignore

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled  # type: ignore

    def getItem(self, index: QtCore.QModelIndex) -> EditorTreeItem:
        if index.isValid():
            item = cast(EditorTreeItem, index.internalPointer())
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole) -> Optional[str]:
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data()

        return None

    def index(self, row: int, column: int, parent_index: QtCore.QModelIndex = ...):
        if parent_index.isValid() and parent_index.column() != 0:
            return QtCore.QModelIndex

        parentItem = self.getItem(parent_index)
        childItem = parentItem.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex

    # TODO: Make this call self.insertChildren()
    def insertChild(self, child, parent: QtCore.QModelIndex = ...):
        parentItem = self.getItem(parent)
        position = parentItem.childCount()

        self.beginInsertRows(parent, position, position)
        success = parentItem.insertChild(child)
        self.endInsertRows()

        return success

    def insertChildren(self, child_items, parent_index: QtCore.QModelIndex = ...) -> None:
        parentItem = self.getItem(parent_index)
        position = parentItem.childCount()

        self.beginInsertRows(parent_index, position,
                             position + len(child_items))
        parentItem.insertChildren(child_items)
        self.endInsertRows()

    def parent(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.QModelIndex()  # type: ignore

        childItem = self.getItem(index)
        parentItem = childItem.parent

        if parentItem == self.rootItem or childItem == self.rootItem:
            return QtCore.QModelIndex()  # type: ignore

        if parentItem is not None:
            return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeRows(self, row: int, count: int, parent_index: QtCore.QModelIndex = ..., delete=False) -> bool:
        parentItem = self.getItem(parent_index)

        self.beginRemoveRows(parent_index, row, row + count)
        success = parentItem.removeChildren(row, count, delete)
        self.endRemoveRows()

        return success

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def hasChildren(self, index: QtCore.QModelIndex) -> bool:
        item = self.getItem(index)

        if item is None:
            return False

        if item.is_dir:
            return True

        return (item.childCount() > 0)

    def setup_model_data(self, editor_items: list[EditorItem], root_tree_item: EditorTreeItem) -> None:
        root_level_editor_items = [
            x for x in editor_items if x.parent_id is None]

        for editor_item in root_level_editor_items:
            self.add_editor_item_to_tree(root_tree_item, editor_item)

    def add_editor_item_to_tree(self, parent_tree_item: EditorTreeItem, editor_item: EditorItem) -> None:
        tree_item = EditorTreeItem.from_editor_item(editor_item)
        parent_tree_item.insertChild(tree_item)

        for child_editor_item in editor_item.children():
            self.add_editor_item_to_tree(tree_item, child_editor_item)
