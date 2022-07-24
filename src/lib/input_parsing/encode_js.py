from lib.input_parsing.encoder import Encoder

class EncodeJs(Encoder):
    def __init__(self):
        self.name = "Javascript Encode"
        self.key = "js"

    def encode(self, value: str) -> str:
        # TODO:
        return value

    def decode(self, str):
        return str
