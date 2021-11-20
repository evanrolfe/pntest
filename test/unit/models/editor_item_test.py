from models.data.editor_item import EditorItem
from support.factories import factory

class TestEditorItem:
    def test_something(self, database, cleanup_database):
        assert 2+2, 4
    # def test_delete_everything(self, database, cleanup_database):
    #     item_dir = factory(EditorItem, 'dir').create()
    #     factory(EditorItem, 'request').create(parent_id=item_dir.id)
    #     factory(EditorItem, 'request').create(parent_id=item_dir.id)

    #     item_dir.delete_everything()

    #     assert EditorItem.count() == 0
    #     assert EditorRequest.count() == 0

    # def test_save(self, database, cleanup_database):
    #     item = factory(EditorItem, 'request').make(item_id=None)
    #     item.save()
    #     request = EditorRequest.where('id', '=', item.id).first()

    #     assert request is not None

    # def test_create_from_network_request(self, database, cleanup_database):
    #     network_request = factory(NetworkRequest).create()

    #     item = EditorItem.create_from_network_request(network_request)
    #     editor_request = item.item()

    #     assert item.item_type == 'request'
    #     assert item.item_id is not None

    #     assert editor_request.method == 'GET'
    #     assert editor_request.url == 'http://example.com/'
    #     assert editor_request.request_headers == '{"host": "<calculated when request is sent>", "content-length": "<calculated when request is sent>", "accept": "*/*", "accept-encoding": "gzip, deflate", "connection": "keep-alive"}' # noqa
