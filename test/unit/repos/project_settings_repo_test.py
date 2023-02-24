from repos.project_settings_repo import ProjectSettingsRepo

class TestSettingsRepo:
    def test_get(self, database, cleanup_database):
        repo = ProjectSettingsRepo()
        settings = repo.get()

        assert settings['capture_filters']['host_list'] == []

    def test_save_insert(self, database, cleanup_database):
        repo = ProjectSettingsRepo()
        settings = repo.get()

        settings['capture_filters']['host_list'] = ['pntest.io']

        repo.save(settings)

        settings2 = repo.get()
        assert settings2['capture_filters']['host_list'] == ['pntest.io']

    def test_save_update(self, database, cleanup_database):
        repo = ProjectSettingsRepo()
        settings = repo.get()

        settings['capture_filters']['host_list'] = ['pntest.io']
        repo.save(settings)
        settings2 = repo.get()
        assert settings2['capture_filters']['host_list'] == ['pntest.io']

        settings2['capture_filters']['host_list'] = ['pntest.io', 'pntest.com']
        repo.save(settings2)
        settings3 = repo.get()
        assert settings3['capture_filters']['host_list'] == ['pntest.io', 'pntest.com']
