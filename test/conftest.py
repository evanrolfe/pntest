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
    print("\n[Test] DB Setup")
    yield
    print("[Test] DB Teardown")
    database.close()

@pytest.fixture(scope="function")
def cleanup_database():
    conn = Database.get_instance().conn

    conn.executescript("""
        DELETE FROM 'editor_items';
        DELETE FROM 'clients';
        DELETE FROM 'settings';
        DELETE FROM 'http_requests';
        DELETE FROM 'http_responses';
        DELETE FROM 'http_flows';
        DELETE FROM 'variables';
        DELETE FROM 'websocket_messages';
    """)

    yield

    # Database.get_instance().close()
