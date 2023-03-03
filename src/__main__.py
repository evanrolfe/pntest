import os
import sys

from PyQt6 import QtCore, QtWidgets

from lib.database import Database
from lib.paths import get_app_config_path, get_app_path, get_resource_path
from lib.stylesheet_loader import StyleheetLoader
from repos.process_repo import ProcessRepo
from services.open_clients_service import OpenClientsService
from services.proxy_service import ProxyService
from ui.widgets.main_window import MainWindow
from version import PNTEST_VERSION

THEME = 'dark'

db_file_arg = None
version_arg = sys.argv[1] if len(sys.argv) > 1 else None
if version_arg == '--version':
    sys.exit(f'pntest v{PNTEST_VERSION}')
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
    style_dir_path = get_resource_path(src_path, 'ui/style')
    assets_path = get_resource_path(src_path, 'ui/assets')

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

    proxy_service = ProxyService()

    client_service = OpenClientsService.get_instance()
    process_repo = ProcessRepo.get_instance()
    process_repo.set_app_path(str(app_path))

    main_window = MainWindow()
    main_window.set_proxy_service(proxy_service)
    main_window.show()
    sys.excepthook = main_window.exception_handler

    # On Quit:
    app.aboutToQuit.connect(main_window.about_to_quit)
    app.aboutToQuit.connect(client_service.on_exit)
    app.aboutToQuit.connect(proxy_service.process_manager.on_exit)

    # Style:
    app.setStyle('Fusion')
    style_loader = StyleheetLoader(style_dir_path)
    stylesheet = style_loader.load_theme(THEME)
    if stylesheet is not None:
        app.setStyleSheet(stylesheet)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
