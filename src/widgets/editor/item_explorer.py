from PyQt6 import QtWidgets, QtCore, QtGui

from models.data.editor_item import EditorItem
from models.qt.editor_tree_model import EditorTreeModel
from models.qt.editor_tree_item import EditorTreeItem

class ItemExplorer(QtWidgets.QTreeView):
    item_created = QtCore.pyqtSignal(EditorItem)
    item_deleted = QtCore.pyqtSignal(EditorItem)
    item_renamed = QtCore.pyqtSignal(EditorItem)
    item_clicked = QtCore.pyqtSignal(EditorItem)
    item_double_clicked = QtCore.pyqtSignal(EditorItem)

    def __init__(self, *args, **kwargs):
        super(ItemExplorer, self).__init__(*args, **kwargs)

        self.reload_data()

        self.setModel(self.tree_model)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ContiguousSelection)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.setDragDropOverwriteMode(True)
        self.setIconSize(QtCore.QSize(25, 15))
        # self.setUniformRowHeights(True)

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

    def reload_item(self, editor_item):
        print(f'ItemExplorer: reloading editor item: {editor_item.name}')
        self.tree_model.layoutChanged.emit()

    def change_selection(self, index):
        self.selectionModel().setCurrentIndex(
            index,
            QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect
        )

    def right_click(self, position):
        index = self.indexAt(position)

        selected_indexes = self.selectionModel().selectedRows()

        if (len(selected_indexes) > 1):
            self.show_multi_selection_context_menu(selected_indexes, position)
        else:
            self.show_single_selection_context_menu(index, position)

    def double_click(self, index):
        item = self.tree_model.getItem(index)
        if not item.is_dir:
            self.item_double_clicked.emit(item.editor_item)

    def click(self, index):
        item = self.tree_model.getItem(index)
        if not item.is_dir:
            self.item_clicked.emit(item.editor_item)

    def show_multi_selection_context_menu(self, indexes, position):
        delete_action = QtGui.QAction(f"Delete {len(indexes)} items")
        delete_action.triggered.connect(
            lambda: self.multi_delete_clicked(indexes))

        menu = QtWidgets.QMenu(self)
        menu.addAction(delete_action)
        menu.exec(self.viewport().mapToGlobal(position))

    def show_single_selection_context_menu(self, index, position):
        tree_item = self.tree_model.getItem(index)

        new_request_action = QtGui.QAction("New Request")
        new_request_action.triggered.connect(lambda: self.new_request_clicked(index))

        new_dir_action = QtGui.QAction("New Folder")
        new_dir_action.triggered.connect(lambda: self.new_dir_clicked(index))

        new_fuzz_action = QtGui.QAction("New Fuzz")
        new_fuzz_action.triggered.connect(lambda: self.new_fuzz_clicked(index))

        rename_action = QtGui.QAction("Rename")
        rename_action.triggered.connect(lambda: self.edit(index))

        paste_action = QtGui.QAction("Paste")
        paste_action.triggered.connect(lambda: self.paste_clicked(index))

        copy_action = QtGui.QAction("Copy")
        copy_action.triggered.connect(lambda: self.copy_clicked(index))

        delete_action = QtGui.QAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_clicked(index))

        # TODO: Refactor all these if statements:
        menu = QtWidgets.QMenu(self)
        if tree_item.is_dir:
            menu.addAction(new_request_action)
            menu.addAction(new_dir_action)
            menu.addAction(new_fuzz_action)
            if self.copied_editor_item is not None:
                menu.addAction(paste_action)
        else:
            menu.addAction(copy_action)

        if index.isValid():
            menu.addAction(delete_action)
            menu.addAction(rename_action)

        menu.exec(self.viewport().mapToGlobal(position))

    def new_editor_item_created(self, editor_item):
        self.insertChild(editor_item, QtCore.QModelIndex())
        self.item_created.emit(editor_item)

    def new_request_clicked(self, parent_index: QtCore.QModelIndex):
        child_editor_item = EditorItem()
        child_editor_item.name = 'New HTTP Request'
        child_editor_item.item_type = EditorItem.TYPE_HTTP_FLOW

        self.insertChild(child_editor_item, parent_index)
        self.item_created.emit(child_editor_item)

    def new_dir_clicked(self, parent_index: QtCore.QModelIndex):
        child_editor_item = EditorItem()
        child_editor_item.name = 'New Folder'
        child_editor_item.item_type = 'dir'

        self.insertChild(child_editor_item, parent_index)

    def new_fuzz_clicked(self, parent_index: QtCore.QModelIndex):
        child_editor_item = EditorItem()
        child_editor_item.name = 'New Fuzz Request'
        child_editor_item.item_type = EditorItem.TYPE_FUZZ

        self.insertChild(child_editor_item, parent_index)
        self.item_created.emit(child_editor_item)

    def copy_clicked(self, parent_index: QtCore.QModelIndex):
        tree_item = self.tree_model.getItem(parent_index)
        if tree_item.editor_item is None:
            return
        self.copied_editor_item = tree_item.editor_item.duplicate()

    def paste_clicked(self, parent_index: QtCore.QModelIndex):
        self.insertChild(self.copied_editor_item, parent_index)
        self.item_created.emit(self.copied_editor_item)

    def delete_clicked(self, index: QtCore.QModelIndex):
        tree_item = self.tree_model.getItem(index)

        if tree_item.is_dir:
            message = 'Are you sure you want to delete this folder and all of its children?'
        else:
            message = 'Are you sure you want to delete this request?'

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('PNTest')
        message_box.setText(message)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
        message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
        response = message_box.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            self.tree_model.removeRows(index.row(), 1, index.parent(), True)
            self.item_deleted.emit(tree_item.editor_item)

    def multi_delete_clicked(self, indexes):
        tree_items = [self.tree_model.getItem(i) for i in indexes]
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('PNTest')
        message_box.setText(f'Are you sure you want to delete these {len(indexes)} items?')
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
        message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
        response = message_box.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
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
            QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect
        )
        self.edit(child_index)
