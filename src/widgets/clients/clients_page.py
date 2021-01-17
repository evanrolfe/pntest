import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from views._compiled.clients.ui_clients_page import Ui_ClientsPage

from lib.backend import Backend
from models.qt.clients_table_model import ClientsTableModel
from models.data.client import Client
from widgets.new_client_modal import NewClientModal

class ClientsPage(QWidget):
  def __init__(self, *args, **kwargs):
    super(ClientsPage, self).__init__(*args, **kwargs)
    self.ui = Ui_ClientsPage()
    self.ui.setupUi(self)

    clients = Client.all()
    self.clients_table_model = ClientsTableModel(clients)

    self.ui.clientsTable.setTableModel(self.clients_table_model)
    self.ui.clientsTable.client_selected.connect(self.select_client)

    # Reload when the clients have changed:
    self.backend = Backend.get_instance()
    self.backend.register_callback('clientsChanged', self.reload_table_data)

    # Create new client modal
    self.new_client_modal = NewClientModal(self)
    self.ui.newClientButton.clicked.connect(self.new_client_click)

  def showEvent(self, event):
    self.reload_table_data()

  def reload_table_data(self):
    clients = Client.all()
    self.clients_table_model.set_clients(clients)

  @Slot()
  def select_client(self, selected, deselected):
    selected_id = selected.indexes()[0].data()
    client = Client.find(selected_id)
    self.ui.clientView.set_client(client)

  @Slot()
  def new_client_click(self):
    self.new_client_modal.show()
