import hashlib
from lib.input_parsing.transformer import Transformer

class HashSHA256(Transformer):
    def __init__(self):
        self.name = "SHA256"
        self.decode_name = ""
        self.key = "sha256"
        self.type = self.TYPE_HASHER

    def encode(self, value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def decode(self, value: str) -> str:
        raise Exception("cannot decode a hash")
