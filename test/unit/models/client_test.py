from models.data.client import Client

def func(x):
    return x + 1

class TestClient:
    def test_open_text(self, database):
        client = Client()
        client.title = 'Browser #1'
        client.type = 'chrome'
        client.open = True
        client.save()

        assert client.open_text() == 'Open'
