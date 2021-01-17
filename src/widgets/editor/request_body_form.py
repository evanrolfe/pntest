from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader

from views._compiled.editor.ui_request_body_form import Ui_RequestBodyForm

class RequestBodyForm(QWidget):
  def __init__(self, editor_item, *args, **kwargs):
    super(RequestBodyForm, self).__init__(*args, **kwargs)
    self.ui = Ui_RequestBodyForm()
    self.ui.setupUi(self)
    self.editor_item = editor_item
    self.load_body()

  def load_body(self):
    body = self.editor_item.item().request_payload
    if body != None:
      self.ui.requestBodyInput.setPlainText(body)

  def get_body(self):
    return self.ui.requestBodyInput.toPlainText()
