from typing import Optional
from PyQt6 import QtWidgets, QtCore
from repos.project_settings_repo import ProjectSettingsRepo
from repos.app_settings_repo import AppSettingsRepo
from repos.available_client_repo import AvailableClientRepo
from entities.available_client import AvailableClient
from ui.views._compiled.preferences_window import Ui_PreferencesWindow

class PreferencesWindow(QtWidgets.QDialog):
    available_clients: list[AvailableClient]
    browser_commands: dict[str, dict[str, str]]
    network_layout_changed = QtCore.pyqtSignal(str)
    app_settings_saved = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(PreferencesWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_PreferencesWindow()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)

        self.available_clients = AvailableClientRepo().find_all()
        self.load_settings()

    def showEvent(self, event):
        self.load_settings()

    def load_settings(self):
        self.project_settings = ProjectSettingsRepo().get()
        self.app_settings = AppSettingsRepo().get()

        ports = ','.join([str(port) for port in self.app_settings['proxy_ports_available']])
        self.ui.proxyPortsInput.setText(ports)

        # Browser commands
        self.browser_commands = {}

        self.__load_browser_cmd('chrome', self.ui.chromeCommandInput)
        self.__display_browser_cmd('chrome')
        self.__set_radio_buttons('chrome')

        self.__load_browser_cmd('chromium', self.ui.chromiumCommandInput)
        self.__display_browser_cmd('chromium')
        self.__set_radio_buttons('chromium')

        self.__load_browser_cmd('firefox', self.ui.firefoxCommandInput)
        self.__display_browser_cmd('firefox')
        self.__set_radio_buttons('firefox')

        self.ui.chromeAuto.toggled.connect(lambda: self.__setting_changed('chrome'))
        self.ui.chromiumAuto.toggled.connect(lambda: self.__setting_changed('chromium'))
        self.ui.firefoxAuto.toggled.connect(lambda: self.__setting_changed('firefox'))

        # Network settings
        self.__display_network_settings()

        self.ui.vertical1.toggled.connect(lambda: self.__network_layout_changed('vertical1'))
        self.ui.vertical2.toggled.connect(lambda: self.__network_layout_changed('vertical2'))
        self.ui.horizontal1.toggled.connect(lambda: self.__network_layout_changed('horizontal1'))
        self.ui.horizontal2.toggled.connect(lambda: self.__network_layout_changed('horizontal2'))

    def save(self):
        proxy_ports_str = self.ui.proxyPortsInput.text()
        proxy_ports = [int(p) for p in proxy_ports_str.split(',')]
        self.app_settings['proxy_ports_available'] = proxy_ports
        self.__update_settings_with_browser('chrome')
        self.__update_settings_with_browser('chromium')
        self.__update_settings_with_browser('firefox')

        AppSettingsRepo().save(self.app_settings)
        self.app_settings_saved.emit()
        self.close()

    def __display_network_settings(self):
        radio_vert_1 = self.ui.vertical1
        radio_vert_2 = self.ui.vertical2
        radio_horiz_1 = self.ui.horizontal1
        radio_horiz_2 = self.ui.horizontal2

        layout = self.app_settings['network_layout']
        if layout == 'vertical1':
            radio_vert_1.setChecked(True)
        elif layout == 'vertical2':
            radio_vert_2.setChecked(True)
        elif layout == 'horizontal1':
            radio_horiz_1.setChecked(True)
        elif layout == 'horizontal2':
            radio_horiz_2.setChecked(True)

    def __network_layout_changed(self, layout: str):
        self.app_settings['network_layout'] = layout
        self.network_layout_changed.emit(layout)

    def __update_settings_with_browser(self, browser_name: str):
        browser_cmd = self.browser_commands.get(browser_name)
        if browser_cmd is None:
            return

        if browser_cmd['setting'] != 'custom':
            if self.app_settings['browser_commands'].get(browser_name):
                del self.app_settings['browser_commands'][browser_name]
            return

        input: QtWidgets.QLineEdit = getattr(self.ui, f'{browser_name}CommandInput')
        custom_cmd = input.text()
        self.app_settings['browser_commands'][browser_name] = custom_cmd

    def __load_browser_cmd(self, browser_name: str, input: QtWidgets.QLineEdit):
        custom_cmd = self.app_settings['browser_commands'].get(browser_name)
        if custom_cmd:
            setting = 'custom'
        else:
            setting = 'auto'

        available_client = self.__get_available_client(browser_name)
        if available_client is None:
            return
        auto_cmd = available_client.command

        self.browser_commands[browser_name] = {
            'auto': auto_cmd or '',
            'custom': custom_cmd or '',
            'setting': setting
        }

    def __display_browser_cmd(self, browser_name: str):
        input: QtWidgets.QLineEdit = getattr(self.ui, f'{browser_name}CommandInput')
        cmd_auto = self.browser_commands[browser_name]['auto']
        cmd_custom = self.browser_commands[browser_name]['custom']

        if self.browser_commands[browser_name]['setting'] == 'auto':
            input.setText(cmd_auto)
            input.setReadOnly(True)
        elif self.browser_commands[browser_name]['setting'] == 'custom':
            input.setText(cmd_custom)
            input.setReadOnly(False)

    def __set_radio_buttons(self, browser_name: str):
        radioAuto: QtWidgets.QRadioButton = getattr(self.ui, f'{browser_name}Auto')
        radioCustom: QtWidgets.QRadioButton = getattr(self.ui, f'{browser_name}Custom')

        if self.browser_commands[browser_name]['setting'] == 'auto':
            radioAuto.setChecked(True)
            radioCustom.setChecked(False)
        elif self.browser_commands[browser_name]['setting'] == 'custom':
            radioAuto.setChecked(False)
            radioCustom.setChecked(True)

    def __setting_changed(self, browser_name: str):
        radioAuto: QtWidgets.QRadioButton = getattr(self.ui, f'{browser_name}Auto')

        if radioAuto.isChecked():
            setting = 'auto'
        else:
            setting = 'custom'

        self.browser_commands[browser_name]['setting'] = setting
        self.__display_browser_cmd(browser_name)

    def __get_available_client(self, client_name: str) -> Optional[AvailableClient]:
        return [b for b in self.available_clients if b.name == client_name][0]
