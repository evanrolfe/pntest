from orator import Model

class Setting(Model):
  @classmethod
  def create_defaults(cls):
    setting = Setting()
    setting.key = 'interceptEnabled'
    setting.value = 0
    setting.save()

  @classmethod
  def intercept_enabled(cls):
    setting = Setting.where('key', '=', 'interceptEnabled').first_or_fail()
    return (setting.value == '1')

