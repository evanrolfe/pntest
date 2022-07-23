import base64

class EncodeBase64Url:
    name = "Base64 URL"
    key = "b64url"

    @staticmethod
    def encode(value: str) -> str:
        return base64.urlsafe_b64encode(bytes(value, 'utf-8')).decode('utf-8')

    @staticmethod
    def decode(str):
        return str
