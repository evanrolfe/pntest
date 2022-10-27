from models.data.settings import Settings

class TestSettings:
    # def test_create_defaults(self, database, cleanup_database):
    #     Settings.create_defaults()
    #     settings = Settings.get()

    #     assert settings.id == 1

    #     settings.parsed()["capture_filters"]["ext_list"] = ["hello", "world"]
    #     settings.save()

    #     assert settings.json == '{"capture_filters": {"host_list": [], "host_setting": "", "path_list": [], "path_setting": "", "ext_list": ["hello", "world"], "ext_setting": ""}}'

    def test_get_from_cache(self, database, cleanup_database):
        Settings.create_defaults()
        settings = Settings.get()
        assert settings.id == 1

        settings = Settings.get_from_cache()
        assert settings.id == 1
