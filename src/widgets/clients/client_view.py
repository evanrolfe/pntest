from PyQt6 import QtWidgets

from views._compiled.clients.client_view import Ui_ClientView

class ClientView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ClientView, self).__init__(*args, **kwargs)
        self.ui = Ui_ClientView()
        self.ui.setupUi(self)

    def clear(self):
        self.ui.clientBodyText.setPlainText('')

    def set_client(self, client):
        text = f"{client.title}\nType: {client.type}\nProxy port: {client.proxy_port}\nStatus: {client.open_text()}"

        self.ui.clientBodyText.setPlainText(text)
