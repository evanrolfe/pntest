from lib.input_parsing.transformer import Transformer

class TransformPayload(Transformer):
    payload_values: dict[str,str]

    def __init__(self, payload_values: dict[str,str]):
        self.name = "Payload"
        self.decode_name = ""
        self.key = "payload"
        self.payload_values = payload_values
        self.type = self.TYPE_PAYLOAD

    def encode(self, key: str) -> str:
        return self.payload_values.get(key) or ""

    def decode(self, value: str) -> str:
        raise Exception("cannot decode a var")
