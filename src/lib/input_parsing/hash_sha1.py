import hashlib
from lib.input_parsing.transformer import Transformer

class HashSHA1(Transformer):
    def __init__(self):
        self.name = "SHA1"
        self.decode_name = ""
        self.key = "sha1"
        self.type = self.TYPE_HASHER

    def encode(self, value: str) -> str:
        return hashlib.sha1(value.encode("utf-8")).hexdigest()

    def decode(self, value: str) -> str:
        raise Exception("cannot decode a hash")
