import sys
import traceback
import pathlib

from PySide2.QtWidgets import QApplication, QLabel, QStyleFactory, QMessageBox

from lib.backend import Backend
from widgets.main_window import MainWindow

def main():
  app = QApplication(sys.argv)

  backend = Backend()
  main_window = MainWindow()

  # Create a simple dialog box
  msg_box = QMessageBox()
  msg_box.setText(backend.hello())
  msg_box.show()

  sys.exit(msg_box.exec_())

if __name__ == "__main__":
  main()
