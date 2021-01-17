import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from views._compiled.clients.ui_client_view import Ui_ClientView

class ClientView(QWidget):
  def __init__(self, *args, **kwargs):
    super(ClientView, self).__init__(*args, **kwargs)
    self.ui = Ui_ClientView()
    self.ui.setupUi(self)

  def set_client(self, client):
    text = f"{client.title}\nType: {client.type}\nProxy port: {client.proxy_port}" \
      f"\nBrowser port: {client.browser_port}\nStatus: {client.open_text()}"

    self.ui.clientBodyText.setPlainText(text)
