from PyQt6 import QtCore, QtWidgets
from repos.project_settings_repo import ProjectSettingsRepo

from ui.views._compiled.network.http.display_filters import Ui_DisplayFilters

class DisplayFilters(QtWidgets.QDialog):
    display_filters_saved = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(DisplayFilters, self).__init__(parent)

        self.ui = Ui_DisplayFilters()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.hostSettingDropdown.currentIndexChanged.connect(self.host_setting_changed)

        self.load_display_filters()

    def showEvent(self, event):
        self.load_display_filters()

    def load_display_filters(self):
        self.settings = ProjectSettingsRepo().get()
        display_filters = self.settings['display_filters']

        host_index = self.setting_to_index(display_filters['host_setting'])
        self.ui.hostSettingDropdown.setCurrentIndex(host_index)

        self.ui.hostsText.setPlainText("\n".join(display_filters['host_list']))

    def save(self):
        host_setting_index = self.ui.hostSettingDropdown.currentIndex()
        host_setting = self.index_to_setting(host_setting_index)
        host_list = self.ui.hostsText.toPlainText().split("\n")

        display_filters = self.settings['display_filters']
        display_filters['host_list'] = list(filter(None, host_list))
        display_filters['host_setting'] = host_setting

        ProjectSettingsRepo().save(self.settings)
        self.display_filters_saved.emit()

        self.close()

    def host_setting_changed(self, index):
        self.ui.hostsText.setDisabled((index == 0))

    def setting_to_index(self, setting: str) -> int:
        if setting == 'include':
            return 1
        elif setting == 'exclude':
            return 2

        return 0

    def index_to_setting(self, index: int) -> str:
        if index == 1:
            return 'include'
        elif index == 2:
            return 'exclude'

        return ''
