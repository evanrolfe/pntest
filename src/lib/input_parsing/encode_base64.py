import base64
from lib.input_parsing.encoder import Encoder

class EncodeBase64(Encoder):
    def __init__(self):
        self.name = "Base64"
        self.decode_name = "Base 64"
        self.key = "b64"
        self.type = self.TYPE_ENCODER

    def encode(self, value: str) -> str:
        return base64.b64encode(bytes(value, 'utf-8')).decode('utf-8')

    def decode(self, value: str) -> str:
        return base64.b64decode(bytes(value, 'utf-8')).decode('utf-8')
