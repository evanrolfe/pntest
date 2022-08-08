from lib.input_parsing.text_wrapper import TextWrapper
from models.data.variable import Variable
from support.factories import factory

class TestTextWrapper:
    def test_parsing_variable_inside_encoding(self, database, cleanup_database):
        factory(Variable, 'global').create(key='myVar', value='hello')
        factory(Variable, 'global').create(key='otherVar', value='world')

        value = '{"this is var:": "${b64:${var:myVar} - ${var:otherVar}}","asdf": "another one!"}'
        text_wrapper = TextWrapper(value)
        result = text_wrapper.get_parsed_text()

        assert result == '{"this is var:": "aGVsbG8gLSB3b3JsZA==","asdf": "another one!"}'
