from typing import Optional
from PyQt6 import QtCore
from entities.app_settings import AppSettings, get_default_app_settings

class AppSettingsRepo():
    qsettings: QtCore.QSettings

    NOT_FOUND_KEY = "not_found"

    def __init__(self, app_name: Optional[str] = None):
        if app_name is None:
            app_name = "PnTest"
        self.qsettings = QtCore.QSettings("Pntest", app_name)

    def get(self) -> AppSettings:
        app_settings = get_default_app_settings()
        for key, value in app_settings.items():
            result = self.qsettings.value(key, self.NOT_FOUND_KEY)
            if result != self.NOT_FOUND_KEY:
                app_settings[key] = result

        return app_settings

    def save(self, app_settings: AppSettings):
        for key, value in app_settings.items():
            self.qsettings.setValue(key, value)

