from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from models.model import Model

from mitmproxy.common_types import SettingsJson, CaptureFilterSettings, DisplayFilterSettings, ProxySettings, BrowserSettings

@dataclass(kw_only=True)
class Settings(Model):
    # Columns
    id: int = field(init=False, default=0)
    created_at: int = field(init=False, default=0)

    json: SettingsJson

    # Relations

    meta = {
        "relationship_keys": [],
        "json_columns": ["json"],
        "do_not_save_keys": [],
    }

    @classmethod
    def build_default(cls):
        capture_filters: CaptureFilterSettings = {
            'host_list': [],
            'host_setting': '',
            'path_list': [],
            'path_setting': '',
        }
        display_filters: DisplayFilterSettings = {
            'host_list': [],
            'host_setting': '',
            'path_list': [],
            'path_setting': '',
        }
        proxy_settings: ProxySettings = { 'ports_available': [8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089] }
        browser_settings: BrowserSettings = { 'browser_commands': {} }
        settings_json: SettingsJson = {
            'capture_filters': capture_filters,
            'display_filters': display_filters,
            'proxy': proxy_settings,
            'browser': browser_settings
        }

        setting = Settings(json = settings_json)
        setting.id = 1

        return setting
