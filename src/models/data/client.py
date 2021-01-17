from orator import Model

class Client(Model):
  def open_text(self):
    if (self.open):
      return 'Open'
    else:
      return 'Closed'
