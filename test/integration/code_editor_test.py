from PyQt6 import QtCore
from pytestqt.qtbot import QtBot
from support.fixtures import load_fixtures
from ui.widgets.shared.code_editor import CodeEditor

lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean ullamcorper non nunc at sollicitudin.
Ut sit amet aliquam lectus. Mauris consequat varius leo vel tempus. Suspendisse vitae nisl nibh.
Sed congue est accumsan, tempor ante et, dictum felis. Maecenas ultricies volutpat ornare.
Vestibulum nunc urna, bibendum a eros nec, volutpat iaculis tellus.
"""

class TestCodeEditor:
    # NOTE: this test is commented because the time.sleep means this test fails in circleCI
    # def test_finding(self, database, cleanup_database, qtbot: QtBot):
    #     load_fixtures()

    #     widget = CodeEditor()
    #     widget.set_value(lorem_ipsum)
    #     qtbot.addWidget(widget)
    #     qtbot.waitExposed(widget)
    #     widget.show()
    #     qtbot.waitExposed(widget)

    #     # Press CTRL+F
    #     qtbot.keyClick(widget, "F", QtCore.Qt.KeyboardModifier.ControlModifier)

    #     # Type in "sit" and hit enter
    #     qtbot.keyClicks(widget.ui.findText, "sit")
    #     qtbot.keyClick(widget, QtCore.Qt.Key.Key_Return)
    #     # TODO: Find a better way than  using time.sleep, without it this test gives intermitten failures
    #     time.sleep(1)

    #     # Check the first instance of sit has been selected
    #     line0, col0, line1, col1 = widget.ui.code.getSelection()
    #     assert line0 == 0
    #     assert col0 == 18
    #     assert line1 == 0
    #     assert col1 == 21

    #     # Hit enter again
    #     qtbot.keyClick(widget, QtCore.Qt.Key.Key_Return)

    #     # Check the second instance of sit has been selected
    #     line0, col0, line1, col1 = widget.ui.code.getSelection()
    #     assert line0 == 1
    #     assert col0 == 3
    #     assert line1 == 1
    #     assert col1 == 6

    #     # Hit enter again
    #     qtbot.keyClick(widget, QtCore.Qt.Key.Key_Return)

    #     # Check the first instance of sit has been selected (again)
    #     line0, col0, line1, col1 = widget.ui.code.getSelection()
    #     # print(f'line0: {line0} col0: {col0}, line1: {line1} col1: {col1}')
    #     assert line0 == 0
    #     assert col0 == 18
    #     assert line1 == 0
    #     assert col1 == 21

    def test_replacing(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = CodeEditor()
        lorem_ipsum_short = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean ullamcorper non nunc at sollicitudin. Ut sit amet aliquam lectus."
        widget.set_value(lorem_ipsum_short)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)
        widget.show()
        qtbot.waitExposed(widget)

        # Press CTRL+F
        qtbot.keyClick(widget, "F", QtCore.Qt.KeyboardModifier.ControlModifier)

        # Type in "sit" for find and "XXX" for replace
        qtbot.keyClicks(widget.ui.findText, "sit")
        qtbot.keyClicks(widget.ui.replaceText, "XXX")

        # Hit replace button
        button = widget.ui.replaceButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        assert widget.get_value() == "Lorem ipsum dolor XXX amet, consectetur adipiscing elit. Aenean ullamcorper non nunc at sollicitudin. Ut sit amet aliquam lectus."

        # Hit replace button again
        button = widget.ui.replaceButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        assert widget.get_value() == "Lorem ipsum dolor XXX amet, consectetur adipiscing elit. Aenean ullamcorper non nunc at sollicitudin. Ut XXX amet aliquam lectus."

    def test_replacing_all(self, database, cleanup_database, qtbot: QtBot):
        load_fixtures()

        widget = CodeEditor()
        lorem_ipsum_short = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean ullamcorper non nunc at sollicitudin. Ut sit amet aliquam lectus."
        widget.set_value(lorem_ipsum_short)
        qtbot.addWidget(widget)
        qtbot.waitExposed(widget)
        widget.show()
        qtbot.waitExposed(widget)

        # Press CTRL+F
        qtbot.keyClick(widget, "F", QtCore.Qt.KeyboardModifier.ControlModifier)

        # Type in "sit" for find and "XXX" for replace
        qtbot.keyClicks(widget.ui.findText, "sit")
        qtbot.keyClicks(widget.ui.replaceText, "XXX")

        # Hit replace all button
        button = widget.ui.replaceAllButton
        qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton, pos=button.rect().center())

        assert widget.get_value() == "Lorem ipsum dolor XXX amet, consectetur adipiscing elit. Aenean ullamcorper non nunc at sollicitudin. Ut XXX amet aliquam lectus."
