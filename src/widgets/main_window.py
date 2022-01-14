import shutil

from PySide2 import QtCore, QtGui, QtWidgets

# NOTE: This line is necessary for pyinstaller to succeed (for some reason):
from PySide2 import QtXml # noqa F401

from views._compiled.ui_main_window import Ui_MainWindow
from lib.app_settings import AppSettings
from lib.database import Database
from lib.stylesheet_loader import StyleheetLoader
from widgets.network.network_page import NetworkPage
from widgets.intercept.intercept_page import InterceptPage
from widgets.clients.clients_page import ClientsPage
from widgets.editor.editor_page import EditorPage

# pyside2-rcc assets/assets.qrc > assets_compiled/assets.py
import assets._compiled.assets # noqa F401

# Makes CTRL+C close the app:
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class MainWindow(QtWidgets.QMainWindow):
    reload_style = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('PnTest')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.toolBar.setVisible(False)

        # Setup pages:
        self.network_page = NetworkPage()
        self.intercept_page = InterceptPage()
        self.clients_page = ClientsPage()
        self.editor_page = EditorPage()

        # Setup stacked widget:
        self.ui.stackedWidget.addWidget(self.network_page)
        self.ui.stackedWidget.addWidget(self.intercept_page)
        self.ui.stackedWidget.addWidget(self.clients_page)
        self.ui.stackedWidget.addWidget(self.editor_page)
        self.ui.stackedWidget.setCurrentWidget(self.network_page)

        # Set padding on widgets:
        self.ui.centralWidget.layout().setContentsMargins(0, 0, 0, 0)

        # Add actions to sidebar:
        self.setup_sidebar()

        # Shortcut for closing app
        self.network_page.send_flow_to_editor.connect(self.editor_page.send_flow_to_editor)
        self.network_page.send_flow_to_editor.connect(self.show_editor_page)

        # Menubar:
        self.setup_menu_actions()
        self.restore_layout_state()

    # Wire-up the proxies (via the process_manager) to the pages and the InterceptQueue
    def set_process_manager(self, process_manager):
        self.process_manager = process_manager

        # TODO: We could probably use the singleton get_instance() and set these in the page's constructors
        # Network Page:
        self.process_manager.flow_created.connect(self.network_page.http_page.flow_created)
        self.process_manager.flow_updated.connect(self.network_page.http_page.flow_updated)
        self.process_manager.websocket_message_created.connect(self.network_page.ws_page.websocket_message_created)

    def restore_layout_state(self):
        settings = AppSettings.get_instance()
        geometry = settings.get('geometry', None)

        if geometry is not None:
            self.restoreGeometry(geometry)

    def save_layout_state(self):
        geometry = self.saveGeometry()

        settings = AppSettings.get_instance()
        settings.save('geometry', geometry)

    @QtCore.Slot()  # type:ignore
    def reload_style(self):
        style_loader = StyleheetLoader('/home/evan/Code/pntest/src/style/')
        stylesheet = style_loader.load_theme('dark')
        self.setStyleSheet(stylesheet)

        print('reloaded the stylesheet!')

    @QtCore.Slot()  # type:ignore
    def show_editor_page(self):
        self.ui.sideBar.setCurrentRow(3)
        self.ui.stackedWidget.setCurrentWidget(self.editor_page)

    @QtCore.Slot()  # type:ignore
    def about_to_quit(self):
        self.save_layout_state()
        self.network_page.save_layout_state()
        self.editor_page.save_layout_state()

    def exit(self):
        QtWidgets.QApplication.quit()

    def setup_sidebar(self):
        self.ui.sideBar.currentItemChanged.connect(self.sidebar_item_clicked)

        self.ui.sideBar.setObjectName('sideBar')

        self.ui.sideBar.setViewMode(QtWidgets.QListView.IconMode)
        self.ui.sideBar.setFlow(QtWidgets.QListView.TopToBottom)
        self.ui.sideBar.setMovement(QtWidgets.QListView.Static)
        self.ui.sideBar.setUniformItemSizes(True)
        # icon_size = QSize(52, 35)

        # Network Item
        network_item = QtWidgets.QListWidgetItem(QtGui.QIcon(":/icons/dark/icons8-cloud-backup-restore-50.png"), None)
        network_item.setData(QtCore.Qt.UserRole, 'network')
        # network_item.setSizeHint(icon_size)
        self.ui.sideBar.addItem(network_item)

        # Intercept Item
        intercept_item = QtWidgets.QListWidgetItem(QtGui.QIcon(":/icons/dark/icons8-rich-text-converter-50.png"), None)
        intercept_item.setData(QtCore.Qt.UserRole, 'intercept')
        self.ui.sideBar.addItem(intercept_item)

        # Clients Item
        clients_item = QtWidgets.QListWidgetItem(QtGui.QIcon(":/icons/dark/icons8-browse-page-50.png"), None)
        clients_item.setData(QtCore.Qt.UserRole, 'clients')
        self.ui.sideBar.addItem(clients_item)

        # Requests Item
        requests_item = QtWidgets.QListWidgetItem(QtGui.QIcon(":/icons/dark/icons8-compose-50.png"), None)
        requests_item.setData(QtCore.Qt.UserRole, 'requests')
        self.ui.sideBar.addItem(QtWidgets.QListWidgetItem(requests_item))

        # Extensions Item
        # extensions_item = QtWidgets.QListWidgetItem(QtGui.QIcon(":/icons/dark/icons8-plus-math-50.png"), None)
        # extensions_item.setData(QtCore.Qt.UserRole, 'extensions')
        # self.ui.sideBar.addItem(extensions_item)

        self.ui.sideBar.setCurrentRow(0)

    @QtCore.Slot()  # type:ignore
    def sidebar_item_clicked(self, item):
        item_value = item.data(QtCore.Qt.UserRole)

        if item_value == 'network':
            self.ui.stackedWidget.setCurrentWidget(self.network_page)
        elif item_value == 'intercept':
            self.ui.stackedWidget.setCurrentWidget(self.intercept_page)
        elif item_value == 'clients':
            self.ui.stackedWidget.setCurrentWidget(self.clients_page)
        elif item_value == 'requests':
            self.ui.stackedWidget.setCurrentWidget(self.editor_page)

    def reload(self):
        self.network_page.reload()
        self.editor_page.reload()
        self.clients_page.reload()

    @QtCore.Slot()  # type:ignore
    def open_project(self):
        # print('Resuming request...')
        # self.proxy_events_manager.resume_request()
        file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "~/",
            "PnTest Project Files (*.pnt *.db)"
        )
        db_path = file[0]
        print(f'Opening {db_path}')
        database = Database.get_instance()
        database.reload_with_new_database(db_path)

        self.reload()

    @QtCore.Slot()  # type:ignore
    def save_project_as(self):
        file = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Project As",
            "~/",
            "PnTest Project Files (*.pnt *.db)"
        )
        new_db_path = file[0]

        database = Database.get_instance()
        database.close()

        shutil.copy(database.db_path, new_db_path)
        print(f'[Frontend] Copied {database.db_path} to {new_db_path}')

        database.load_new_database(new_db_path)
        self.reload()

    def setup_menu_actions(self):
        self.ui.actionOpen.triggered.connect(self.open_project)
        self.ui.actionSave.triggered.connect(self.save_project_as)
