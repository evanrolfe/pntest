from PySide2 import QtWidgets

from views._compiled.network.http.ui_display_filters import Ui_DisplayFilters

class DisplayFilters(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DisplayFilters, self).__init__(parent)

        self.ui = Ui_DisplayFilters()
        self.ui.setupUi(self)
        self.setModal(True)
