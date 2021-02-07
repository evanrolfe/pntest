import sys
import pathlib
import shutil

from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QHeaderView, QAbstractItemView, QStackedWidget, QToolButton, QAction, QMenu, QShortcut, QListWidgetItem, QListView, QFileDialog
from PySide2.QtCore import QFile, Qt, QTextStream, QResource, SIGNAL, Slot, QPoint, QSize, QSettings, Signal
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtGui import QIcon, QKeySequence
# NOTE: This line is necessary for pyinstaller to succeed (for some reason):
from PySide2 import QtXml

from views._compiled.ui_main_window import Ui_MainWindow

from lib.app_settings import AppSettings
from lib.database import Database
from lib.stylesheet_loader import StyleheetLoader
from widgets.network.network_page_widget import NetworkPageWidget
from widgets.intercept.intercept_page import InterceptPage
from widgets.clients.clients_page import ClientsPage
from widgets.crawls.crawls_page import CrawlsPage
from widgets.editor.editor_page import EditorPage

# pyside2-rcc assets/assets.qrc > assets_compiled/assets.py
import assets._compiled.assets

# Makes CTRL+C close the app:
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class MainWindow(QMainWindow):
    reload_style = Signal()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('PnTest')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.toolBar.setVisible(False)

        # Setup pages:
        self.network_page_widget = NetworkPageWidget()
        self.intercept_page = InterceptPage()
        self.clients_page = ClientsPage()
        self.crawls_page = CrawlsPage()
        self.editor_page = EditorPage()

        # Setup stacked widget:
        self.ui.stackedWidget.addWidget(self.network_page_widget)
        self.ui.stackedWidget.addWidget(self.intercept_page)
        self.ui.stackedWidget.addWidget(self.clients_page)
        self.ui.stackedWidget.addWidget(self.crawls_page)
        self.ui.stackedWidget.addWidget(self.editor_page)
        self.ui.stackedWidget.setCurrentWidget(self.network_page_widget)

        # Set padding on widgets:
        self.ui.centralWidget.layout().setContentsMargins(0, 0, 0, 0)

        # Add actions to sidebar:
        self.setup_sidebar()

        # Shortcut for closing app:
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_C),
                               self), SIGNAL('activated()'), self.exit)
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R),
                               self), SIGNAL('activated()'), self.reload_style)

        self.network_page_widget.send_request_to_editor.connect(
            self.editor_page.send_request_to_editor)
        self.network_page_widget.send_request_to_editor.connect(
            self.show_editor_page)

        # Menubar:
        self.setup_menu_actions()
        self.restore_layout_state()
        self.show_editor_page()

    def set_backend(self, backend):
        self.backend = backend

    def restore_layout_state(self):
        settings = AppSettings.get_instance()
        geometry = settings.get('geometry', None)

        if (geometry != None):
            self.restoreGeometry(geometry)

    def save_layout_state(self):
        geometry = self.saveGeometry()

        settings = AppSettings.get_instance()
        settings.save('geometry', geometry)

    @Slot()
    def reload_style(self):
        style_loader = StyleheetLoader('/home/evan/Code/pntest/src/style/')
        stylesheet = style_loader.load_theme('dark')
        self.setStyleSheet(stylesheet)

        print('reloaded the stylesheet!')

    @Slot()
    def show_editor_page(self):
        self.ui.sideBar.setCurrentRow(3)
        self.ui.stackedWidget.setCurrentWidget(self.editor_page)

    @Slot()
    def about_to_quit(self):
        self.save_layout_state()
        self.network_page_widget.save_layout_state()
        self.editor_page.save_layout_state()
        self.backend.kill()

    def exit(self):
        QApplication.quit()

    def setup_sidebar(self):
        self.ui.sideBar.currentItemChanged.connect(self.sidebar_item_clicked)

        self.ui.sideBar.setObjectName('sideBar')

        self.ui.sideBar.setViewMode(QListView.IconMode)
        self.ui.sideBar.setFlow(QListView.TopToBottom)
        self.ui.sideBar.setMovement(QListView.Static)
        self.ui.sideBar.setUniformItemSizes(True)
        #icon_size = QSize(52, 35)

        # Network Item
        network_item = QListWidgetItem(
            QIcon(":/icons/dark/icons8-cloud-backup-restore-50.png"), None)
        network_item.setData(Qt.UserRole, 'network')
        # network_item.setSizeHint(icon_size)
        self.ui.sideBar.addItem(network_item)

        # Intercept Item
        intercept_item = QListWidgetItem(
            QIcon(":/icons/dark/icons8-rich-text-converter-50.png"), None)
        intercept_item.setData(Qt.UserRole, 'intercept')
        self.ui.sideBar.addItem(intercept_item)

        # Clients Item
        clients_item = QListWidgetItem(
            QIcon(":/icons/dark/icons8-browse-page-50.png"), None)
        clients_item.setData(Qt.UserRole, 'clients')
        self.ui.sideBar.addItem(clients_item)

        # Requests Item
        requests_item = QListWidgetItem(
            QIcon(":/icons/dark/icons8-compose-50.png"), None)
        requests_item.setData(Qt.UserRole, 'requests')
        self.ui.sideBar.addItem(QListWidgetItem(requests_item))

        # Crawler Item
        crawler_item = QListWidgetItem(
            QIcon(":/icons/dark/icons8-spiderweb-50.png"), None)
        crawler_item.setData(Qt.UserRole, 'crawler')
        self.ui.sideBar.addItem(crawler_item)

        # Extensions Item
        extensions_item = QListWidgetItem(
            QIcon(":/icons/dark/icons8-plus-math-50.png"), None)
        extensions_item.setData(Qt.UserRole, 'extensions')
        self.ui.sideBar.addItem(extensions_item)

        self.ui.sideBar.setCurrentRow(0)

    @Slot()
    def sidebar_item_clicked(self, item):
        item_value = item.data(Qt.UserRole)

        if item_value == 'network':
            self.ui.stackedWidget.setCurrentWidget(self.network_page_widget)
        elif item_value == 'intercept':
            self.ui.stackedWidget.setCurrentWidget(self.intercept_page)
        elif item_value == 'clients':
            self.ui.stackedWidget.setCurrentWidget(self.clients_page)
        elif item_value == 'crawler':
            self.ui.stackedWidget.setCurrentWidget(self.crawls_page)
        elif item_value == 'requests':
            self.ui.stackedWidget.setCurrentWidget(self.editor_page)

    def reload(self):
        self.network_page_widget.reload()
        self.editor_page.reload()
        self.clients_page.reload()

    @Slot()
    def open_project(self):
        file = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "~/",
            "PnTest Project Files (*.pnt *.db)"
        )
        db_path = file[0]
        print(f'Opening {db_path}')
        database = Database.get_instance()
        database.reload_with_new_database(db_path)
        self.backend.reload_with_new_database(db_path)

        self.reload()

    @Slot()
    def save_project_as(self):
        file = QFileDialog.getSaveFileName(
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

        # self.backend.reload_with_new_database(file_path)

    def setup_menu_actions(self):
        self.ui.actionOpen.triggered.connect(self.open_project)
        self.ui.actionSave.triggered.connect(self.save_project_as)
