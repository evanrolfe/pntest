import sys
import pathlib
import os
from PySide2.QtCore import QStandardPaths

from lib.utils import is_dev_mode

def get_app_config_path():
    return QStandardPaths.standardLocations(QStandardPaths.AppConfigLocation)[0]  # type: ignore

def get_app_path():
    return pathlib.Path(__file__).parent.parent.absolute()

def get_include_path():
    if is_dev_mode():
        app_path = pathlib.Path(__file__).parent.parent.parent.absolute()
        return f"{app_path}/include"
    else:
        app_path = pathlib.Path(__file__).parent.parent
        return f"{app_path}/include"

# Get absolute path to resource, works for dev and for PyInstaller
def get_resource_path(app_path, relative_path):
    default = app_path
    base_path = getattr(sys, '_MEIPASS', default)
    return os.path.join(str(base_path), relative_path)
