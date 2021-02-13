from orator.orm import Factory
from models.data.editor_request import EditorRequest

factory = Factory()

@factory.define(EditorRequest)
def editor_request_factory(faker):
    return {
        'method': 'GET',
        'url': 'http://example.com',
        'request_headers': '{"host": "example.com", "content-length": 123, "accept": "*/*", "accept-encoding": "gzip, deflate", "connection": "keep-alive"}', # noqa
        'request_payload': None
    }


class TestEditorRequest:
    def test_get_request_headers(self, database):
        editor_request = factory(EditorRequest).make()
        headers = editor_request.get_request_headers()

        assert headers['host'] == 'example.com'
        assert headers['accept'] == '*/*'
        assert headers['accept-encoding'] == 'gzip, deflate'
        assert headers['connection'] == 'keep-alive'

    def test_overwrite_calculated_headers(self, database):
        editor_request = factory(EditorRequest).make()
        editor_request.overwrite_calculated_headers()
        headers = editor_request.get_request_headers()

        assert headers['host'] == '<calculated when request is sent>'
        assert headers['content-length'] == '<calculated when request is sent>'

    # TODO: I think we can delete the editor_request.parent_id and its related methods as that is
    # handled by the EditorItem model
    def test_children(self, database, cleanup_database):
        editor_request1 = factory(EditorRequest).create()
        editor_request2 = factory(EditorRequest).make()
        editor_request3 = factory(EditorRequest).make()

        editor_request2.parent_id = editor_request1.id
        editor_request2.save()
        editor_request3.parent_id = editor_request1.id
        editor_request3.save()

        children = editor_request1.children()
        children_ids = [c.id for c in list(children)]

        assert len(children) == 2
        assert editor_request2.id in children_ids
        assert editor_request3.id in children_ids

    def test_delete_resursive(self, database, cleanup_database):
        editor_request1 = factory(EditorRequest).create()
        editor_request2 = factory(EditorRequest).make()
        editor_request3 = factory(EditorRequest).make()

        editor_request2.parent_id = editor_request1.id
        editor_request2.save()
        editor_request3.parent_id = editor_request2.id
        editor_request3.save()

        editor_request1.delete_resursive()

        editor_requests = EditorRequest.all()
        assert len(editor_requests) == 0
