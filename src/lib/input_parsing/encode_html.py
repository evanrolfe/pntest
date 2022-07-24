from lib.input_parsing.encoder import Encoder

class EncodeHTML(Encoder):
    def __init__(self):
        self.name = "HTML Encode"
        self.key = "html"

    def encode(self, value: str) -> str:
        # TODO:
        return value

    def decode(self, str):
        return str
