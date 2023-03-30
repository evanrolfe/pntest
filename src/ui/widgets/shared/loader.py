from PyQt6 import QtCore, QtWidgets

from ui.views._compiled.shared.loader import Ui_Loader
from ui.widgets.qt.waiting_spinner import QtWaitingSpinner


class Loader(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Loader, self).__init__(*args, **kwargs)
        self.ui = Ui_Loader()
        self.ui.setupUi(self)

        spinner = QtWaitingSpinner(self.ui.spinnerWidget)

        spinner.setRoundness(70.0)
        spinner.setMinimumTrailOpacity(15.0)
        spinner.setTrailFadePercentage(70.0)
        spinner.setNumberOfLines(12)
        spinner.setLineLength(5)
        spinner.setLineWidth(5)
        spinner.setInnerRadius(10)
        spinner.setRevolutionsPerSecond(0.75)
        # TODO: Change this to QtGui.QColor('#D4D4D4')
        spinner.setColor(QtCore.Qt.GlobalColor.white)

        spinner.start()
