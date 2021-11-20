import os
import pathlib

def is_dev_mode():
    return os.getenv('DEV_MODE') is not None

def get_include_path():
    if is_dev_mode():
        app_path = pathlib.Path(__file__).parent.parent.parent.absolute()
        return f"{app_path}/include"
    else:
        app_path = pathlib.Path(__file__).parent
        return f"{app_path}/include"
