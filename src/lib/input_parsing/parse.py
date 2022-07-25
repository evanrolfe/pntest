import re
import typing
from lib.input_parsing.replace_variables import replace_variables
from lib.input_parsing.encode_base64 import EncodeBase64
from lib.input_parsing.encode_base64_url import EncodeBase64Url
from lib.input_parsing.encode_url import EncodeUrl
from lib.input_parsing.encode_url_full import EncodeUrlFull
from lib.input_parsing.encode_ascii_hex import EncodeAsciiHex
from lib.input_parsing.encode_html import EncodeHTML
from lib.input_parsing.encode_js import EncodeJs
from lib.input_parsing.encoder import Encoder

from lib.input_parsing.hash_md5 import HashMD5
from lib.input_parsing.hash_sha1 import HashSHA1
from lib.input_parsing.hash_sha256 import HashSHA256

PAYLOAD_REGEX = r'\${payload:(\w+)\}'

def get_available_encoders() -> list[Encoder]:
    return [
        EncodeBase64(),
        EncodeBase64Url(),
        EncodeUrl(),
        EncodeUrlFull(),
        EncodeAsciiHex(),
        EncodeHTML(),
        EncodeJs(),
    ]

def get_available_hashers() -> list[Encoder]:
    return [
        HashMD5(),
        HashSHA1(),
        HashSHA256(),
    ]

# parse_value replace variables, encodings, hashes etc. it is called when an HttpRequest is saved
# from the request edit form
def parse_value(value: str) -> str:
    value = replace_variables(value)
    value = replace_encoded_value(EncodeBase64(), value)
    value = replace_encoded_value(EncodeBase64Url(), value)
    value = replace_encoded_value(EncodeUrl(), value)
    value = replace_encoded_value(EncodeUrlFull(), value)
    value = replace_encoded_value(EncodeAsciiHex(), value)
    value = replace_encoded_value(EncodeHTML(), value)
    value = replace_encoded_value(EncodeJs(), value)

    value = replace_encoded_value(HashMD5(), value)
    value = replace_encoded_value(HashSHA1(), value)
    value = replace_encoded_value(HashSHA256(), value)

    return value

def replace_encoded_value(encoder: Encoder, value: str):
    regex = r'\${' + encoder.key + ':(.+)}'
    for match in re.finditer(regex, value):
        value_to_encode = match[1]
        value = value.replace(match[0], encoder.encode(value_to_encode))

    return value

# parse_payload_values replaces payload values and is called at a different time than parse_value is.
# it is called only when the fuzz button is clicked (lib.FuzzHttpRequests)
def parse_payload_values(value: str, payload_values: dict[str, str]) -> str:
    for match in re.finditer(PAYLOAD_REGEX, value):
        key = match[1]
        payload_value = payload_values.get(key) or ''
        value = value.replace(match[0], payload_value)

    return value
