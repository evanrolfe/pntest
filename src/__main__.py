import sys
import pathlib
import os
import atexit
from PySide2 import QtCore, QtWidgets

from lib.proxy_events_service import ProxyEventsWorker
from lib.process_manager import ProcessManager
from lib.database import Database
from lib.stylesheet_loader import StyleheetLoader
from widgets.main_window import MainWindow

THEME = 'dark'
BACKEND_PATH_RELATIVE = 'include/pntest-core'

# Get absolute path to resource, works for dev and for PyInstaller
def resource_path(app_path, relative_path):
    default = app_path
    base_path = getattr(sys, '_MEIPASS', default)
    return os.path.join(base_path, relative_path)

def main():
    app = QtWidgets.QApplication(sys.argv)

    app_path = pathlib.Path(__file__).parent.parent.absolute()
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

    process_manager = ProcessManager()
    main_window = MainWindow()
    main_window.set_process_manager(process_manager)
    main_window.show()

    app.aboutToQuit.connect(main_window.about_to_quit)

    # Settings:
    QtCore.QCoreApplication.setOrganizationName('PnT Limted')
    QtCore.QCoreApplication.setOrganizationDomain('getpntest.com')
    QtCore.QCoreApplication.setApplicationName('PnTest')

    # Style:
    app.setStyle('Fusion')
    style_loader = StyleheetLoader(style_dir_path)
    stylesheet = style_loader.load_theme(THEME)
    app.setStyleSheet(stylesheet)

    process_manager.launch_proxy(8080)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
