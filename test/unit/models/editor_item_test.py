from models.data.editor_item import EditorItem
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from support.factories import factory

class TestEditorItem:
    def test_delete_everything(self, database, cleanup_database):
        item_dir = factory(EditorItem, 'dir').create()
        item_child1 = factory(EditorItem, 'request').create(parent_id=item_dir.id)
        factory(EditorItem, 'request').create(parent_id=item_dir.id)
        factory(EditorItem, 'request').create(parent_id=item_child1.id)

        item_dir.delete_everything()

        assert EditorItem.count() == 0

    def test_save(self, database, cleanup_database):
        item = factory(EditorItem, 'request').make(item_id=None)
        item.save()

        flow = HttpFlow.where('id', '=', item.id).first()
        assert flow is not None

    def test_create_for_http_flow(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'proxy').make()
        http_request.save()

        http_flow = factory(HttpFlow, 'proxy').make(request_id=http_request.id)
        http_flow.save()

        item = EditorItem.create_for_http_flow(http_flow)

        assert item.id is not None
        assert item.item_type == EditorItem.TYPE_HTTP_FLOW
        assert item.item_id == http_flow.id

    def test_duplicate(self, database, cleanup_database):
        http_request = factory(HttpRequest, 'editor').make()
        http_request.save()

        http_flow = factory(HttpFlow, 'editor').make(request_id=http_request.id)
        http_flow.save()

        item = EditorItem.create_for_http_flow(http_flow)
        new_item = item.duplicate()

        assert new_item.name == item.name
        assert new_item.item_type == item.item_type
        assert new_item.item_id != http_flow.id
