import html
from lib.input_parsing.encoder import Encoder

class EncodeHTML(Encoder):
    def __init__(self):
        self.name = "HTML Encode"
        self.key = "html"

    def encode(self, value: str) -> str:
        return html.escape(value)

    def decode(self, value: str) -> str:
        return html.unescape(value)
