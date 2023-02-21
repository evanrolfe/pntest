from __future__ import annotations
from typing import Optional
from PyQt6 import QtCore
from entities.available_client import AvailableClient
from entities.browser import Browser
from entities.client import Client
from repos.browser_repo import BrowserRepo
from repos.client_repo import ClientRepo
from repos.process_repo import ProcessRepo
from repos.container_repo import ContainerRepo
from repos.project_settings_repo import ProjectSettingsRepo
from repos.app_settings_repo import AppSettingsRepo
from repos.available_client_repo import AvailableClientRepo

class AvailableClientService():
    def __init__(self):
        super().__init__()

    def get_all(self) -> list[AvailableClient]:
        settings = AppSettingsRepo().get()
        return AvailableClientRepo().find_all_with_settings_override(settings)
