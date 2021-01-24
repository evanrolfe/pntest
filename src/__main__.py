import sys
import traceback
import pathlib
import os
from PySide2.QtWidgets import QApplication, QLabel, QStyleFactory, QMessageBox
from PySide2.QtCore import QFile, QTextStream, Qt, QCoreApplication, QSettings
from PySide2.QtGui import QPalette, QColor

from lib.backend import Backend
from lib.database import Database
from lib.palettes import Palettes
from widgets.main_window import MainWindow

THEME = 'dark'
BACKEND_PATH_RELATIVE = 'include/pntest-core'

# Get absolute path to resource, works for dev and for PyInstaller
def resource_path(app_path, relative_path):
  default = app_path
  base_path = getattr(sys, '_MEIPASS', default)
  return os.path.join(base_path, relative_path)

def excepthook(type, value, tb):
  # TODO: Only close the backend if the exception is fatal
  backend = Backend.get_instance()
  backend.kill()

  print("----------------------------------------------------------")
  traceback_details = '\n'.join(traceback.extract_tb(tb).format())
  print(f"Type: {type}\nValue: {value}\nTraceback: {traceback_details}")

sys.excepthook = excepthook

def main():
  app = QApplication(sys.argv)

  app_path = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
  src_path = os.path.join(app_path, 'src')
  backend_path = resource_path(app_path, BACKEND_PATH_RELATIVE)
  data_path = resource_path(app_path, 'include')
  tmp_db_path = resource_path(app_path, 'pntest-tmp.db')
  style_dir_path = resource_path(src_path, 'style')

  print(f'[Frontend] App path: {app_path}')
  print(f'[Frontend] Backend path: {backend_path}')
  print(f'[Frontend] Data path: {data_path}')
  print(f'[Frontend] DB path: {tmp_db_path}')
  print(f'[Frontend] style dir path: {style_dir_path}')

  database = Database(tmp_db_path)
  database.delete_existing_db()
  database.load_or_create()

  backend = Backend(app_path, data_path, tmp_db_path, backend_path)
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
    style_path = os.path.join(style_dir_path, 'light.qss')
  elif (THEME == 'dark'):
    style_path = os.path.join(style_dir_path, 'dark.qss')

  print(f'--------> looking for style sheet in {style_path}')
  file = QFile(style_path)
  file.open(QFile.ReadOnly | QFile.Text)
  stream = QTextStream(file)
  app.setStyleSheet(stream.readAll())

  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
