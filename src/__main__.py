import sys
import traceback
import pathlib

from PySide2.QtWidgets import QApplication, QLabel, QStyleFactory, QMessageBox
from PySide2.QtCore import QFile, QTextStream, Qt, QCoreApplication, QSettings
from PySide2.QtGui import QPalette, QColor

from lib.backend import Backend
from lib.database import Database
from lib.palettes import Palettes
from widgets.main_window import MainWindow

THEME = 'dark2'

DARK2_STYLE = """
QListWidget#sideBar {
  background: #3F3F3F;
}

QListWidget::item#sideBar {
  padding: 5px;
}

QListWidget::item::!selected#sideBar {
  border-left: 2px solid #3F3F3F;
}

QListWidget::item::selected#sideBar {
  border-left: 2px solid #2A82DA;
}

QTabWidget::pane {
  margin: 1px 1px 1px 1px;
  padding: -1px;
}
"""

LIGHT_STYLE = """
QTabWidget::pane {
  margin: 1px 1px 1px 1px;
  padding: -1px;
}
"""

def excepthook(type, value, tb):
  # TODO: Only close the backend if the exception is fatal
  backend = Backend.get_instance()
  backend.kill()

  print("----------------------------------------------------------")
  traceback_details = '\n'.join(traceback.extract_tb(tb).format())
  print(f"Type: {type}\nValue: {value}\nTraceback: {traceback_details}")

sys.excepthook = excepthook

def main_test():
  app = QApplication(sys.argv)

  # Create a simple dialog box
  msg_box = QMessageBox()
  msg_box.setText("Hello World!")
  msg_box.show()

  sys.exit(msg_box.exec_())

def main():
  app = QApplication(sys.argv)

  app_path = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
  db_path = '/home/evan/Desktop/oneproxy.db'

  print(f'[Frontend] App path: {app_path}')
  print(f'[Frontend] DB path: {db_path}')

  database = Database(db_path)
  database.load_or_create()

  backend = Backend(app_path, db_path)
  backend.register_callback('backendLoaded', lambda: print('Backend Loaded!'))
  backend.start()

  main_window = MainWindow()
  main_window.set_backend(backend)
  main_window.show()

  app.aboutToQuit.connect(main_window.about_to_quit)

  # Settings:
  QCoreApplication.setOrganizationName('PnTLimted')
  QCoreApplication.setOrganizationDomain('getpntest.com')
  QCoreApplication.setApplicationName('PnTest')

  # Style:
  app.setStyle('Fusion')

  if (THEME == 'light'):
    app.setStyleSheet(LIGHT_STYLE)
  elif (THEME == 'dark'):
    app.setPalette(Palettes.dark())
  elif (THEME == 'dark2'):
    # Setup stylesheet:
    file = QFile('/home/evan/Code/oneproxy/src/frontend/assets/style/dark2.qss')
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
