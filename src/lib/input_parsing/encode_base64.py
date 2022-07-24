import base64
from lib.input_parsing.encoder import Encoder

class EncodeBase64(Encoder):
    def __init__(self):
        self.name = "Base64"
        self.key = "b64"

    def encode(self, value: str) -> str:
        return base64.b64encode(bytes(value, 'utf-8')).decode('utf-8')

    def decode(self, str):
        return str
