
from typing import Optional
from lib.input_parsing.encoder import Encoder
from lib.input_parsing.text_tree import TreeNode

# TODO: This is not actually a widget, should probably go in models/qt
class UserAction:
    trigger: str
    # If a user is updating an exisitn node, then this will be set:
    node: Optional[TreeNode]
    # These are the values the user selects
    transformer: Optional[Encoder]
    value_to_transform: str

    TRIGGER_RIGHT_CLICK = 'right_click'
    TRIGGER_TEXT = 'text'
    TRIGGER_INDICATOR_CLICK = 'indicator_click'

    def __init__(self, trigger: str, node: Optional[TreeNode] = None):
        self.trigger = trigger
        self.node = node
        self.value_to_transform = ''

    def set_transformer(self, transformer: Encoder):
        self.transformer = transformer

    def set_value_to_transform(self, value: str):
        self.value_to_transform = value
