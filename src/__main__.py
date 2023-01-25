import os
import sys
from PyQt6 import QtWidgets, QtGui, QtCore

from lib.paths import get_app_path, get_resource_path, get_app_config_path
from lib.process_manager import ProcessManager
from lib.database import Database
from lib.stylesheet_loader import StyleheetLoader
from widgets.main_window import MainWindow
from version import version

THEME = 'dark'

db_file_arg = None
version_arg = sys.argv[1] if len(sys.argv) > 1 else None
if version_arg == '--version':
    sys.exit(f'pntest v{version}')
else:
    db_file_arg = version_arg

def except_hook(cls, exception, traceback):
    print("------------------------------------------------\nERROR\n------------------------------------------------")
    print(traceback)
    sys.__excepthook__(cls, exception, traceback)

def main():
    QtCore.QCoreApplication.setApplicationName('pntest')

    app = QtWidgets.QApplication(sys.argv)

    # Determine paths
    app_path = get_app_path()
    src_path = os.path.join(app_path, 'src')
    tmp_db_path = get_resource_path(src_path, 'pntest-tmp.db')
    style_dir_path = get_resource_path(src_path, 'assets/style')
    assets_path = get_resource_path(src_path, 'assets')

    print(f'[Gui] App path: {app_path}')
    print(f'[Gui] DB path: {tmp_db_path}')
    print(f'[Gui] App config path: {get_app_config_path()}')
    print(f'[Gui] assets path: {assets_path}')

    QtCore.QDir.addSearchPath('assets', assets_path)

    # Ensure clean slate on start so delete the tmp db if it exists
    if db_file_arg:
        db_path = db_file_arg
    else:
        if os.path.isfile(tmp_db_path):
            print(f'[Gui] found existing db at {tmp_db_path}, deleting.')
            os.remove(tmp_db_path)

        db_path = tmp_db_path

    database = Database(db_path)

    process_manager = ProcessManager(str(app_path))
    main_window = MainWindow()
    main_window.set_process_manager(process_manager)
    main_window.show()
    sys.excepthook = main_window.exception_handler
    # On Quit:
    app.aboutToQuit.connect(main_window.about_to_quit)
    app.aboutToQuit.connect(process_manager.on_exit)

    # Style:
    app.setStyle('Fusion')
    style_loader = StyleheetLoader(style_dir_path)
    stylesheet = style_loader.load_theme(THEME)
    if stylesheet is not None:
        app.setStyleSheet(stylesheet)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
