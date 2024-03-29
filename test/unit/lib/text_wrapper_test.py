from lib.input_parsing.text_wrapper import TextWrapper
from entities.variable import Variable
from repos.variable_repo import VariableRepo

class TestTextWrapper:
    def test_parsing_variable_inside_encoding(self, database, cleanup_database):
        var1 = Variable(key='myVar', value='hello', source_type=Variable.SOURCE_TYPE_GLOBAL)
        var2 = Variable(key='otherVar', value='world', source_type=Variable.SOURCE_TYPE_GLOBAL)
        VariableRepo().save(var1)
        VariableRepo().save(var2)

        value = '{"this is var:": "${b64:${var:myVar} - ${var:otherVar}}","asdf": "another one!"}'
        text_wrapper = TextWrapper(value, {})
        result = text_wrapper.get_parsed_text()

        assert result == '{"this is var:": "aGVsbG8gLSB3b3JsZA==","asdf": "another one!"}'

    def test_finding_the_node_containing_index(self, database, cleanup_database):
        var1 = Variable(key='myVar', value='hello', source_type=Variable.SOURCE_TYPE_GLOBAL)
        var2 = Variable(key='otherVar', value='world', source_type=Variable.SOURCE_TYPE_GLOBAL)
        VariableRepo().save(var1)
        VariableRepo().save(var2)

        value = '{"this is var:": "${b64:${var:myVar} - ${var:otherVar}}","asdf": "another one!"}'
        text_wrapper = TextWrapper(value, {})

        var_node = text_wrapper.find_node_containing_index(54)

        assert var_node is not None
        assert var_node.sub_str == 'b64:${var:myVar} - ${var:otherVar}'

    def test_when_a_node_contains_an_invalid_value(self, database, cleanup_database):
        var1 = Variable(key='myVar', value='hello', source_type=Variable.SOURCE_TYPE_GLOBAL)
        var2 = Variable(key='otherVar', value='world', source_type=Variable.SOURCE_TYPE_GLOBAL)
        VariableRepo().save(var1)
        VariableRepo().save(var2)

        value = '{"this is var:": "${var:otherVar}","asdf": "${this_is_not_valid}"}'
        text_wrapper = TextWrapper(value, {})

        result = text_wrapper.get_parsed_text()
        child_nodes = text_wrapper.get_immediate_children()

        assert result == '{"this is var:": "world","asdf": "${this_is_not_valid}"}'
        assert len(child_nodes) == 1

    def test_when2(self, database, cleanup_database):
        value = """{
    "this is var:": "${var:baseUrl}",
    "& this is an encoding!": "${ascii:hello}",
    "asdf": "another one!${md5:adsf}"
}"""
        text_wrapper = TextWrapper(value, {})

        result = text_wrapper.find_node_containing_index(15)
        print(result)

    # TODO: Make it handle this case correctly
    def test_a_weird_syntax_situation(self, database, cleanup_database):
        value = '{"this is var:": "${var:myVar}","asdf": "another one!"}'
        text_wrapper = TextWrapper(value, {})
        children = text_wrapper.get_immediate_children()

    def test_when_text_contains_a_node_and_nothing_else(self, database, cleanup_database):
        var1 = Variable(key='myVar', value='hello', source_type=Variable.SOURCE_TYPE_GLOBAL)
        VariableRepo().save(var1)

        value = '${var:myVar}'
        text_wrapper = TextWrapper(value, {})

        result = text_wrapper.get_parsed_text()
        assert result == "hello"
