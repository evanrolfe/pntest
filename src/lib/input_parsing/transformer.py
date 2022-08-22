from abc import abstractmethod

# TODO: Rename this to "Transformer"
# Abstract class for all encoders to inherit from
class Transformer:
    TYPE_ENCODER = "encoder"
    TYPE_DECODER = "decoder"
    TYPE_HASHER = "hasher"
    TYPE_VAR = "var"
    TYPE_PAYLOAD = "payload"

    name: str
    decode_name: str
    key: str
    type: str

    def __init__(self) -> None:
        pass

    @abstractmethod
    def encode(self, value: str) -> str:
        pass

    @abstractmethod
    def decode(self, value: str) -> str:
        pass
