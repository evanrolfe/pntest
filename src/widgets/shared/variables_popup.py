from PySide2 import QtCore, QtWidgets

from views._compiled.shared.ui_variables_popup import Ui_VariablesPopup

class VariablesPopup(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(VariablesPopup, self).__init__(parent)

        self.ui = Ui_VariablesPopup()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)

    @QtCore.Slot()
    def save(self):
        print('You clicked save!')
        self.close()
