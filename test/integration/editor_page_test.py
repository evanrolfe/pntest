# import time
from support.fixtures import load_fixtures
from widgets.editor.editor_page import EditorPage

class TestEditorPage:
    def test_editor_page(self, database, qtbot):
        load_fixtures()

        widget = EditorPage()
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)

        # widget.show()
        # qtbot.waitForWindowShown(widget)
        # time.sleep(3)

        # TODO:
        assert 1 == 1
