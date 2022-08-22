import base64
from lib.input_parsing.transformer import Transformer

class EncodeBase64Url(Transformer):
    def __init__(self):
        self.name = "Base64 URL"
        self.decode_name = "Base64 URL"
        self.key = "b64url"
        self.type = self.TYPE_ENCODER

    def encode(self, value: str) -> str:
        return base64.urlsafe_b64encode(bytes(value, 'utf-8')).decode('utf-8')

    def decode(self, value: str) -> str:
        return base64.urlsafe_b64decode(bytes(value, 'utf-8')).decode('utf-8')

