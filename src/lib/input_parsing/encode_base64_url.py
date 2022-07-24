import base64
from lib.input_parsing.encoder import Encoder

class EncodeBase64Url(Encoder):
    def __init__(self):
        self.name = "Base64 URL"
        self.key = "b64url"

    def encode(self, value: str) -> str:
        return base64.urlsafe_b64encode(bytes(value, 'utf-8')).decode('utf-8')

    def decode(self, str):
        return str
