from PySide2 import QtWidgets

from views._compiled.network.ws.ui_message_view import Ui_MessageView

class MessageView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MessageView, self).__init__(*args, **kwargs)
        self.ui = Ui_MessageView()
        self.ui.setupUi(self)

        # Disable modified tabs to start with:
        self.ui.messageTabs.setTabEnabled(1, False)

    def clear_message(self):
        self.ui.messageText.setPlainText('')
        self.ui.messageTabs.setTabEnabled(1, False)

    def set_message(self, message):
        self.ui.messageText.setPlainText(message.body)
        if message.body_modified is not None:
            self.ui.messageModifiedText.setPlainText(message.body_modified)
            self.ui.messageTabs.setTabEnabled(1, True)
        else:
            self.ui.messageModifiedText.setPlainText('')
            self.ui.messageTabs.setTabEnabled(1, False)
