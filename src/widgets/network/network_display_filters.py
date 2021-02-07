from PySide2 import QtWidgets

from views._compiled.network.ui_network_display_filters import Ui_NetworkDisplayFilters

class NetworkDisplayFilters(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NetworkDisplayFilters, self).__init__(parent)

        self.ui = Ui_NetworkDisplayFilters()
        self.ui.setupUi(self)
        self.setModal(True)
