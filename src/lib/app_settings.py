from PySide2.QtCore import QSettings

class AppSettings:
  # Singleton method stuff:
  __instance = None
  @staticmethod
  def get_instance():
    # Static access method.
    if AppSettings.__instance == None:
        AppSettings()
    return AppSettings.__instance

  def __init__(self):
    self.qsettings = QSettings()

    # Virtually private constructor.
    if AppSettings.__instance != None:
        raise Exception("This class is a singleton!")
    else:
        AppSettings.__instance = self
  # /Singleton method stuff

  def get(self, key, default):
    return self.qsettings.value(key, default)

  def save(self, key, value):
    return self.qsettings.setValue(key, value)
