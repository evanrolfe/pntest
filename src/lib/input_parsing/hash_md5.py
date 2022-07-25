import hashlib
from lib.input_parsing.encoder import Encoder

class HashMD5(Encoder):
    def __init__(self):
        self.name = "MD5"
        self.decode_name = ""
        self.key = "md5"

    def encode(self, value: str) -> str:
        return hashlib.md5(value.encode("utf-8")).hexdigest()

    def decode(self, value: str) -> str:
        raise Exception("cannot decode a hash")