import pytest

from lib.database import Database
from models.data.http_flow_search import HttpFlowSearch
from models.data.settings import Settings
# from models.data.editor_request import EditorRequest
from models.data.editor_item import EditorItem
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from models.data.variable import Variable

@pytest.fixture(scope="session")
def database():
    database = Database('tmp.db')
    print("=============> DB Setup")
    yield
    print("=============> DB Teardown")
    database.close()

@pytest.fixture(scope="function")
def cleanup_database():
    # EditorItem.truncate()
    # HttpFlow.truncate()
    # HttpRequest.truncate()
    # HttpResponse.truncate()
    # HttpFlowSearch.truncate()
    # Variable.truncate()
    # Settings.truncate()

    yield

    # Database.get_instance().close()
