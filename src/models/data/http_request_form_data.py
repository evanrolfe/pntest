from __future__ import annotations
import json
from lib.types import Headers

class HttpRequestFormData:
    method: str
    url: str
    headers: Headers
    body: str

    def __init__(self, method: str, url: str, headers: Headers, body: str):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def serialize(self) -> str:
        data = {
            'method': self.method,
            'url': self.url,
            'headers': self.headers,
            'body': self.body,
        }
        return json.dumps(data)
