import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView, QMenu, QAction, QItemDelegate, QMessageBox
from PySide2.QtCore import QFile, Slot, Qt, QItemSelectionModel

from views._compiled.editor.ui_editor_page import Ui_EditorPage

from lib.app_settings import AppSettings
from lib.backend import Backend
from models.data.editor_item import EditorItem
from models.qt.editor_tree_model import EditorTreeModel
from models.qt.editor_tree_item import EditorTreeItem

class EditorPage(QWidget):
  def __init__(self, *args, **kwargs):
    super(EditorPage, self).__init__(*args, **kwargs)

    self.ui = Ui_EditorPage()
    self.ui.setupUi(self)
    self.restore_layout_state()

    self.ui.itemExplorer.item_double_clicked.connect(self.ui.tabs.open_item)
    self.ui.itemExplorer.item_created.connect(self.ui.tabs.open_item)
    self.ui.itemExplorer.item_deleted.connect(self.ui.tabs.close_item)
    self.ui.itemExplorer.item_renamed.connect(self.ui.tabs.change_item)

  def restore_layout_state(self):
    settings = AppSettings.get_instance()
    splitter_state = settings.get("EditorPage.splitter", None)
    self.ui.editorSplitter.restoreState(splitter_state)

  def save_layout_state(self):
    splitter_state = self.ui.editorSplitter.saveState()
    settings = AppSettings.get_instance()
    settings.save("EditorPage.splitter", splitter_state)

    #self.ui.requestGroupView.save_layout_state()

  @Slot()
  def send_request_to_editor(self, request):
    editor_item = EditorItem.create_from_network_request(request)
    print(f'Created EditorItem {editor_item.id} and editor request: {editor_item.item_id}')
    self.ui.itemExplorer.new_editor_item_created(editor_item)
