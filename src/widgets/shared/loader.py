from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPixmap

from views._compiled.shared.ui_loader import Ui_Loader

class Loader(QWidget):
  def __init__(self, *args, **kwargs):
    super(Loader, self).__init__(*args, **kwargs)
    self.ui = Ui_Loader()
    self.ui.setupUi(self)

    #img = QPixmap(':/icons/dark/loader.gif')
    #self.ui.loaderIconLabel.setText('hello')
    #self.ui.loaderIconLabel.setPixmap(img)
