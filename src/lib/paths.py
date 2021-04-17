from PySide2 import QtCore

def get_app_config_path():
    return QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.AppConfigLocation)[0]
