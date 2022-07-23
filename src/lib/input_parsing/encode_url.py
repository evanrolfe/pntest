import urllib.parse

class EncodeUrl:
    name = "URL Encode"
    key = "url"

    @staticmethod
    def encode(value: str) -> str:
        return urllib.parse.quote_plus(value)

    @staticmethod
    def decode(str):
        return str
