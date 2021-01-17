import sys

from PySide2.QtWidgets import QApplication, QWidget, QTabWidget
from PySide2.QtCore import Slot

from lib.app_settings import AppSettings
from lib.backend import Backend
from widgets.editor.request_edit_page import RequestEditPage

class Tabs(QTabWidget):
  def __init__(self, *args, **kwargs):
    super(Tabs, self).__init__(*args, **kwargs)

    self.setTabsClosable(True)
    self.setMovable(True)

    self.tabCloseRequested.connect(self.close_tab)

  @Slot()
  def open_item(self, editor_item):
    existing_tab_index = self.get_index_for_editor_item(editor_item)

    if existing_tab_index == None:
      request_edit_page = RequestEditPage(editor_item)
      request_edit_page.form_input_changed.connect(lambda modified: self.editor_item_form_changed(editor_item, modified))
      self.insertTab(self.count(), request_edit_page, editor_item.name)
      self.setCurrentIndex(self.count()-1)
    else:
      self.setCurrentIndex(existing_tab_index)

  @Slot()
  def close_tab(self, index):
    self.removeTab(index)

  @Slot()
  def close_item(self, tree_item):
    index = self.get_index_for_editor_item(tree_item.editor_item)
    if index:
      self.removeTab(index)

  @Slot()
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

    print(f'Changing {editor_item.id} {editor_item.name} in index {index}')

  @Slot()
  def editor_item_form_changed(self, editor_item, modified):
    print(f'Editor Item {editor_item.id} is modified? {modified}')

    index = self.get_index_for_editor_item(editor_item)
    tab_text = self.tabText(index)
    last_char = tab_text[-1]

    # if its modified but has no *
    if modified and last_char != '*':
      self.setTabText(index, tab_text + '*')

    # if its no longer modified has a *
    elif not modified and last_char == '*':
      self.setTabText(index, tab_text[0:-1])

  def get_index_for_editor_item(self, editor_item):
    editor_items = [self.widget(i).editor_item for i in range(0,self.count())]

    try:
      return editor_items.index(editor_item)
    except ValueError:
      return None
