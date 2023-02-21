import factory

from entities.http_response import HttpResponse

class HttpResponseFactory(factory.Factory):
    class Meta:
        model = HttpResponse

    http_version="HTTP/2.0"
    headers={"Content-Type": "text/html"}
    content=str.encode("<html>hello world</html>")
    timestamp_start=1.0
    timestamp_end=2.0
    status_code=200
    reason=None
