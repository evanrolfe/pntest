from __future__ import annotations
from typing import Optional
from lib.input_parsing.text_wrapper import TextWrapper

OPENING_CHARS = "{"
CLOSING_CHARS = "}"

class TreeNode:
    left: Optional[TreeNode]
    right: Optional[TreeNode]
    children: list[TreeNode]

    def __init__(self, data):
        self.data = data
        self.left = self.right = None
        self.children = []

    def debug(self, level = 0):
        tabs = level * "-"
        print(tabs, self.data)

        if self.left is not None:
            self.left.debug(level+1)

        if self.right is not None:
            self.right.debug(level+1)

    def debug_children(self, level = 1):
        tabs = level * "-"
        print(tabs, self.data)

        for child in self.children:
            child.debug_children(level + 1)

    def add_child(self, child: TreeNode):
        self.children.append(child)

def find_closing_chars_index(input, start_index, end_index):
    if (start_index > end_index):
        return -1

    # Inbuilt stack
    s = []
    for i in range(start_index, end_index + 1):
        # if open parenthesis, push it
        prev = input[i-1] if i-1 > 0 else None
        if (input[i] == OPENING_CHARS and prev == "$"):
            s.append(input[i])

        # if close parenthesis
        elif (input[i] == CLOSING_CHARS):
            if (s[-1] == OPENING_CHARS):
                s.pop(-1)

                # if stack is empty, this is the required index
                if len(s) == 0:
                    return i

    # if not found return -1
    return -1

def find_opening_chars_index(input, start_index, end_index):
    for i in range(start_index, end_index + 1):
        prev = input[i-1] if i-1 > 0 else None
        if input[i] == OPENING_CHARS and prev == "$":
            return i

    return -1

def tree_node_from_string(input, start_index, end_index) -> Optional[TreeNode]:
    # Base case
    if (start_index > end_index):
        return None

    sub_string = input[start_index:end_index]

    root = TreeNode(sub_string)

    i = start_index
    while i < end_index:
        prev = input[i-1] if i-1 > 0 else None
        if input[i] == OPENING_CHARS and prev == "$":
            opening_chars_index = i
            closing_chars_index = find_closing_chars_index(input, opening_chars_index, end_index)

            child = tree_node_from_string(input, opening_chars_index+1, closing_chars_index)
            if child is not None:
                root.add_child(child)

            i = closing_chars_index
        else:
            i += 1

    return root

class TestTree:
    def test_tree(self):
        input = "axxx${${b}x${c${grandchild}}bbbasdf${fuckoff}}"
        #input = "axxx${b}"
        root = tree_node_from_string(input, 0, len(input))
        if root is None:
            return

        print("")
        root.debug_children()
        assert 1 == 1

