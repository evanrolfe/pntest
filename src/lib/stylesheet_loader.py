import os
import re

from PySide2.QtCore import QFile, QTextStream, Qt

class StyleheetLoader:
  def __init__(self, style_dir_path):
    self.style_dir_path = style_dir_path

  def load_theme(self, theme):
    if (theme == 'light'):
      style_path = os.path.join(self.style_dir_path, 'light.qss')
    elif (theme == 'dark'):
      theme_path = os.path.join(self.style_dir_path, 'dark_theme.qss')
      style_path = os.path.join(self.style_dir_path, 'dark.qss')

    file = QFile(style_path)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)

    stylesheet = stream.readAll()
    theme_vars = self.get_theme_vars(theme_path)
    return self.replace_vars_in_stylesheet(stylesheet, theme_vars)

  def replace_vars_in_stylesheet(self, stylesheet, theme_vars):
    for key, value in theme_vars.items():
      stylesheet = stylesheet.replace('$' + key, value)

    return stylesheet

  def get_theme_vars(self, theme_path):
    file = QFile(theme_path)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    theme_str = stream.readAll()

    matches = re.search('\{(.*)\}', theme_str, flags=re.DOTALL)
    var_strings = matches[1].replace('\n', '').replace(' ', '').split(';')[:-1]

    var_map = {}
    for str in var_strings:
      key,value = str.split(':')
      var_map[key] = value

    return var_map

