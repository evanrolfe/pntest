import sys
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon

from views._compiled.network.ui_network_display_filters import Ui_NetworkDisplayFilters

from lib.backend import Backend

class NetworkDisplayFilters(QDialog):
  def __init__(self, parent = None):
    super(NetworkDisplayFilters, self).__init__(parent)

    self.ui = Ui_NetworkDisplayFilters()
    self.ui.setupUi(self)
    self.setModal(True)

  #def showEvent(self, event):
    # print("NewClientModal - showEvent")
    # self.backend.get_available_clients()
