from __future__ import annotations
import re
from typing import Optional, Tuple

OPENING_CHAR0 = "$"
OPENING_CHAR1 = "{"
CLOSING_CHAR = "}"

class TreeNode:
    sub_str: str
    children: list[TreeNode]
    start_index: int
    end_index: int

    def __init__(self, sub_str: str, start_index: int, end_index: int):
        self.sub_str = sub_str
        self.start_index = start_index
        self.end_index = end_index
        self.children = []

    def debug(self, level = 1):
        tabs = level * "-"
        print(tabs, self.sub_str)

        for child in self.children:
            child.debug(level + 1)

    def add_child(self, child: TreeNode):
        self.children.append(child)

    def is_leaf_node(self) -> bool:
        return len(self.children) == 0

    def get_leaves(self):
        if self.is_leaf_node():
            yield self

        for child in self.children:
            for leaf in child.get_leaves():
                yield leaf

    def find_node_containing_index(self, index: int) -> Optional[TreeNode]:
        for child in self.children:
            if index >= child.start_index and index <= child.end_index:
                return child
            else:
                child.find_node_containing_index(index)

    def get_encoding_values(self) -> Optional[Tuple[str, str]]:
        REGEX = r'(\w+):(.*)'
        matches = re.match(REGEX, self.sub_str)
        if matches is None:
            return

        str_type = matches[1]
        value = matches[2]

        return (str_type, value)

    def get_type(self) -> Optional[str]:
        values = self.get_encoding_values()
        if values is not None:
            return values[0]

def find_closing_chars_index(input: str, start_index: int, end_index: int):
    if (start_index > end_index):
        return -1

    # Inbuilt stack
    s = []
    for i in range(start_index, end_index + 1):
        if i >= len(input):
            return -1

        # if open parenthesis, push it
        if (input[i] == OPENING_CHAR1 and get_prev_char(input, i) == OPENING_CHAR0):
            s.append(input[i])

        # if close parenthesis
        elif (input[i] == CLOSING_CHAR):
            if (s[-1] == OPENING_CHAR1):
                s.pop(-1)

                # if stack is empty, this is the required index
                if len(s) == 0:
                    return i

    # if not found return -1
    return -1

def find_opening_chars_index(input: str, start_index: int, end_index: int):
    for i in range(start_index, end_index + 1):
        if input[i] == OPENING_CHAR1 and get_prev_char(input, i) == OPENING_CHAR0:
            return i

    return -1

def get_prev_char(input: str, i: int) -> Optional[str]:
    return input[i-1] if i-1 > 0 else None

def tree_node_from_string(input: str, start_index: int, end_index: int) -> Optional[TreeNode]:
    # Base case
    if (start_index > end_index):
        return None

    sub_string = input[start_index:end_index]

    root = TreeNode(sub_string, start_index, end_index)

    i = start_index
    while i < end_index:
        if input[i] == OPENING_CHAR1 and get_prev_char(input, i) == OPENING_CHAR0:
            opening_chars_index = i
            closing_chars_index = find_closing_chars_index(input, opening_chars_index, end_index)

            if closing_chars_index == -1:
                return root

            child = tree_node_from_string(input, opening_chars_index+1, closing_chars_index)
            if child is not None:
                root.add_child(child)

            i = closing_chars_index
        else:
            i += 1

    return root

