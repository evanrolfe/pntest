from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPixmap, QColor

from views._compiled.shared.ui_loader import Ui_Loader
from widgets.qt.waiting_spinner import QtWaitingSpinner


class Loader(QWidget):
    def __init__(self, *args, **kwargs):
        super(Loader, self).__init__(*args, **kwargs)
        self.ui = Ui_Loader()
        self.ui.setupUi(self)

        #img = QPixmap(':/icons/dark/loader.gif')
        # self.ui.loaderIconLabel.setText('hello')
        # self.ui.loaderIconLabel.setPixmap(img)
        spinner = QtWaitingSpinner(self.ui.spinnerWidget)

        spinner.setRoundness(70.0)
        spinner.setMinimumTrailOpacity(15.0)
        spinner.setTrailFadePercentage(70.0)
        spinner.setNumberOfLines(12)
        spinner.setLineLength(5)
        spinner.setLineWidth(5)
        spinner.setInnerRadius(10)
        spinner.setRevolutionsPerSecond(0.75)
        spinner.setColor(QColor('#D4D4D4'))

        spinner.start()
