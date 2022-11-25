import hashlib
from lib.input_parsing.transformer import Transformer
from repos.variable_repo import VariableRepo

class TransformVar(Transformer):
    def __init__(self):
        self.name = "Variable"
        self.decode_name = ""
        self.key = "var"
        self.type = self.TYPE_VAR

    def encode(self, key: str) -> str:
        var = VariableRepo().find_by_key(key)
        if not var:
            return ''

        return var.value

    def decode(self, value: str) -> str:
        raise Exception("cannot decode a var")
