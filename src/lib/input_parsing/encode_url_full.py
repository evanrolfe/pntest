import urllib.parse
from lib.input_parsing.transformer import Transformer

class EncodeUrlFull(Transformer):
    def __init__(self):
        self.name = "URL Encode Full"
        self.decode_name = "URL Decode Full"
        self.key = "urlfull"
        self.type = self.TYPE_ENCODER

    def encode(self, value: str) -> str:
        return urllib.parse.quote(value)

    def decode(self, value: str) -> str:
        return urllib.parse.unquote(value)

