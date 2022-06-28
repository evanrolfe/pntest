from PySide2 import QtWidgets

from views._compiled.ui_preferences_window import Ui_PreferencesWindow

class PreferencesWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(PreferencesWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_PreferencesWindow()
        self.ui.setupUi(self)
        self.setModal(True)
