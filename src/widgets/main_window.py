import shutil
from pathlib import Path
import traceback
from PyQt6 import QtCore, QtGui, QtWidgets, QtXml

from views._compiled.main_window import Ui_MainWindow
from lib.app_settings import AppSettings
from lib.database import Database
from lib.database_cache import DatabaseCache
from lib.stylesheet_loader import StyleheetLoader
from widgets.network.network_page import NetworkPage
from widgets.intercept.intercept_page import InterceptPage
from widgets.clients.clients_page import ClientsPage
from widgets.editor.editor_page import EditorPage
from widgets.preferences_window import PreferencesWindow

# Makes CTRL+C close the app:
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# https://stackoverflow.com/questions/34445507/change-background-color-of-qwidget-using-animation
class Sidebar(QtWidgets.QListWidget):
    def setColor(self, color: QtGui.QColor):
        r = color.red()
        g = color.green()
        b = color.blue()

        super().setStyleSheet("""QListWidget::item::selected#sideBar {
            border-left: 2px solid #FC6A0C;
            background: #FC6A0C;
        }""")

class MainWindow(QtWidgets.QMainWindow):
    # reload_style = QtCore.Signal()

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

        # Prefrences Window
        self.preferences_window = PreferencesWindow(self)

        # Menubar:
        self.setup_menu_actions()
        self.restore_layout_state()

        # For testing purposes only:
        self.show_editor_page()
        keyseq_ctrl_r = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+R'), self)
        keyseq_ctrl_r.activated.connect(self.reload_style)

    def exception_handler(self, type, exception, tb):
        print("------------------------------------------------\nERROR\n------------------------------------------------")
        exception_str = "\n".join(traceback.format_exception_only(exception))
        traceback_str = "\n".join(traceback.format_tb(tb))

        error_message =  exception_str + "\n" + traceback_str
        print(error_message)

        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('Error')
        message_box.setText(error_message)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.exec()

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

    def reload_style(self):
        print("Reloading style...")
        style_loader = StyleheetLoader('/Users/evan/Code/pntest/src/style')
        stylesheet = style_loader.load_theme('dark')
        if stylesheet is None:
            return
        self.setStyleSheet(stylesheet)

    def show_editor_page(self):
        self.ui.sideBar.setCurrentRow(3)
        self.ui.stackedWidget.setCurrentWidget(self.editor_page)

    def about_to_quit(self):
        self.save_layout_state()
        self.network_page.save_layout_state()
        self.editor_page.save_layout_state()

    def exit(self):
        QtWidgets.QApplication.quit()

    def setup_sidebar(self):
        self.ui.sideBar.currentItemChanged.connect(self.sidebar_item_clicked)

        self.ui.sideBar.setObjectName('sideBar')

        self.ui.sideBar.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.ui.sideBar.setFlow(QtWidgets.QListView.Flow.TopToBottom)
        self.ui.sideBar.setMovement(QtWidgets.QListView.Movement.Static)
        self.ui.sideBar.setUniformItemSizes(True)
        # icon_size = QSize(52, 35)

        # Network Item
        network_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-cloud-backup-restore-50.png"), "Network", None)
        network_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'network')
        network_item.setToolTip("Network")
        self.ui.sideBar.addItem(network_item)

        # Intercept Item
        intercept_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-rich-text-converter-50.png"), "Intercept", None)
        intercept_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'intercept')
        intercept_item.setToolTip("Intercept")
        self.ui.sideBar.addItem(intercept_item)

        # Clients Item
        clients_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-browse-page-50.png"), "Clients", None)
        clients_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'clients')
        clients_item.setToolTip("Clients")
        self.ui.sideBar.addItem(clients_item)

        # Requests Item
        requests_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-compose-50.png"), "Requests", None)
        requests_item.setData(QtCore.Qt.ItemDataRole.UserRole, 'requests')
        requests_item.setToolTip("Request Editor")
        self.ui.sideBar.addItem(requests_item)

        # Extensions Item
        # extensions_item = QtWidgets.QListWidgetItem(QtGui.QIcon("assets:icons/dark/icons8-plus-math-50.png"), None)
        # extensions_item.setData(QtCore.Qt.UserRole, 'extensions')
        # self.ui.sideBar.addItem(extensions_item)
        self.ui.sideBar.setCurrentRow(0)

    def sidebar_item_clicked(self, item):
        item_value = item.data(QtCore.Qt.ItemDataRole.UserRole)

        if item_value == 'network':
            print('todo')
            self.ui.stackedWidget.setCurrentWidget(self.network_page)
        elif item_value == 'intercept':
            print('todo')
            self.ui.stackedWidget.setCurrentWidget(self.intercept_page)
        elif item_value == 'clients':
            self.ui.stackedWidget.setCurrentWidget(self.clients_page)
        elif item_value == 'requests':
            print('todo')
            self.ui.stackedWidget.setCurrentWidget(self.editor_page)

    def reload(self):
        self.network_page.reload()
        self.editor_page.reload()
        self.clients_page.reload()

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

        if db_path == '':  # Cancel was pressed:
            return

        print(f'Opening {db_path}')
        database_cache = DatabaseCache.get_instance()
        database_cache.clear()

        database = Database.get_instance()
        database.reload_with_new_database(db_path)

        self.reload()

    def save_project_as(self):
        file = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Project As",
            "~/",
            ".pnt"
        )
        new_db_path = file[0]

        ext = Path(new_db_path).suffix
        if ext == '':
            new_db_path += '.pnt'

        database = Database.get_instance()
        database.close()

        shutil.copy(database.db_path, new_db_path)
        print(f'[Frontend] Copied {database.db_path} to {new_db_path}')

        database.load_new_database(new_db_path)
        self.reload()

    def show_preferences(self):
        self.preferences_window.show()

    def setup_menu_actions(self):
        # File menu
        fileMenu = self.menuBar().addMenu("&File")

        action_open = fileMenu.addAction("Open project")
        action_save = fileMenu.addAction("Save project as")
        action_preferences = fileMenu.addAction("Preferences")

        action_open.triggered.connect(self.open_project)
        action_save.triggered.connect(self.save_project_as)
        action_preferences.triggered.connect(self.show_preferences)
