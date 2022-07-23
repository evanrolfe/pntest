from lib.input_parsing.parse import parse_value

class TestFuzzHttpRequests:
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
