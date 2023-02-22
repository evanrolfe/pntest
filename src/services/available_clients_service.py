from __future__ import annotations

from entities.available_client import AvailableClient
from repos.app_settings_repo import AppSettingsRepo
from repos.available_client_repo import AvailableClientRepo

# AvailableClientsService returns a list of clients that are available to be started on this machine
class AvailableClientsService():
    def __init__(self):
        super().__init__()

    def get_all(self) -> list[AvailableClient]:
        settings = AppSettingsRepo().get()
        return AvailableClientRepo().find_all_with_settings_override(settings)
