from __future__ import annotations
from typing import Any, Optional, TypedDict
import re

from lib.input_parsing.text_tree import TreeNode, tree_node_from_string

def parse_text(value: str) -> str:
    text_wrapper = TextWrapper(value, {})
    return text_wrapper.get_parsed_text()

def parse_text_with_payload_values(value: str, payload_values: dict[str, str]) -> str:
    text_wrapper = TextWrapper(value, payload_values)
    return text_wrapper.get_parsed_text()

def get_matches_for_indicators(value: str) -> list[TreeNode]:
    text_wrapper = TextWrapper(value, {})
    return text_wrapper.get_immediate_children()

class TextWrapper:
    raw_text: str
    parsed_text: str
    payload_values: dict[str, str]

    def __init__(self, raw_text: str, payload_values: dict[str, str]):
        self.raw_text = raw_text
        self.parsed_text = raw_text
        self.payload_values = payload_values

    def set_text(self, raw_text: str):
        self.raw_text = raw_text

    def find_node_containing_index(self, index: int) -> Optional[TreeNode]:
        root_node = self.get_text_tree(self.raw_text)
        if root_node is None:
            return None

        return root_node.find_node_containing_index(index)

    def get_immediate_children(self) -> list[TreeNode]:
        root_node = self.get_text_tree(self.raw_text)
        if root_node is None:
            return []

        return root_node.children

    def get_parsed_text(self) -> str:
        root_node = self.get_text_tree(self.parsed_text)

        if root_node is None:
            return self.parsed_text

        while len(root_node.children) > 0:
            root_node = self.get_text_tree(self.parsed_text)

            if root_node is None:
                raise Exception("root_node returns None")

            if len(root_node.children) == 0:
                return self.parsed_text

            leaf_nodes = root_node.get_leaves()
            for leaf in leaf_nodes:
                parsed_value = leaf.get_transformed_value() or ''
                self.parsed_text = self.parsed_text.replace("${" + leaf.sub_str + "}", parsed_value)

        return self.parsed_text

    def get_text_tree(self, text: str) -> Optional[TreeNode]:
        return tree_node_from_string(text, 0, len(text), self.payload_values)
