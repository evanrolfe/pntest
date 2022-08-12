import urllib.parse
from lib.input_parsing.encoder import Encoder

class EncodeUrl(Encoder):
    def __init__(self):
        self.name = "URL Encode"
        self.decode_name = "URL Decode"
        self.key = "url"
        self.type = self.TYPE_ENCODER

    def encode(self, value: str) -> str:
        return urllib.parse.quote_plus(value)

    def decode(self, value: str) -> str:
        return urllib.parse.unquote_plus(value)
