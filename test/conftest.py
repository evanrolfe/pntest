import pytest

from lib.database import Database

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
