from PySide2 import QtCore, QtWidgets

from views._compiled.network.http.ui_capture_filters import Ui_CaptureFilters
from models.data.capture_filter import CaptureFilter

class CaptureFilters(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CaptureFilters, self).__init__(parent)

        self.ui = Ui_CaptureFilters()
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

    @QtCore.Slot()  # type:ignore
    def save(self):
        host_setting_index = self.ui.hostSettingDropdown.currentIndex()
        host_setting = self.index_to_setting(host_setting_index)
        host_list = self.ui.hostsText.toPlainText().split("\n")

        path_setting_index = self.ui.pathSettingDropdown.currentIndex()
        path_setting = self.index_to_setting(path_setting_index)
        path_list = self.ui.pathsText.toPlainText().split("\n")

        self.capture_filters.set_filters({
            'host_list': list(filter(None, host_list)),
            'host_setting': host_setting,
            'path_list': list(filter(None, path_list)),
            'path_setting': path_setting
        })
        self.capture_filters.save()
        self.close()

    @QtCore.Slot()  # type:ignore
    def host_setting_changed(self, index):
        self.ui.hostsText.setDisabled((index == 0))

    @QtCore.Slot()  # type:ignore
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
