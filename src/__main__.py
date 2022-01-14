import sys
import os
from PySide2 import QtCore, QtWidgets, QtGui

from lib.paths import get_app_path, get_resource_path
from lib.process_manager import ProcessManager
from lib.database import Database
from lib.stylesheet_loader import StyleheetLoader
from widgets.main_window import MainWindow

THEME = 'dark'

def main():
    QtCore.QCoreApplication.setApplicationName('pntest')

    app = QtWidgets.QApplication(sys.argv)

    app_path = get_app_path()
    src_path = os.path.join(app_path, 'src')
    data_path = get_resource_path(app_path, 'include')
    tmp_db_path = get_resource_path(app_path, 'pntest-tmp.db')
    style_dir_path = get_resource_path(app_path, 'style')

    print(f'[Gui] App path: {app_path}')
    print(f'[Gui] Data path: {data_path}')
    print(f'[Gui] DB path: {tmp_db_path}')
    print(f'[Gui] style dir path: {style_dir_path}')

    # Load DB from the CLI if argument given
    try:
        tmp_db_path = sys.argv[1]
        print(f'[Frontend] Overridding DB path from CLI: {tmp_db_path}')
        database = Database(tmp_db_path)
        database.load_or_create()
    except IndexError:
        database = Database(tmp_db_path)
        database.delete_existing_db()
        database.load_or_create()

    process_manager = ProcessManager(src_path)
    main_window = MainWindow()
    main_window.set_process_manager(process_manager)
    main_window.show()

    app.aboutToQuit.connect(main_window.about_to_quit)  # type: ignore

    # Style:
    app.setStyle('Fusion')
    style_loader = StyleheetLoader(style_dir_path)
    stylesheet = style_loader.load_theme(THEME)

    if stylesheet is not None:
        app.setStyleSheet(stylesheet)

    # Icon:
    app.setWindowIcon(QtGui.QIcon(QtGui.QPixmap('/home/evan/Code/pntest/pntest-icon32.ico')))
    main_window.setWindowIcon(QtGui.QIcon(QtGui.QPixmap('/home/evan/Code/pntest/pntest-icon32.ico')))

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
