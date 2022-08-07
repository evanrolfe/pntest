from __future__ import annotations
from typing import Any, Optional, TypedDict

from lib.input_parsing.text_tree import TreeNode, tree_node_from_string

class TextRange(TypedDict):
    line_start: int
    col_start: int
    line_end: int
    col_end: int

class TextWrapper:
    raw_text: str

    def __init__(self, raw_text: str):
        self.raw_text = raw_text

    def set_text(self, raw_text: str):
        self.raw_text = raw_text

    def get_parsed_text(self) -> str:


        return ''

    def get_text_tree(self) -> Optional[TreeNode]:
        return tree_node_from_string(self.raw_text, 0, len(self.raw_text))
