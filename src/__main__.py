import os
import sys
from PyQt6 import QtWidgets, QtGui, QtCore

from lib.paths import get_app_path, get_resource_path
from lib.process_manager import ProcessManager
from lib.database import Database
from lib.stylesheet_loader import StyleheetLoader
from widgets.main_window import MainWindow
from version import version

THEME = 'dark'

version_arg = sys.argv[1] if 1 < len(sys.argv) else None
if version_arg == '--version':
    sys.exit(f'pntest v{version}')

def except_hook(cls, exception, traceback):
    print("------------------------------------------------\nERROR\n------------------------------------------------")
    print(traceback)
    sys.__excepthook__(cls, exception, traceback)

def main():
    sys.excepthook = except_hook

    QtCore.QCoreApplication.setApplicationName('pntest')

    app = QtWidgets.QApplication(sys.argv)

    # Determine paths
    app_path = get_app_path()
    src_path = os.path.join(app_path, 'src')
    tmp_db_path = get_resource_path(app_path, 'pntest-tmp.db')
    style_dir_path = get_resource_path(app_path, 'style')
    assets_path = get_resource_path(app_path, 'assets')

    print(f'[Gui] App path: {app_path}')
    print(f'[Gui] DB path: {tmp_db_path}')
    print(f'[Gui] style dir path: {style_dir_path}')
    print(f'[Gui] assets path: {assets_path}')

    QtCore.QDir.addSearchPath('assets', assets_path)

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
