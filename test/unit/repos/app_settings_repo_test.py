from repos.app_settings_repo import AppSettingsRepo

class TestSettingsRepo:
    SETTINGS_APP_NAME = "PnTest_TEST"

    def test_getting_and_saving_settings(self, database, cleanup_database):
        repo = AppSettingsRepo(self.SETTINGS_APP_NAME)
        settings = repo.get()

        settings['network_layout'] = 'helloworld'
        settings['browser_commands']['chrome'] = 'google-chrome'
        repo.save(settings)

        settings2 = repo.get()
        assert settings2['network_layout'] == 'helloworld'
        assert settings2['browser_commands']['chrome'] == 'google-chrome'

        repo.reset()

