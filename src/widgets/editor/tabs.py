from typing import Optional, cast
from PyQt6 import QtCore, QtWidgets, QtGui

from models.editor_item import EditorItem
from models.qt.editor_tree_item import EditorTreeItem
from widgets.editor.request_edit_page import RequestEditPage
from widgets.editor.fuzz_edit_page import FuzzEditPage

class Tabs(QtWidgets.QTabWidget):
    item_changed = QtCore.pyqtSignal(EditorItem)
    new_request_saved = QtCore.pyqtSignal(EditorItem)

    def __init__(self, *args, **kwargs):
        super(Tabs, self).__init__(*args, **kwargs)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setIconSize(QtCore.QSize(20, 12))

        self.tabCloseRequested.connect(self.close_tab)

    def open_blank_item(self):
        editor_item = EditorItem(name='Untitled', item_type=EditorItem.TYPE_HTTP_FLOW)
        editor_item.build_blank_http_flow()

        request_edit_page = RequestEditPage(editor_item)
        request_edit_page.request_saved.connect(self.reload_icon)
        request_edit_page.request_saved.connect(self.new_request_saved)

        icon = self.__get_icon(editor_item)
        self.insertTab(self.count(), request_edit_page, icon, editor_item.name)
        self.setCurrentIndex(self.count() - 1)

    def open_item(self, editor_item: EditorItem):
        existing_tab_index = self.get_index_for_editor_item(editor_item)

        if existing_tab_index is None:
            if editor_item.item_type == EditorItem.TYPE_FUZZ:
                edit_page = FuzzEditPage(editor_item)
            elif editor_item.item_type == EditorItem.TYPE_HTTP_FLOW:
                edit_page = RequestEditPage(editor_item)
            else:
                return

            edit_page.form_input_changed.connect(
                lambda modified: self.editor_item_form_changed(editor_item, modified)
            )
            edit_page.request_saved.connect(lambda: self.reload_icon(editor_item))

            icon = self.__get_icon(editor_item)
            self.insertTab(self.count(), edit_page, icon, editor_item.name)
            self.setCurrentIndex(self.count() - 1)
        else:
            self.setCurrentIndex(existing_tab_index)

    def close_tab(self, index):
        self.removeTab(index)

    def close_item(self, editor_item: EditorItem):
        index = self.get_index_for_editor_item(editor_item)

        if index is not None:
            self.removeTab(index)

    def change_item(self, editor_item):
        index = self.get_index_for_editor_item(editor_item)
        if index is None:
            return
        new_tab_text = editor_item.name

        # Preserve the *
        # TODO: Find a better way of doing this, probably have to a hash of tab indexes and modified booleans
        tab_text = self.tabText(index)
        last_char = tab_text[-1]
        if last_char == '*':
            new_tab_text += '*'

        self.setTabText(index, new_tab_text)

    def reload_icon(self, editor_item: EditorItem):
        index = self.get_index_for_editor_item(editor_item)
        if index is None:
            return

        icon = self.__get_icon(editor_item)
        self.setTabIcon(index, icon)
        self.item_changed.emit(editor_item)

    def editor_item_form_changed(self, editor_item, modified):
        index = self.get_index_for_editor_item(editor_item)
        if index is None:
            return
        tab_text = self.tabText(index)
        last_char = tab_text[-1]

        # if its modified but has no *
        if modified and last_char != '*':
            self.setTabText(index, tab_text + '*')

        # if its no longer modified has a *
        elif not modified and last_char == '*':
            self.setTabText(index, tab_text[0:-1])

    def close_current_tab(self):
        self.close_tab(self.currentIndex())

    def get_page_for_tab(self, index: int) -> RequestEditPage:
        return cast(RequestEditPage, self.widget(index))

    def get_index_for_editor_item(self, editor_item: EditorItem) -> Optional[int]:
        editor_item_ids = [self.get_page_for_tab(i).editor_item.id for i in range(0, self.count())]
        try:
            return editor_item_ids.index(editor_item.id)
        except ValueError:
            return None

    def __get_icon(self, editor_item: EditorItem) -> QtGui.QIcon:
        editor_tree_item = EditorTreeItem("", editor_item)
        icon = editor_tree_item.icon()
        if icon is None:
            icon = QtGui.QIcon(f"assets:icons/dark/methods/get.png")

        return icon
