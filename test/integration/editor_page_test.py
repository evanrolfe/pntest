import threading
from PyQt6 import QtCore, QtWidgets
from pytestqt.qtbot import QtBot
from repos.editor_item_repo import EditorItemRepo
from ui.widgets.editor.editor_page import EditorPage

class TestEditorPage:
    def test_deleting_an_item(self, database, cleanup_database, qtbot: QtBot):
        widget = EditorPage()
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # Open a new tab
        widget.ui.editorTabs.open_blank_item()

        # Click save button
        current_index = widget.ui.editorTabs.currentIndex()
        request_edit_page = widget.ui.editorTabs.get_page_for_tab(current_index)

        # Enter request URL and Click save button
        request_edit_page.ui.urlInput.setText("http://localhost:3000")
        button = request_edit_page.ui.saveButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        # Simulate a right click to delete the request
        index = widget.ui.itemExplorer.tree_model.index(0,0, QtCore.QModelIndex())

        # Hit enter on confirmation prompt
        # Very hacky way of hitting enter in a thread separate from the GUI, see:
        # https://stackoverflow.com/questions/61213729/simulate-the-click-on-a-button-in-the-pyqt5-qmessagebox-widget-during-unittest
        self.qtbot = qtbot
        threading.Timer(0.2, self.accept_confirmation_prompt).start()
        print("Delete clicked...")
        widget.ui.itemExplorer.delete_clicked(index)

        editor_items = EditorItemRepo().find_all_with_children()
        assert len(editor_items) == 0

    def accept_confirmation_prompt(self):
        print("Hitting enter")
        promptWindow = QtWidgets.QApplication.activeWindow()
        self.qtbot.keyPress(promptWindow, QtCore.Qt.Key.Key_Enter)
