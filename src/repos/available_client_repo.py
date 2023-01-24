import platform
import re
import sqlite3
import subprocess
from typing import Generic, Optional, Type, TypeVar
from models.app_settings import AppSettings
from models.available_client import AvailableClient

DEFAULT_CLIENTS = [
    {
        'name': 'chrome',
        'commands': [
            'chrome',
            'google-chrome',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        ],
        'regex': r'Google Chrome (.+)',
        'type': 'chrome',
        'command': None,
        'version': None
    },
    {
        'name': 'chromium',
        'commands': ['chromium', 'chromium-browser'],
        'regex': r'Chromium ([0-9,\.]+) (.+)',
        'type': 'chrome',
        'command': None,
        'version': None
    },
    {
        'name': 'firefox',
        'commands': [
            'firefox',
            '/Applications/Firefox.app/Contents/MacOS/firefox-bin'
        ],
        'regex': r'Mozilla Firefox (.+)',
        'type': 'firefox',
        'command': None,
        'version': None
    },
    {
        'name': 'docker',
        'commands': ['docker'],
        'regex': r'Docker version ([0-9,\.]+), (.+)',
        'type': 'docker',
        'command': None,
        'version': None
    },
    {
        'name': 'anything',
        'commands': [],
        'regex': r'',
        'type': 'anything',
        'command': None,
        'version': None
    }
]

class AvailableClientRepo():
    def __init__(self):
        super().__init__()

    def find_all(self) -> list[AvailableClient]:
        return self.find_all_with_settings_override()

    def find_all_with_settings_override(self, settings: Optional[AppSettings] = None) -> list[AvailableClient]:
        clients: list[AvailableClient] = []
        for default_client in DEFAULT_CLIENTS:
            client = AvailableClient(**default_client)
            client.verify_command()

            # Apply the settings override command, if it exists
            if settings:
                override_command = settings['browser_commands'].get(client.name)
                if override_command:
                    client.command = override_command

            clients.append(client)

        return clients
