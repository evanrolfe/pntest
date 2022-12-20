import re
from lib.input_parsing.text_wrapper import parse_text
from lib.input_parsing.encode_base64 import EncodeBase64
from lib.input_parsing.encode_base64_url import EncodeBase64Url
from lib.input_parsing.encode_url import EncodeUrl
from lib.input_parsing.encode_url_full import EncodeUrlFull
from lib.input_parsing.encode_ascii_hex import EncodeAsciiHex
from lib.input_parsing.encode_html import EncodeHTML
from lib.input_parsing.encode_js import EncodeJs

class TestFuzzHttpRequests:
    # Encoding Tests
    def test_parsing_base64_encode(self, database):
        result = parse_text('{"this is var:": "${var:test}","& this is an encoding!": "${b64:hello world}","asdf": "another one!"}')
        assert result == '{"this is var:": "","& this is an encoding!": "aGVsbG8gd29ybGQ=","asdf": "another one!"}'

    def test_parsing_base64url_encode(self, database):
        result = parse_text("the value: ${b64url:hello world} is encoded")
        assert result == "the value: aGVsbG8gd29ybGQ= is encoded"

    def test_parsing_url_encode(self, database):
        result = parse_text("the value: ${url:hello world} is encoded")
        assert result == "the value: hello+world is encoded"

    def test_parsing_url_full_encode(self, database):
        result = parse_text("the value: ${urlfull:hello world} is encoded")
        assert result == "the value: hello%20world is encoded"

    def test_parsing_ascii_hex_encode(self, database):
        result = parse_text("the value: ${ascii:hello world} is encoded")
        assert result == "the value: 68656c6c6f20776f726c64 is encoded"

    def test_parsing_html_encode(self, database):
        result = parse_text("the value: ${html:<hello>} is encoded")
        assert result == "the value: &lt;hello&gt; is encoded"

    def test_parsing_js_encode(self, database):
        result = parse_text("the value: ${js:hello£} is encoded")
        assert result == "the value: hello\\u00a3 is encoded"

    # # Decoding Tests
    def test_parsing_base64_decode(self, database):
        result = EncodeBase64().decode("aGVsbG8gd29ybGQ=")
        assert result == "hello world"

    def test_parsing_base64url_decode(self, database):
        result = EncodeBase64Url().decode("aGVsbG8gd29ybGQ=")
        assert result == "hello world"

    def test_parsing_url_decode(self, database):
        result = EncodeUrl().decode("hello+world")
        assert result == "hello world"

    def test_parsing_url_full_decode(self, database):
        result = EncodeUrlFull().decode("hello%20world")
        assert result == "hello world"

    def test_parsing_ascii_hex_decode(self, database):
        result = EncodeAsciiHex().decode("68656c6c6f20776f726c64")
        assert result == "hello world"

    def test_parsing_html_decode(self, database):
        result = EncodeHTML().decode("&lt;hello&gt;")
        assert result == "<hello>"

    def test_parsing_js_decode(self, database):
        result = EncodeJs().decode("hello\\u00a3")
        assert result == "hello£"

    # # # Hasher Tests
    def test_parsing_md5_hash(self, database):
        result = parse_text("the value: ${md5:123} is encoded")
        assert result == "the value: 202cb962ac59075b964b07152d234b70 is encoded"

    def test_parsing_sha1_hash(self, database):
        result = parse_text("the value: ${sha1:123} is encoded")
        assert result == "the value: 40bd001563085fc35165329ea1ff5c5ecbdbbeef is encoded"

    def test_parsing_sha256_hash(self, database):
        result = parse_text("the value: ${sha256:123} is encoded")
        assert result == "the value: a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3 is encoded"
