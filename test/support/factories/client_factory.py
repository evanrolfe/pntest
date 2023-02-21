import factory

from entities.client import Client

class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    title="test client!"
    type="browser"
    proxy_port=8080
