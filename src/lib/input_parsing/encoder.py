from abc import abstractmethod

# Abstract class for all encoders to inherit from
class Encoder:
    name: str
    decode_name: str
    key: str

    def __init__(self) -> None:
        pass

    @abstractmethod
    def encode(self, value: str) -> str:
        pass

    @abstractmethod
    def decode(self, value: str) -> str:
        pass
