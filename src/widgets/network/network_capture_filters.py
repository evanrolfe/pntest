import sys
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon

from views._compiled.network.ui_network_capture_filters import Ui_NetworkCaptureFilters
from models.data.capture_filter import CaptureFilter

from lib.backend import Backend

class NetworkCaptureFilters(QDialog):
  def __init__(self, parent = None):
    super(NetworkCaptureFilters, self).__init__(parent)

    self.ui = Ui_NetworkCaptureFilters()
    self.ui.setupUi(self)
    self.setModal(True)

    self.ui.cancelButton.clicked.connect(self.close)
    self.ui.saveButton.clicked.connect(self.save)
    self.ui.hostSettingDropdown.currentIndexChanged.connect(self.host_setting_changed)
    self.ui.pathSettingDropdown.currentIndexChanged.connect(self.path_setting_changed)

    self.load_capture_filters()

  def showEvent(self, event):
    self.load_capture_filters()

  def load_capture_filters(self):
    print("Loading capture filters")
    self.capture_filters = CaptureFilter.find(1)

    host_index = self.setting_to_index(self.capture_filters.host_setting)
    self.ui.hostSettingDropdown.setCurrentIndex(host_index)

    path_index = self.setting_to_index(self.capture_filters.path_setting)
    self.ui.pathSettingDropdown.setCurrentIndex(path_index)

    self.ui.hostsText.setPlainText("\n".join(self.capture_filters.host_list))
    self.ui.pathsText.setPlainText("\n".join(self.capture_filters.path_list))

  @Slot()
  def save(self):
    #self.backend.send_command(self.launch_command)
    host_setting_index = self.ui.hostSettingDropdown.currentIndex()
    host_setting =  self.index_to_setting(host_setting_index)
    host_list = self.ui.hostsText.toPlainText().split("\n")

    path_setting_index = self.ui.pathSettingDropdown.currentIndex()
    path_setting =  self.index_to_setting(path_setting_index)
    path_list = self.ui.pathsText.toPlainText().split("\n")

    self.capture_filters.set_filters({
      'host_list': list(filter(None, host_list)),
      'host_setting': host_setting,
      'path_list': list(filter(None, path_list)),
      'path_setting': path_setting
    })
    self.capture_filters.save()
    self.close()

  @Slot()
  def host_setting_changed(self, index):
    self.ui.hostsText.setDisabled((index == 0))

  @Slot()
  def path_setting_changed(self, index):
    self.ui.pathsText.setDisabled((index == 0))

  def setting_to_index(self, setting):
    if setting == '':
      return 0
    elif setting == 'include':
      return 1
    elif setting == 'exclude':
      return 2

  def index_to_setting(self, index):
    if index == 0:
      return ''
    elif index == 1:
      return 'include'
    elif index == 2:
      return 'exclude'
