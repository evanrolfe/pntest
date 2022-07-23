import base64

class EncodeBase64:
    name = "Base64"
    key = "b64"

    @staticmethod
    def encode(value: str) -> str:
        return base64.b64encode(bytes(value, 'utf-8')).decode('utf-8')

    @staticmethod
    def decode(str):
        return str
