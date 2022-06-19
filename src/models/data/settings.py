from __future__ import annotations
import json
from typing import Optional
from lib.database_cache import DatabaseCache
from models.data.orator_model import OratorModel
from proxy.common_types import SettingsJson, CaptureFilterSettings, DisplayFilterSettings

class Settings(OratorModel):
    __table__ = 'settings'

    id: int
    json: str
    created_at: int
    updated_at: Optional[int]
    parsedObj: SettingsJson

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)

    @classmethod
    def create_defaults(cls):
        setting = Settings()
        setting.id = 1

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
        settings_json: SettingsJson = {
            'capture_filters': capture_filters,
            'display_filters': display_filters,
        }
        setting.json = json.dumps(settings_json)
        setting.save()

    @classmethod
    def get(cls) -> Settings:
        settings = cls.find(1)
        cache = DatabaseCache.get_instance()
        cache.cache_record('settings', settings.id, settings)

        return settings

    @classmethod
    def get_from_cache(cls) -> Settings:
        cache = DatabaseCache.get_instance()
        cached_settings = cache.get_record('settings', 1)

        if cached_settings:
            return cached_settings

        return cls.find(1)

    def parsed(self) -> SettingsJson:
        parsedObj = getattr(self, 'parsedObj', None)

        if parsedObj is None:
            self.parsedObj = json.loads(self.json)

        return self.parsedObj

    def save(self, *args, **kwargs):
        self.json = json.dumps(self.parsed())

        # Dont try to save the parsedObj to the db
        delattr(self, 'parsedObj')

        return super(Settings, self).save(*args, **kwargs)
