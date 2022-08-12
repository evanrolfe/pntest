import json
from lib.input_parsing.encoder import Encoder

class EncodeJs(Encoder):
    def __init__(self):
        self.name = "Javascript Encode"
        self.key = "js"
        self.type = self.TYPE_ENCODER

    def encode(self, value: str) -> str:
        return json.dumps(value).strip('"')

    def decode(self, value: str) -> str:
        return value.encode().decode("unicode-escape")
