import urllib.parse
from lib.input_parsing.transformer import Transformer

class EncodeUrl(Transformer):
    def __init__(self):
        self.name = "URL Encode"
        self.decode_name = "URL Decode"
        self.key = "url"
        self.type = self.TYPE_ENCODER

    def encode(self, value: str) -> str:
        return urllib.parse.quote_plus(value)

    def decode(self, value: str) -> str:
        return urllib.parse.unquote_plus(value)
