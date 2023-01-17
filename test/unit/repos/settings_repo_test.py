import sqlite3
from models.settings import Settings
from repos.settings_repo import SettingsRepo
from lib.database import Database

class TestSettingsRepo:
    def test_inserting_and_fetching_settings(self, database, cleanup_database):
        repo = SettingsRepo()
        settings = Settings.build_default()
        repo.insert(settings)

        assert settings.id is not None
        assert settings.json['capture_filters']['host_list'] == []
        assert settings.created_at is not None

        settings2 = repo.get_settings()
        assert settings2 is not None
        assert settings2.id is not None
        assert settings2.json['capture_filters']['host_list'] == []
        assert settings2.created_at is not None

    def test_get_settings(self, database, cleanup_database):
        repo = SettingsRepo()
        settings = repo.get_settings()

        assert settings.id == 1
        assert settings.json['capture_filters']['host_list'] == []
        assert settings.created_at is not None

        settings2 = repo.get_settings()
        assert settings2.id == 1
        assert settings2.json['capture_filters']['host_list'] == []
        assert settings2.created_at is not None
