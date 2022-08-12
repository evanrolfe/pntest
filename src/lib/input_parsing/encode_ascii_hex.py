import codecs
from lib.input_parsing.encoder import Encoder

class EncodeAsciiHex(Encoder):
    def __init__(self):
        self.name = "ASCII Hex Encode"
        self.decode_name = "ASCII Hex Decode"
        self.key = "ascii"
        self.type = self.TYPE_ENCODER

    def encode(self, value: str) -> str:
        return codecs.encode(value.encode("utf-8"), "hex").decode('utf-8')

    def decode(self, value: str) -> str:
        return codecs.decode(value.encode("utf-8"), "hex").decode('utf-8')

