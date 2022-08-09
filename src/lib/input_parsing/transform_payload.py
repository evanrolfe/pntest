import hashlib
from lib.input_parsing.encoder import Encoder
from models.data.variable import Variable

class TransformPayload(Encoder):
    payload_values: dict[str,str]

    def __init__(self, payload_values: dict[str,str]):
        self.name = "Payload"
        self.decode_name = ""
        self.key = "payload"
        self.payload_values = payload_values

    def encode(self, key: str) -> str:
        return self.payload_values.get(key) or ""

    def decode(self, value: str) -> str:
        raise Exception("cannot decode a var")
