from typing import Optional
from PyQt6 import QtWidgets
from repos.settings_repo import SettingsRepo
from lib.browser_launcher.detect import detect_available_browsers, Browser
from views._compiled.preferences_window import Ui_PreferencesWindow

class PreferencesWindow(QtWidgets.QDialog):
    available_browsers: list[Browser]
    browser_commands: dict[str, dict[str, str]]

    def __init__(self, *args, **kwargs):
        super(PreferencesWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_PreferencesWindow()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)

        self.available_browsers = detect_available_browsers()
        self.load_settings()

    def showEvent(self, event):
        self.load_settings()

    def load_settings(self):
        self.settings = SettingsRepo().get_settings()
        print(self.settings.json)
        ports = ','.join([str(port) for port in self.settings.json['proxy']['ports_available']])
        self.ui.proxyPortsInput.setText(ports)

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

    def save(self):
        proxy_ports_str = self.ui.proxyPortsInput.text()
        proxy_ports = [int(p) for p in proxy_ports_str.split(',')]
        self.settings.json['proxy']['ports_available'] = proxy_ports
        self.__update_settings_with_browser('chrome')
        self.__update_settings_with_browser('chromium')
        self.__update_settings_with_browser('firefox')

        SettingsRepo().update(self.settings)
        self.close()

    def __update_settings_with_browser(self, browser_name: str):
        browser_cmd = self.browser_commands.get(browser_name)
        if browser_cmd is None:
            return

        if browser_cmd['setting'] != 'custom':
            if self.settings.json['browser']['browser_commands'].get(browser_name):
                del self.settings.json['browser']['browser_commands'][browser_name]
            return

        input: QtWidgets.QLineEdit = getattr(self.ui, f'{browser_name}CommandInput')
        custom_cmd = input.text()
        self.settings.json['browser']['browser_commands'][browser_name] = custom_cmd

    def __load_browser_cmd(self, browser_name: str, input: QtWidgets.QLineEdit):
        custom_cmd = self.settings.json['browser']['browser_commands'].get(browser_name)
        if custom_cmd:
            setting = 'custom'
        else:
            setting = 'auto'

        browser = self.__get_browser(browser_name)
        if browser is None:
            return
        auto_cmd = browser.get('command')

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

    def __get_browser(self, browser_name: str) -> Optional[Browser]:
        return [b for b in self.available_browsers if b['name'] == browser_name][0]
