from entities.http_request import HttpRequest
from repos.http_request_repo import HttpRequestRepo

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
        )
        http_request_repo.save(request)

        assert request.id > 0

        request2 = http_request_repo.find(request.id)
        assert request2 is not None
        assert request2.id > 0
        assert request2.created_at > 0
        assert request.host == "synack.com"
        assert request.form_data["url"] == "http://www.synack.com/login.php"
        assert request.headers["hello"] == "world"
