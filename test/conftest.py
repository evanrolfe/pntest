import pytest

from lib.database import Database
from models.data.http_flow_search import HttpFlowSearch
from models.data.settings import Settings
# from models.data.editor_request import EditorRequest
from models.data.editor_item import EditorItem
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
@pytest.fixture(scope="session")
def database():
    database = Database('test/tmp.db')
    database.delete_existing_db()
    database.load_or_create()

@pytest.fixture(scope="function")
def cleanup_database():
    EditorItem.truncate()
    Settings.truncate()
    HttpFlow.truncate()
    HttpRequest.truncate()
    HttpResponse.truncate()

    yield
