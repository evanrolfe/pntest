import sys
import pathlib
import os
from PySide2.QtCore import QStandardPaths

def get_app_config_path():
    return QStandardPaths.standardLocations(QStandardPaths.AppConfigLocation)[0]

def get_app_path():
    return pathlib.Path(__file__).parent.parent.absolute()

# Get absolute path to resource, works for dev and for PyInstaller
def get_resource_path(app_path, relative_path):
    default = app_path
    base_path = getattr(sys, '_MEIPASS', default)
    return os.path.join(base_path, relative_path)
