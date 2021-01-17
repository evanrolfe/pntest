import sys
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon

from views._compiled.ui_new_client_modal import Ui_NewClientModal

from lib.backend import Backend

CHROMIUM_COMMAND = b'{"command": "createClient", "type": "chromium"}'
CHROME_COMMAND = b'{"command": "createClient", "type": "chrome"}'
FIREFOX_COMMAND = b'{"command": "createClient", "type": "firefox"}'
ANYTHING_COMMAND = b'{"command": "createClient", "type": "anything"}'

class NewClientModal(QDialog):
  def __init__(self, parent = None):
    super(NewClientModal, self).__init__(parent)

    # Register callback with the backend:
    self.backend = Backend.get_instance()
    self.backend.register_callback('clientsAvailable', self.set_clients)

    self.ui = Ui_NewClientModal()
    self.ui.setupUi(self)
    self.setModal(True)

    self.client_buttons = [
      self.ui.chromiumButton,
      self.ui.chromeButton,
      self.ui.firefoxButton,
      self.ui.anythingButton
    ]

    # Add Icons:
    self.ui.chromiumButton.setIcon(QIcon(':/icons/icons8-chromium.svg'))
    self.ui.chromeButton.setIcon(QIcon(':/icons/icons8-chrome.svg'))
    self.ui.firefoxButton.setIcon(QIcon(':/icons/icons8-firefox.svg'))
    self.ui.anythingButton.setIcon(QIcon(':/icons/icons8-question-mark.png'))

    # Set Checkable
    for button in self.client_buttons:
      button.setCheckable(True)

    # Connect buttons
    self.ui.chromiumButton.clicked.connect(self.make_button_clicked('chromium'))
    self.ui.chromeButton.clicked.connect(self.make_button_clicked('chrome'))
    self.ui.firefoxButton.clicked.connect(self.make_button_clicked('firefox'))
    self.ui.anythingButton.clicked.connect(self.make_button_clicked('anything'))
    self.ui.cancelButton.clicked.connect(self.close)
    self.ui.launchButton.clicked.connect(self.launch_client)

    # Disable clients not available
    self.client_buttons = {
      'chromium': self.ui.chromiumButton,
      'chrome': self.ui.chromeButton,
      'firefox': self.ui.firefoxButton,
      'anything': self.ui.anythingButton
    }
    self.clients = []

    for browser_type, button in self.client_buttons.items():
      button.setEnabled(False)

    # Default is Chromium:
    self.ui.chromiumButton.setChecked(True)
    self.set_chromium_description()
    self.launch_command = CHROMIUM_COMMAND
    self.current_client_type = 'chromium'

  def showEvent(self, event):
    print("NewClientModal - showEvent")
    self.backend.get_available_clients()

  def set_clients(self, clients):
    self.clients = clients

    for client in clients:
      button = self.client_buttons[client['name']]
      button.setEnabled(True)

    # Update the anything button port
    anything_client_info = self.get_client_info('anything')
    self.ui.anythingButton.setText(f'Anything (Port {anything_client_info["proxyPort"]})')

    # Refresh the current client description:
    self.refresh_current_description()

  def make_button_clicked(self, browser_type):
    @Slot()
    def button_clicked():
      # Uncheck all buttons:
      for _browser_type, button in self.client_buttons.items():
        button.setChecked(False)

      if browser_type == 'chromium':
        self.set_chromium_description()
        self.ui.chromiumButton.setChecked(True)
        self.launch_command = CHROMIUM_COMMAND

      elif browser_type == 'chrome':
        self.set_chrome_description()
        self.ui.chromeButton.setChecked(True)
        self.launch_command = CHROME_COMMAND

      elif browser_type == 'firefox':
        self.set_firefox_description()
        self.ui.firefoxButton.setChecked(True)
        self.launch_command = FIREFOX_COMMAND

      elif browser_type == 'anything':
        self.set_anything_description()
        self.ui.anythingButton.setChecked(True)
        self.launch_command = ANYTHING_COMMAND

    self.current_client_type = browser_type

    return button_clicked

  @Slot()
  def launch_client(self):
    self.backend.send_command(self.launch_command)
    self.close()

  def refresh_current_description(self):
    self.current_client_type
    if self.current_client_type == 'chromium':
      self.set_chromium_description()

    elif self.current_client_type == 'chrome':
      self.set_chrome_description()

    elif self.current_client_type == 'firefox':
      self.set_firefox_description()

    elif self.current_client_type == 'anything':
      self.set_anything_description()

  def set_chromium_description(self):
    client_info = self.get_client_info('chromium')

    text = 'Launch a new Chromium instance:\n\n'
    text += '- Isolated from all other browser instances\n'
    text += f'- Pre-configured to use proxy port {client_info["proxyPort"]} and accept OneProxy SSL Certificates\n'
    text += f'- Records rendered HTML from the browser using port {client_info["browserPort"]}\n'
    text += f'- Version {client_info["version"]}\n'
    text += f'- Command: {client_info["command"]}\n'

    self.ui.descLabel.setText(text)

  def set_chrome_description(self):
    client_info = self.get_client_info('chrome')

    text = 'Launch a new Chrome instance:\n\n'
    text += '- Isolated from all other browser instances\n'
    text += f'- Pre-configured to use proxy port {client_info["proxyPort"]} and accept OneProxy SSL Certificates\n'
    text += f'- Records rendered HTML from the browser using port {client_info["browserPort"]}\n'
    text += f'- Version {client_info["version"]}\n'
    text += f'- Command: {client_info["command"]}\n'

    self.ui.descLabel.setText(text)

  def set_firefox_description(self):
    client_info = self.get_client_info('firefox')

    text = 'Launch a new Firefox instance:\n\n'
    text += '- Isolated from all other browser instances\n'
    text += f'- Pre-configured to use proxy port {client_info["proxyPort"]} and accept OneProxy SSL Certificates\n'
    text += f'- DOES NOT Record rendered HTML from the browser as this is not yet supported by Firefox\n'
    text += f'- Version {client_info["version"]}\n'
    text += f'- Command: {client_info["command"]}\n'

    self.ui.descLabel.setText(text)

  def set_anything_description(self):
    client_info = self.get_client_info('anything')

    text = 'Launch a new proxy instance:\n\n'
    text += f'- Opens a proxy on port {client_info["proxyPort"]}\n'

    self.ui.descLabel.setText(text)

  def get_client_info(self, browser_type):
    client_infos = [c for c in self.clients if c['type'] == browser_type]

    if len(client_infos) == 0:
      client_info = {'version': 'N/A', 'proxyPort': 'N/A', 'browserPort': 'N/A', 'command': 'N/A'}
    else:
      client_info = client_infos[0]

    return client_info
