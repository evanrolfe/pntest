from asyncio import create_task
from venv import create
from lib.database import Database
from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from repo.http_request_repo import HttpRequestRepo

class TestHttpRequestRepo:
    def test_saving_a_request(self, database, cleanup_database):
        session_factory = Database.get_instance().get_session_factory()
        http_request_repo = HttpRequestRepo(session_factory)
        request = HttpRequest(
            http_version="HTTP/2.0",
            headers="{}",
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/",
            form_data="{}",
            created_at=1
        )
        http_request_repo.save(request)

        request2 = http_request_repo.find(request.id)
        assert request2 is not None

    def test_finding_a_request_that_doesnt_exist(self, database, cleanup_database):
        session_factory = Database.get_instance().get_session_factory()
        http_request_repo = HttpRequestRepo(session_factory)
        request = http_request_repo.find(0)

        assert request is None
