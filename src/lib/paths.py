import sys
import pathlib
import os
from PyQt6.QtCore import QStandardPaths

from lib.utils import is_production_env

def get_app_config_path():
    return QStandardPaths.standardLocations(QStandardPaths.StandardLocation.AppConfigLocation)[0]

def get_app_path():
    if is_production_env():
        return pathlib.Path(__file__).parent.parent.absolute()
    else:
        return pathlib.Path(__file__).parent.parent.parent.absolute()

def get_include_path():
    if is_production_env():
        app_path = pathlib.Path(__file__).parent.parent
        return f"{app_path}/include"
    else:
        app_path = pathlib.Path(__file__).parent.parent.parent.absolute()
        return f"{app_path}/include"

# Get absolute path to resource, works for dev and for PyInstaller
def get_resource_path(app_path: str, relative_path: str):
    default = app_path
    base_path = getattr(sys, '_MEIPASS', default)
    return os.path.join(str(base_path), relative_path)
