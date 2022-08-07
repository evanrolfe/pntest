from __future__ import annotations
from typing import Optional
from lib.input_parsing.text_tree import tree_node_from_string

class TestTree:
    def test_tree(self):
        input = "axxx${${b}x${c${grandchild}}bbbasdf${fuckoff}}"
        #input = "axxx${b}"
        root = tree_node_from_string(input, 0, len(input))
        if root is None:
            return

        print("")
        root.debug()
        assert 1 == 1

