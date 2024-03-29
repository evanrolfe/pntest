from entities.client import Client
from repos.client_repo import ClientRepo

class TestClientRepo:
    def test_saving_and_retrieving_a_client(self, database, cleanup_database):
        client_repo = ClientRepo()
        client = Client(title="test client!", type="chrome", proxy_port=8080)
        client_repo.save(client)

        assert client.id is not None
        assert "test client!" in client.title
        assert client.type == "chrome"
        assert client.proxy_port == 8080
        assert client.open == False
        assert client.created_at is not None

        client2 = client_repo.find(client.id)
        assert client2 is not None
        assert client2.id == client.id
        assert client2.created_at == client.created_at

    def test_finding_a_client_that_doesnt_exist(self, database, cleanup_database):
        client_repo = ClientRepo()
        result = client_repo.find(0)

        assert result is None

    def test_get_next_port_available(self, database, cleanup_database):
        client_repo = ClientRepo()
        client = Client(title="test client!", type="chrome", proxy_port=8080)
        client_repo.save(client)

        result = client_repo.get_next_port_available()
        assert result == 8081
