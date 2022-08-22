import html
from lib.input_parsing.transformer import Transformer

class EncodeHTML(Transformer):
    def __init__(self):
        self.name = "HTML Encode"
        self.key = "html"
        self.type = self.TYPE_ENCODER

    def encode(self, value: str) -> str:
        return html.escape(value)

    def decode(self, value: str) -> str:
        return html.unescape(value)
