import pytest

from lib.database import Database
# from models.data.editor_request import EditorRequest
from models.data.editor_item import EditorItem

@pytest.fixture(scope="session")
def database():
    database = Database('test/tmp.db')
    database.delete_existing_db()
    database.load_or_create()

@pytest.fixture(scope="function")
def cleanup_database():
    # EditorRequest.truncate()
    EditorItem.truncate()

    yield
