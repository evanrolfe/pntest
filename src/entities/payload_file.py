from __future__ import annotations
from typing import TypedDict

class PayloadFileSerialised(TypedDict):
    key: str
    file_path: str
    num_items: int
    description: str

class PayloadFile:
    key: str
    file_path: str
    num_items: int
    description: str
    values: list[str]

    def __init__(self, file_path, key):
        self.file_path = file_path
        self.key = key
        self.num_items = 0
        self.description = ''

    @classmethod
    def from_serialised(cls, serialised_payload: PayloadFileSerialised) -> PayloadFile:
        payload_file = PayloadFile(serialised_payload['file_path'], serialised_payload['key'])
        payload_file.num_items = serialised_payload['num_items']
        payload_file.description = serialised_payload['description']

        return payload_file

    def verify_file(self) -> None:
        with open(self.file_path) as file:
            self.num_items = sum(1 for _ in file)

    def load_values(self):
        with open(self.file_path, 'r') as file:
            self.values = file.read().split('\n')

    def serialise(self) -> PayloadFileSerialised:
        return {
            'file_path': self.file_path,
            'key': self.key,
            'num_items': self.num_items,
            'description': self.description,
        }
