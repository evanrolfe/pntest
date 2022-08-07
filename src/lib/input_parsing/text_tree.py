from __future__ import annotations
from typing import Optional

OPENING_CHAR0 = "$"
OPENING_CHAR1 = "{"
CLOSING_CHAR = "}"

class TreeNode:
    raw_text: str
    children: list[TreeNode]

    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.children = []

    def debug(self, level = 1):
        tabs = level * "-"
        print(tabs, self.raw_text)

        for child in self.children:
            child.debug(level + 1)

    def add_child(self, child: TreeNode):
        self.children.append(child)

def find_closing_chars_index(input: str, start_index: int, end_index: int):
    if (start_index > end_index):
        return -1

    # Inbuilt stack
    s = []
    for i in range(start_index, end_index + 1):
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

    root = TreeNode(sub_string)

    i = start_index
    while i < end_index:
        if input[i] == OPENING_CHAR1 and get_prev_char(input, i) == OPENING_CHAR0:
            opening_chars_index = i
            closing_chars_index = find_closing_chars_index(input, opening_chars_index, end_index)

            child = tree_node_from_string(input, opening_chars_index+1, closing_chars_index)
            if child is not None:
                root.add_child(child)

            i = closing_chars_index
        else:
            i += 1

    return root

