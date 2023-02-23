import shutil
from pathlib import Path
import traceback
from typing import Optional
from PyQt6 import QtCore, QtGui, QtWidgets, QtXml
from lib.proxy_message_receiver import ProxyMessageReceiver
from services.proxy_service import ProxyService

from ui.views._compiled.main_window import Ui_MainWindow
from repos.app_settings_repo import AppSettingsRepo
from lib.database import Database
from lib.stylesheet_loader import StyleheetLoader
from ui.widgets.network.network_page import NetworkPage
from ui.widgets.intercept.intercept_page import InterceptPage
from ui.widgets.clients.clients_page import ClientsPage
from ui.widgets.editor.editor_page import EditorPage
from ui.widgets.preferences_window import PreferencesWindow

# Makes CTRL+C close the app:
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

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

        # Shortcut for closing app
        self.network_page.send_flow_to_editor.connect(self.editor_page.send_flow_to_editor)
        self.network_page.send_flow_to_editor.connect(self.show_editor_page)
        self.network_page.send_flow_to_fuzzer.connect(self.editor_page.send_flow_to_fuzzer)
        self.network_page.send_flow_to_fuzzer.connect(self.show_editor_page)

        self.intercept_page.something_intercepted.connect(self.ui.sideBar.highlight_intercept)
        self.intercept_page.intercept_queue_empty.connect(self.ui.sideBar.un_highlight_intercept)

        # Prefrences Window
        self.preferences_window = PreferencesWindow(self)
        self.preferences_window.network_layout_changed.connect(self.network_page.set_layout)
        self.preferences_window.app_settings_saved.connect(self.clients_page.load_available_clients)

        # Menubar:
        self.setup_menu_actions()
        self.restore_layout_state()

        # Sidebar:
        self.ui.sideBar.currentItemChanged.connect(self.sidebar_item_clicked)

        # For testing purposes only:
        # self.show_editor_page()
        keyseq_ctrl_r = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+R'), self)
        keyseq_ctrl_r.activated.connect(self.reload_style)

        # Status Bar
        self.intercept_status = QtWidgets.QPushButton()
        self.intercept_status.setText("Intercept: Disabled")
        self.intercept_status.setObjectName("interceptStatus")
        self.intercept_status.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.network_status = QtWidgets.QPushButton()
        self.network_status.setText("Network: Recording")
        self.network_status.setObjectName("networkStatus")
        self.network_status.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.proxy_status = QtWidgets.QLabel()
        self.proxy_status.setText("Proxies: None")
        self.proxy_status.setObjectName("proxyStatus")

        line1 = QtWidgets.QFrame(self)
        line1.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        line1.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        line1.setLineWidth(1)
        line1.setObjectName("statusBarLine")
        line2 = QtWidgets.QFrame(self)
        line2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        line2.setLineWidth(1)
        line2.setObjectName("statusBarLine")

        self.ui.statusBar.insertPermanentWidget(0, self.proxy_status)
        self.ui.statusBar.insertPermanentWidget(1, line1)
        self.ui.statusBar.insertPermanentWidget(2, self.network_status)
        self.ui.statusBar.insertPermanentWidget(3, line2)
        self.ui.statusBar.insertPermanentWidget(4, self.intercept_status)

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
    def set_proxy_service(self, proxy_service: ProxyService):
        self.process_manager = proxy_service.process_manager
        self.proxy_service = proxy_service

        # TODO: We could probably use the singleton get_instance() and set these in the page's constructors
        # Network Page:
        self.process_manager.proxy_request.connect(self.network_page.http_page.proxy_request_received)
        self.process_manager.proxy_response.connect(self.network_page.http_page.proxy_response_received)
        self.process_manager.proxy_ws_message.connect(self.network_page.ws_page.proxy_ws_message_received)

        self.network_status.clicked.connect(self.toggle_recording_enabled)
        self.intercept_status.clicked.connect(self.toggle_intercept_enabled)

        self.proxy_service.proxy_state_manager.recording_changed.connect(self.recording_changed)
        self.proxy_service.proxy_state_manager.intercept_changed.connect(self.intercept_changed)
    #     self.process_manager.clients_changed.connect(self.clients_changed)

    # def clients_changed(self):
    #     clients = self.process_manager.get_open_clients()

    #     if len(clients) > 0:
    #         proxy_ports = [str(c.proxy_port) for c in clients]
    #         proxy_ports_str = ",".join(proxy_ports)
    #         self.proxy_status.setText(f"Proxies: {proxy_ports_str}")
    #     else:
    #         self.proxy_status.setText("Proxies: None")

    def toggle_recording_enabled(self):
        self.proxy_service.proxy_state_manager.toggle_recording_enabled()

    def toggle_intercept_enabled(self):
        self.proxy_service.proxy_state_manager.toggle_intercept_enabled()

    def recording_changed(self):
        if self.proxy_service.proxy_state_manager.recording_enabled:
            self.network_status.setText("Network: Recording")
        else:
            self.network_status.setText("Network: Paused")

    def intercept_changed(self):
        if self.proxy_service.proxy_state_manager.intercept_enabled:
            self.intercept_status.setText("Intercept: Enabled")
        else:
            self.intercept_status.setText("Intercept: Disabled")

    def restore_layout_state(self):
        settings = AppSettingsRepo().get()
        geometry = settings["main_window_geometry"]

        if geometry is not None:
            self.restoreGeometry(geometry)

    def save_layout_state(self):
        settings = AppSettingsRepo().get()
        geometry = self.saveGeometry()
        settings["main_window_geometry"] = geometry
        AppSettingsRepo().save(settings)

    def reload_style(self):
        print("Reloading style...")
        style_loader = StyleheetLoader('/Users/evan/Code/pntest/src/ui/style')
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

    def sidebar_item_clicked(self, item: QtWidgets.QListWidgetItem, prev: QtWidgets.QListWidgetItem):
        item_value = item.data(QtCore.Qt.ItemDataRole.UserRole)

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

        database.reload_with_new_database(new_db_path)
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
