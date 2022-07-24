import codecs
from lib.input_parsing.encoder import Encoder

class EncodeAsciiHex(Encoder):
    def __init__(self):
        self.name = "ASCII Hex Encode"
        self.key = "ascii"

    def encode(self, value: str) -> str:
        return codecs.encode(value.encode("utf-8"), "hex").decode('utf-8')

    def decode(self, str: str) -> str:
        return str
