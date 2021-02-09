from lib.database import Database
from models.data.client import Client

database = Database('test/tmp.db')
database.delete_existing_db()
database.load_or_create()

def func(x):
    return x + 1

def describe_client():
    def test_answer():
        client = Client()
        client.title = 'THis is from the test!'
        client.type = 'chrome'
        client.save()

        assert func(3) == 4
