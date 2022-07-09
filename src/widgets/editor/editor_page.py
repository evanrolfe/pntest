from PyQt6 import QtCore, QtGui, QtWidgets

from views._compiled.editor.editor_page import Ui_EditorPage
from widgets.shared.variables_popup import VariablesPopup
from lib.app_settings import AppSettings
from models.data.editor_item import EditorItem

class EditorPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(EditorPage, self).__init__(*args, **kwargs)

        self.ui = Ui_EditorPage()
        self.ui.setupUi(self)
        self.restore_layout_state()

        self.ui.itemExplorer.item_double_clicked.connect(self.ui.editorTabs.open_item)
        self.ui.itemExplorer.item_created.connect(self.ui.editorTabs.open_item)
        self.ui.itemExplorer.item_deleted.connect(self.ui.editorTabs.close_item)
        self.ui.itemExplorer.item_renamed.connect(self.ui.editorTabs.change_item)

        self.ui.editorTabs.new_request_saved.connect(self.ui.itemExplorer.reload_data)
        self.ui.editorTabs.item_changed.connect(self.ui.itemExplorer.reload_item)
        self.ui.editorTabs.setObjectName('editorTabs')

        self.variables_popup = VariablesPopup(self)
        self.ui.varsButton.clicked.connect(lambda: self.variables_popup.show())

        # Keyboard shortcuts:
        keyseq_ctrl_n = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+N'), self)
        keyseq_ctrl_n.activated.connect(self.ui.editorTabs.open_blank_item)

        keyseq_ctrl_w = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+W'), self)
        keyseq_ctrl_w.activated.connect(self.ui.editorTabs.close_current_tab)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape.value:
            self.close()

    def reload(self):
        self.ui.editorTabs.clear()
        self.ui.itemExplorer.reload_data()

    def restore_layout_state(self):
        settings = AppSettings.get_instance()
        splitter_state = settings.get("EditorPage.splitter", None)
        self.ui.editorSplitter.restoreState(splitter_state)

    def save_layout_state(self):
        splitter_state = self.ui.editorSplitter.saveState()
        settings = AppSettings.get_instance()
        settings.save("EditorPage.splitter", splitter_state)

        # self.ui.requestGroupView.save_layout_state()

    def send_flow_to_editor(self, flow):
        new_flow = flow.duplicate_for_editor()
        editor_item = EditorItem.create_for_http_flow(new_flow)

        print(f'Created EditorItem {editor_item.id} and editor request: {editor_item.item_id}')
        self.ui.itemExplorer.new_editor_item_created(editor_item)
