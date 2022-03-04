from PySide2 import QtCore, QtWidgets

from models.data.editor_item import EditorItem
from models.data.editor_item_unsaved import EditorItemUnsaved
from widgets.editor.request_edit_page import RequestEditPage
from widgets.editor.fuzz_edit_page import FuzzEditPage

class Tabs(QtWidgets.QTabWidget):
    item_changed = QtCore.Signal(EditorItem)
    new_request_saved = QtCore.Signal(EditorItem)

    def __init__(self, *args, **kwargs):
        super(Tabs, self).__init__(*args, **kwargs)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setIconSize(QtCore.QSize(20, 12))
        self.open_blank_item()

        self.tabCloseRequested.connect(self.close_tab)

    def open_blank_item(self):
        editor_item = EditorItemUnsaved()
        request_edit_page = RequestEditPage(editor_item)
        request_edit_page.request_saved.connect(lambda: self.reload_icon)
        request_edit_page.request_saved.connect(lambda: self.new_request_saved.emit(request_edit_page.editor_item))
        self.insertTab(self.count(), request_edit_page, editor_item.icon(), editor_item.name)
        self.setCurrentIndex(self.count() - 1)

    @QtCore.Slot()  # type:ignore
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
            self.insertTab(self.count(), edit_page, editor_item.icon(), editor_item.name)
            self.setCurrentIndex(self.count() - 1)
        else:
            self.setCurrentIndex(existing_tab_index)

    @QtCore.Slot()  # type:ignore
    def close_tab(self, index):
        self.removeTab(index)

    @QtCore.Slot()  # type:ignore
    def close_item(self, tree_item):
        index = self.get_index_for_editor_item(tree_item.editor_item)
        if index:
            self.removeTab(index)

    @QtCore.Slot()  # type:ignore
    def change_item(self, editor_item):
        index = self.get_index_for_editor_item(editor_item)
        new_tab_text = editor_item.name

        # Preserve the *
        # TODO: Find a better way of doing this, probably have to a hash of tab indexes and modified booleans
        tab_text = self.tabText(index)
        last_char = tab_text[-1]
        if last_char == '*':
            new_tab_text += '*'

        self.setTabText(index, new_tab_text)

    @QtCore.Slot()  # type:ignore
    def reload_icon(self, editor_item):
        index = self.get_index_for_editor_item(editor_item)
        self.setTabIcon(index, editor_item.icon())
        self.item_changed.emit(editor_item)

    @QtCore.Slot()  # type:ignore
    def editor_item_form_changed(self, editor_item, modified):
        index = self.get_index_for_editor_item(editor_item)
        tab_text = self.tabText(index)
        last_char = tab_text[-1]

        # if its modified but has no *
        if modified and last_char != '*':
            self.setTabText(index, tab_text + '*')

        # if its no longer modified has a *
        elif not modified and last_char == '*':
            self.setTabText(index, tab_text[0:-1])

    @QtCore.Slot()  # type:ignore
    def close_current_tab(self):
        self.close_tab(self.currentIndex())

    def get_index_for_editor_item(self, editor_item):
        editor_item_ids = [self.widget(i).editor_item.id for i in range(0, self.count())]

        try:
            return editor_item_ids.index(editor_item.id)
        except ValueError:
            return None
