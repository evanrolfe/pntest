import factory

from entities.editor_item import EditorItem

class EditorItemFactory(factory.Factory):
    class Meta:
        model = EditorItem

    parent_id = None
    name = "A saved request"
    item_type = EditorItem.TYPE_HTTP_FLOW
    item_id = None
