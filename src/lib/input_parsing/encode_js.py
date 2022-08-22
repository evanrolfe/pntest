import json
from lib.input_parsing.transformer import Transformer

class EncodeJs(Transformer):
    def __init__(self):
        self.name = "Javascript Encode"
        self.key = "js"
        self.type = self.TYPE_ENCODER

    def encode(self, value: str) -> str:
        return json.dumps(value).strip('"')

    def decode(self, value: str) -> str:
        return value.encode().decode("unicode-escape")
