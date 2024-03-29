from entities.editor_item import EditorItem
from repos.editor_item_repo import EditorItemRepo
from services.editor_item_service import EditorItemService
from support.factories.editor_item_factory import EditorItemFactory

def create_editor_item_with_many_children() -> list[EditorItem]:
    editor_items = []

    repo = EditorItemRepo()
    parent_item: EditorItem = EditorItemFactory.build(name="parent")
    parent_item.build_blank_http_flow()
    repo.save(parent_item)
    editor_items.append(parent_item)

    parent_item2: EditorItem = EditorItemFactory.build(name="parent2")
    parent_item2.build_blank_http_flow()
    repo.save(parent_item2)
    editor_items.append(parent_item2)

    child_item1: EditorItem = EditorItemFactory.build(name="child1", parent_id=parent_item.id)
    child_item1.build_blank_http_flow()
    repo.save(child_item1)
    editor_items.append(child_item1)

    child_item2: EditorItem = EditorItemFactory.build(name="child2", parent_id=parent_item.id)
    child_item2.build_blank_http_flow()
    repo.save(child_item2)
    editor_items.append(child_item2)

    grand_child_item1: EditorItem = EditorItemFactory.build(name="grandchild1", parent_id=child_item2.id)
    grand_child_item1.build_blank_http_flow()
    repo.save(grand_child_item1)
    editor_items.append(grand_child_item1)

    grand_child_item2: EditorItem = EditorItemFactory.build(name="grandchild2", parent_id=child_item2.id)
    grand_child_item2.build_blank_http_flow()
    repo.save(grand_child_item2)
    editor_items.append(grand_child_item2)

    great_grand_child_item2: EditorItem = EditorItemFactory.build(name="greatgrandchild2", parent_id=grand_child_item1.id)
    great_grand_child_item2.build_blank_http_flow()
    repo.save(great_grand_child_item2)
    editor_items.append(great_grand_child_item2)

    return editor_items

class TestEditorItemService:
    def test_saving_and_retrieving_an_item(self, database, cleanup_database):
        editor_item: EditorItem = EditorItemFactory.build()
        editor_item.build_blank_http_flow()
        EditorItemService().save(editor_item)

        assert editor_item.id is not None
        assert editor_item.created_at is not None
        assert editor_item.item is not None
        assert editor_item.item.id > 0

        editor_item2 = EditorItemService().find(editor_item.id)
        assert editor_item2 is not None
        assert editor_item2.id == editor_item.id
        assert editor_item2.created_at == editor_item.created_at

        assert editor_item2.item is not None
        assert editor_item2.item.id == editor_item.item.id

    def test_finding_a_client_that_doesnt_exist(self, database, cleanup_database):
        result = EditorItemService().find(0)
        assert result is None

    def test_saving_and_retrieving_an_item_with_children(self, database, cleanup_database):
        create_editor_item_with_many_children()

        # Find all items with children
        editor_items = EditorItemService().find_all_with_children()
        assert len(editor_items) == 7

        root_items = [item for item in editor_items if item.parent_id is None]
        assert len(root_items) == 2

        # TODO: Actually test the result is correct here

    def test_deleting_an_item_and_all_its_offspring(self, database, cleanup_database):
        create_editor_item_with_many_children()

        # Delete one of the root items
        editor_items = EditorItemService().find_all_with_children()
        assert editor_items[0] is not None
        EditorItemService().delete(editor_items[0])

        # Find all items with children
        editor_items = EditorItemService().find_all_with_children()
        assert len(editor_items) == 4

        root_items = [item for item in editor_items if item.parent_id is None]
        assert len(root_items) == 1
