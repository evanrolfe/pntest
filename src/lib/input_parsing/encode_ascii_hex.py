import codecs

class EncodeAsciiHex:
    name = "ASCII Hex Encode"
    key = "ascii"

    @staticmethod
    def encode(value: str) -> str:
        return codecs.encode(value.encode("utf-8"), "hex").decode('utf-8')

    @staticmethod
    def decode(str):
        return str
