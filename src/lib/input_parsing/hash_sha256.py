import hashlib
from lib.input_parsing.encoder import Encoder

class HashSHA256(Encoder):
    def __init__(self):
        self.name = "SHA256"
        self.decode_name = ""
        self.key = "sha256"

    def encode(self, value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def decode(self, value: str) -> str:
        raise Exception("cannot decode a hash")
