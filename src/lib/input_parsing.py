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
