from asyncio import create_task
import sqlite3
from venv import create
from lib.database import Database
from models.client import Client
from models.data import http_flow
from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from models.websocket_message import WebsocketMessage
from repos.http_request_repo import HttpRequestRepo
from repos.client_repo import ClientRepo
from lib.database import Database
from lib.database_schema import SCHEMA_SQL, NUM_TABLES

class TestHttpRequestRepo:
    def test_saving_a_request(self, database, cleanup_database):
        http_request_repo = HttpRequestRepo()

        request = HttpRequest(
            http_version="HTTP/2.0",
            headers={"hello": "world"},
            host="synack.com",
            port=80,
            method="GET",
            scheme="http",
            path="/",
            form_data={
                "method": "GET",
                "url": "http://www.synack.com/login.php",
                "headers": {"Content-Length": "<calculated when request is sent>", "Host": "<calculated when request is sent>", "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "User-Agent": "pntest/0.1"},
                "content": '{ "username": "${payload:usernames}", "password": "${payload:passwords}" }',
                "fuzz_data": None,
            },
            created_at=1
        )
        http_request_repo.save(request)

        assert request.id > 0

        request2 = http_request_repo.find(request.id)
        assert request2 is not None
        assert request2.id > 0
        assert request.host == "synack.com"
        assert request.form_data["url"] == "http://www.synack.com/login.php"
        assert request.headers["hello"] == "world"
