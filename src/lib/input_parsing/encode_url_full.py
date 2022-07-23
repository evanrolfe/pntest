import urllib.parse

class EncodeUrlFull:
    name = "URL Encode Full"
    key = "urlfull"

    @staticmethod
    def encode(value: str) -> str:
        return urllib.parse.quote(value)

    @staticmethod
    def decode(str):
        return str
