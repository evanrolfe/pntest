from PyQt6 import QtWidgets

from views._compiled.preferences_window import Ui_PreferencesWindow

class PreferencesWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(PreferencesWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_PreferencesWindow()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)

    def save(self):
        # TODO
        self.close()
