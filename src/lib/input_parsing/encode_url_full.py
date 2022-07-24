import urllib.parse
from lib.input_parsing.encoder import Encoder

class EncodeUrlFull(Encoder):
    def __init__(self):
        self.name = "URL Encode Full"
        self.key = "urlfull"

    def encode(self, value: str) -> str:
        return urllib.parse.quote(value)

    def decode(self, str):
        return str
