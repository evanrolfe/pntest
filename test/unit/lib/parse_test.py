from lib.input_parsing.parse import parse_value
from lib.input_parsing.encode_base64 import EncodeBase64
from lib.input_parsing.encode_base64_url import EncodeBase64Url
from lib.input_parsing.encode_url import EncodeUrl
from lib.input_parsing.encode_url_full import EncodeUrlFull
from lib.input_parsing.encode_ascii_hex import EncodeAsciiHex
from lib.input_parsing.encode_html import EncodeHTML
from lib.input_parsing.encode_js import EncodeJs

class TestFuzzHttpRequests:
    # Encoding Tests
    def test_parsing_base64_encode(self, database, cleanup_database):
        result = parse_value("the value: ${b64:hello world} is encoded")
        assert result == "the value: aGVsbG8gd29ybGQ= is encoded"

    def test_parsing_base64url_encode(self, database, cleanup_database):
        result = parse_value("the value: ${b64url:hello world} is encoded")
        assert result == "the value: aGVsbG8gd29ybGQ= is encoded"

    def test_parsing_url_encode(self, database, cleanup_database):
        result = parse_value("the value: ${url:hello world} is encoded")
        assert result == "the value: hello+world is encoded"

    def test_parsing_url_full_encode(self, database, cleanup_database):
        result = parse_value("the value: ${urlfull:hello world} is encoded")
        assert result == "the value: hello%20world is encoded"

    def test_parsing_ascii_hex_encode(self, database, cleanup_database):
        result = parse_value("the value: ${ascii:hello world} is encoded")
        assert result == "the value: 68656c6c6f20776f726c64 is encoded"

    # def test_parsing_html_encode(self, database, cleanup_database):
    #     result = parse_value("the value: ${b64:hello world} is encoded")
    #     assert result == "the value: aGVsbG8gd29ybGQ= is encoded"

    # def test_parsing_js_encode(self, database, cleanup_database):
    #     result = parse_value("the value: ${b64:hello world} is encoded")
    #     assert result == "the value: aGVsbG8gd29ybGQ= is encoded"

    # Decoding Tests
    def test_parsing_base64_decode(self, database, cleanup_database):
        result = EncodeBase64().decode("aGVsbG8gd29ybGQ=")
        assert result == "hello world"

    def test_parsing_base64url_decode(self, database, cleanup_database):
        result = EncodeBase64Url().decode("aGVsbG8gd29ybGQ=")
        assert result == "hello world"

    def test_parsing_url_decode(self, database, cleanup_database):
        result = EncodeUrl().decode("hello+world")
        assert result == "hello world"

    def test_parsing_url_full_decode(self, database, cleanup_database):
        result = EncodeUrlFull().decode("hello%20world")
        assert result == "hello world"

    def test_parsing_ascii_hex_decode(self, database, cleanup_database):
        result = EncodeAsciiHex().decode("68656c6c6f20776f726c64")
        assert result == "hello world"
