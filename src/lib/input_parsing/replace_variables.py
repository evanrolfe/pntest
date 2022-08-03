import re
from models.data.variable import Variable

VAR_REGEX = r'\${var:([^}]+)}'

# parse_value replace variables, encodings, hashes etc. it is called when an HttpRequest is saved
# from the request edit form
def replace_variables(value: str) -> str:
    for match in re.finditer(VAR_REGEX, value):
        key = match[1]
        var = Variable.find_by_key(key)

        if var:
            new_value = var.value
        else:
            new_value = ''

        value = value.replace(match[0], new_value)

    return value
