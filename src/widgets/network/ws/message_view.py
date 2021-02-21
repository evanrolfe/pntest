from PySide2 import QtWidgets

from views._compiled.network.ws.ui_message_view import Ui_MessageView

class MessageView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MessageView, self).__init__(*args, **kwargs)
        self.ui = Ui_MessageView()
        self.ui.setupUi(self)

        # Disable modified tabs to start with:
        self.ui.messageTabs.setTabEnabled(1, False)

    def clear_request(self):
        self.ui.messageText.setPlainText('')

    def set_request(self, request):
        self.ui.messageText.setPlainText(f'Request: {request.id}')
