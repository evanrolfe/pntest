from __future__ import annotations

from PyQt6 import QtCore

class AppSettings:
    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance() -> AppSettings:
        # Static access method.
        if AppSettings.__instance is not None:
            return AppSettings.__instance

        return AppSettings()

    def __init__(self):
        self.qsettings = QtCore.QSettings("Pntest", "Pntest")

        # Virtually private constructor.
        if AppSettings.__instance is not None:
            raise Exception("AppSettings class is a singleton!")
        else:
            AppSettings.__instance = self
    # /Singleton method stuff

    def get(self, key, default):
        return self.qsettings.value(key, default)

    def save(self, key, value):
        return self.qsettings.setValue(key, value)
