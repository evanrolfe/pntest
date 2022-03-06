import re
from copy import deepcopy
from lib.types import Headers
from models.data.variable import Variable

def parse_headers(headers: Headers) -> Headers:
    new_headers = deepcopy(headers)

    for key, value in new_headers.items():
        new_headers[key] = parse_value(value)

    return new_headers

def parse_value(value: str) -> str:
    for match in re.finditer(r'\${var:(\w+)\}', value):
        key = match[1]
        var = Variable.find_by_key(key)

        if var:
            new_value = var.value
        else:
            new_value = ''

        value = value.replace(match[0], new_value)

    return value

def parse_payload_values(value: str, payload_values: dict[str, str]) -> str:
    for match in re.finditer(r'\${payload:(\w+)\}', value):
        key = match[1]
        payload_value = payload_values.get(key) or ''
        value = value.replace(match[0], payload_value)

    return value
