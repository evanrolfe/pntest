import os
import re

from PyQt6 import QtCore

class StyleheetLoader:
    def __init__(self, style_dir_path):
        self.style_dir_path = style_dir_path

    def load_theme(self, theme):
        if (theme == 'light'):
            style_path = os.path.join(self.style_dir_path, 'light.qss')

            theme_vars = {}
        elif (theme == 'dark'):
            theme_path = os.path.join(self.style_dir_path, 'dark_theme.qss')
            style_path = os.path.join(self.style_dir_path, 'dark.qss')

            theme_vars = self.get_theme_vars(theme_path)
        else:
            return

        file = QtCore.QFile(style_path)
        file.open(QtCore.QIODeviceBase.OpenModeFlag.ReadOnly | QtCore.QIODeviceBase.OpenModeFlag.Text)
        stream = QtCore.QTextStream(file)

        stylesheet = stream.readAll()

        return self.replace_vars_in_stylesheet(stylesheet, theme_vars)

    def replace_vars_in_stylesheet(self, stylesheet, theme_vars):
        for key, value in theme_vars.items():
            stylesheet = stylesheet.replace('$' + key, value)

        return stylesheet

    def get_theme_vars(self, theme_path):
        file = QtCore.QFile(theme_path)
        file.open(QtCore.QIODeviceBase.OpenModeFlag.ReadOnly | QtCore.QIODeviceBase.OpenModeFlag.Text)
        stream = QtCore.QTextStream(file)
        theme_str = stream.readAll()

        matches = re.search(r'\{(.*)\}', theme_str, flags=re.DOTALL)  # noqa W605

        if matches is None:
            return

        match = matches[1]

        if match is None:
            return

        var_strings = match.replace('\n', '').replace(' ', '').split(';')[:-1]

        var_map = {}
        for str in var_strings:
            key, value = str.split(':')
            var_map[key] = value

        return var_map
