from orator.orm import Factory
from models.data.editor_item import EditorItem
from models.data.editor_request import EditorRequest
from models.data.network_request import NetworkRequest

factory = Factory()

# TODO: Move these factories into their own files
@factory.define_as(EditorItem, 'request')
def editor_item_factory_request(faker):
    return {
        'name': 'Login request',
        'item_type': 'request',
        'item_id': 1
    }

@factory.define_as(EditorItem, 'dir')
def editor_item_factory_dir(faker):
    return {
        'name': 'My requests',
        'item_type': 'dir'
    }

@factory.define(NetworkRequest)
def network_request_factory(faker):
    return {
        'client_id': 1,
        'method': 'GET',
        'host': 'example.com',
        'path': '/',
        'encrypted': 0,
        'http_version': '1.1',
        'request_headers': '{"host": "example.com", "content-length": 123, "accept": "*/*", "accept-encoding": "gzip, deflate", "connection": "keep-alive"}', # noqa
        'request_payload': None,
        'request_type': 'http',
    }

class TestEditorItem:
    def test_delete_everything(self, database, cleanup_database):
        item_dir = factory(EditorItem, 'dir').create()
        factory(EditorItem, 'request').create(parent_id=item_dir.id)
        factory(EditorItem, 'request').create(parent_id=item_dir.id)

        item_dir.delete_everything()

        assert EditorItem.count() == 0
        assert EditorRequest.count() == 0

    def test_save(self, database, cleanup_database):
        item = factory(EditorItem, 'request').make(item_id=None)
        item.save()
        request = EditorRequest.where('id', '=', item.id).first()

        assert request is not None

    def test_create_from_network_request(self, database, cleanup_database):
        network_request = factory(NetworkRequest).create()

        item = EditorItem.create_from_network_request(network_request)
        editor_request = item.item()

        assert item.item_type == 'request'
        assert item.item_id is not None

        assert editor_request.method == 'GET'
        assert editor_request.url == 'http://example.com/'
        assert editor_request.request_headers == '{"host": "<calculated when request is sent>", "content-length": "<calculated when request is sent>", "accept": "*/*", "accept-encoding": "gzip, deflate", "connection": "keep-alive"}' # noqa
