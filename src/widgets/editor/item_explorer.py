from PySide2 import QtWidgets, QtCore

from models.data.editor_item import EditorItem
from models.qt.editor_tree_model import EditorTreeModel
from models.qt.editor_tree_item import EditorTreeItem

class ItemExplorer(QtWidgets.QTreeView):
    item_created = QtCore.Signal(EditorItem)
    item_deleted = QtCore.Signal(EditorItem)
    item_renamed = QtCore.Signal(EditorItem)
    item_clicked = QtCore.Signal(EditorItem)
    item_double_clicked = QtCore.Signal(EditorItem)

    def __init__(self, *args, **kwargs):
        super(ItemExplorer, self).__init__(*args, **kwargs)

        self.reload_data()

        self.setModel(self.tree_model)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setDragDropOverwriteMode(True)
        self.setIconSize(QtCore.QSize(25, 15))

        self.customContextMenuRequested.connect(self.right_click)
        self.doubleClicked.connect(self.double_click)
        self.clicked.connect(self.click)
        self.header().setObjectName('itemExplorerHeader')
        self.copied_editor_item = None

    def reload_data(self):
        editor_items = EditorItem.order_by('item_type', 'asc').get()
        self.tree_model = EditorTreeModel('Requests', editor_items)
        self.tree_model.change_selection.connect(self.change_selection)
        self.tree_model.item_renamed.connect(self.item_renamed)
        self.setModel(self.tree_model)
        print(f'ItemExplorer: reloading with {len(editor_items)} items')

    @QtCore.Slot()
    def reload_item(self, editor_item):
        print(f'ItemExplorer: reloading editor item: {editor_item.name}')
        self.tree_model.layoutChanged.emit()

    @QtCore.Slot()
    def change_selection(self, index):
        self.selectionModel().setCurrentIndex(
            index,
            QtCore.QItemSelectionModel.ClearAndSelect
        )

    @QtCore.Slot()
    def right_click(self, position):
        index = self.indexAt(position)

        selected_indexes = self.selectionModel().selectedRows()

        if (len(selected_indexes) > 1):
            self.show_multi_selection_context_menu(selected_indexes, position)
        else:
            self.show_single_selection_context_menu(index, position)

    @QtCore.Slot()
    def double_click(self, index):
        item = self.tree_model.getItem(index)
        if not item.is_dir:
            self.item_double_clicked.emit(item.editor_item)

    @QtCore.Slot()
    def click(self, index):
        item = self.tree_model.getItem(index)
        if not item.is_dir:
            self.item_clicked.emit(item.editor_item)

    def show_multi_selection_context_menu(self, indexes, position):
        delete_action = QtWidgets.QAction(f"Delete {len(indexes)} items")
        delete_action.triggered.connect(
            lambda: self.multi_delete_clicked(indexes))

        menu = QtWidgets.QMenu(self)
        menu.addAction(delete_action)
        menu.exec_(self.viewport().mapToGlobal(position))

    def show_single_selection_context_menu(self, index, position):
        tree_item = self.tree_model.getItem(index)

        new_request_action = QtWidgets.QAction("New Request")
        new_request_action.triggered.connect(lambda: self.new_request_clicked(index))

        new_dir_action = QtWidgets.QAction("New Folder")
        new_dir_action.triggered.connect(lambda: self.new_dir_clicked(index))

        rename_action = QtWidgets.QAction("Rename")
        rename_action.triggered.connect(lambda: self.edit(index))

        paste_action = QtWidgets.QAction("Paste")
        paste_action.triggered.connect(lambda: self.paste_clicked(index))

        copy_action = QtWidgets.QAction("Copy")
        copy_action.triggered.connect(lambda: self.copy_clicked(index))

        delete_action = QtWidgets.QAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_clicked(index))

        # TODO: Refactor all these if statements:
        menu = QtWidgets.QMenu(self)
        if tree_item.is_dir:
            menu.addAction(new_request_action)
            menu.addAction(new_dir_action)
            if self.copied_editor_item is not None:
                menu.addAction(paste_action)
        else:
            menu.addAction(copy_action)

        if index.isValid():
            menu.addAction(delete_action)
            menu.addAction(rename_action)

        menu.exec_(self.viewport().mapToGlobal(position))

    def new_editor_item_created(self, editor_item):
        self.insertChild(editor_item, QtCore.QModelIndex())
        self.item_created.emit(editor_item)

    @QtCore.Slot()
    def new_request_clicked(self, parent_index):
        child_editor_item = EditorItem()
        child_editor_item.name = 'new request'
        child_editor_item.item_type = 'request'

        self.insertChild(child_editor_item, parent_index)
        self.item_created.emit(child_editor_item)

    @QtCore.Slot()
    def new_dir_clicked(self, parent_index):
        child_editor_item = EditorItem()
        child_editor_item.name = 'new folder'
        child_editor_item.item_type = 'dir'

        self.insertChild(child_editor_item, parent_index)

    @QtCore.Slot()
    def copy_clicked(self, parent_index):
        tree_item = self.tree_model.getItem(parent_index)
        self.copied_editor_item = tree_item.editor_item.duplicate()

    @QtCore.Slot()
    def paste_clicked(self, parent_index):
        self.insertChild(self.copied_editor_item, parent_index)
        self.item_created.emit(self.copied_editor_item)

    @QtCore.Slot()
    def delete_clicked(self, index):
        tree_item = self.tree_model.getItem(index)

        if tree_item.is_dir:
            message = 'Are you sure you want to delete this folder and all of its children?'
        else:
            message = 'Are you sure you want to delete this request?'

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('PNTest')
        message_box.setText(message)
        message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        message_box.setDefaultButton(QtWidgets.QMessageBox.Yes)
        response = message_box.exec_()

        if response == QtWidgets.QMessageBox.Yes:
            self.tree_model.removeRows(index.row(), 1, index.parent(), True)
            self.item_deleted.emit(tree_item)

    def multi_delete_clicked(self, indexes):
        tree_items = [self.tree_model.getItem(i) for i in indexes]
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('PNTest')
        message_box.setText(f'Are you sure you want to delete these {len(indexes)} items?')
        message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        message_box.setDefaultButton(QtWidgets.QMessageBox.Yes)
        response = message_box.exec_()

        if response == QtWidgets.QMessageBox.Yes:
            self.selectionModel().clearSelection()

            rows = sorted([i.row() for i in indexes])
            diff = rows[-1] - rows[0]

            self.tree_model.removeRows(
                rows[0], diff + 1, indexes[0].parent(), True)
            for item in tree_items:
                self.item_deleted.emit(item)

    # TODO: Most of this method's logic should be in EditorTreeModel, not here.
    def insertChild(self, child_editor_item, parent_index):
        parent_tree_item = self.tree_model.getItem(parent_index)

        if parent_tree_item.editor_item is not None:
            child_editor_item.parent_id = parent_tree_item.editor_item.id

        child_editor_item.save()

        child_tree_item = EditorTreeItem.from_editor_item(child_editor_item)
        self.tree_model.insertChild(child_tree_item, parent_index)

        child_index = self.tree_model.index(child_tree_item.childNumber(), 0, parent_index)
        self.selectionModel().setCurrentIndex(
            child_index,
            QtCore.QItemSelectionModel.ClearAndSelect
        )
        self.edit(child_index)
