import hashlib
from lib.input_parsing.transformer import Transformer

class HashMD5(Transformer):
    def __init__(self):
        self.name = "MD5"
        self.decode_name = ""
        self.key = "md5"
        self.type = self.TYPE_HASHER

    def encode(self, value: str) -> str:
        return hashlib.md5(value.encode("utf-8")).hexdigest()

    def decode(self, value: str) -> str:
        raise Exception("cannot decode a hash")
