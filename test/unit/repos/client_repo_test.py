from asyncio import create_task
import sqlite3
from venv import create
from lib.database import Database
from models.client import Client
from repos.client_repo import ClientRepo
from lib.database import Database
from lib.database_schema import SCHEMA_SQL, NUM_TABLES

class TestClientRepo:
    def test_saving_and_retrieving_a_client(self, database):
        conn = Database.get_instance().conn
        client_repo = ClientRepo()

        client = Client(title="test client!", type="browser", proxy_port=8080)

        client_repo.save(client)

        assert client.id is not None
        assert client.title == "test client!"
        assert client.type == "browser"
        assert client.proxy_port == 8080
        assert client.open == False
        assert client.created_at is not None
        print(client)

        client2 = client_repo.find(client.id)
        assert client2 is not None
        assert client2.id is not None

    def test_finding_a_client_that_doesnt_exist(self, database, cleanup_database):
        client_repo = ClientRepo()
        result = client_repo.find(0)

        print("========> ", result)
