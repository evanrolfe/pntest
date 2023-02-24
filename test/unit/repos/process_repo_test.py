from entities.client import Client
from repos.client_repo import ClientRepo
from repos.process_repo import ProcessRepo

class TestProcessRepo:
    def test_launch_proxy(self, database, cleanup_database):
        ProcessRepo()
        repo = ProcessRepo.get_instance()
        assert repo.procs == []

        client = Client(title="test client!", type="anything", proxy_port=8080)
        ClientRepo().save(client)

        # settings = ProjectSettingsRepo().get()

        # repo.launch_proxy(client, settings)
        # assert len(repo.procs) == 1
