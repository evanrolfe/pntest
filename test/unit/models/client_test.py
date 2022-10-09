from asyncio import create_task
from venv import create
from lib.database import Database
from models.client import Client

class TestClient:
    def test_instantiating_a_client(self):
        client = Client(title="test client!", type="browser", proxy_port=8080)

        assert client.title == "test client!"
        assert client.type == "browser"
        assert client.browser_port is None

        client.title = "I've been changed!"
        print(client.__dict__)
