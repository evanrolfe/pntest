OPENING_CHARS = "{"
CLOSING_CHARS = "}"

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None

    def debug(self, level = 0):
        tabs = level * "-"
        print(tabs, self.data)

        if self.left is not None:
            self.left.debug(level+1)

        if self.right is not None:
            self.right.debug(level+1)

def find_closing_chars_index(input, start_index, end_index):
    if (start_index > end_index):
        return -1

    # Inbuilt stack
    s = []
    for i in range(start_index, end_index + 1):
        # if open parenthesis, push it
        if (input[i] == OPENING_CHARS):
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
        if input[i] == OPENING_CHARS:
            return i

    return -1

def tree_node_from_string(input, start_index, end_index):
    # Base case
    if (start_index > end_index):
        return None

    # new root
    sub_string = input[start_index:end_index+1]
    root = TreeNode(sub_string)

    opening_chars_index = find_opening_chars_index(input, start_index, end_index)
    closing_chars_index = -1

    print("===================================================================")
    print("start_index:", start_index, "end_index:", end_index)
    print("sub_string:", sub_string)

    # if next char is OPENING_CHARS find the index of its complement CLOSING_CHARS
    if start_index >= end_index:
        print("Terminal node.")
        return root

    if input[opening_chars_index] == OPENING_CHARS:
        closing_chars_index = find_closing_chars_index(input, opening_chars_index, end_index)

    # if index found
    if (closing_chars_index != -1):
        # print("opening_chars_index:", opening_chars_index)
        next_opening_chars_index = find_opening_chars_index(input, closing_chars_index + 1, end_index - 1)
        print("next_opening_chars_index:", next_opening_chars_index)
        print("Left tree: ", opening_chars_index + 1, ":", closing_chars_index - 1)
        print("Right tree: ", closing_chars_index + 2, ":", end_index - 1)
        # call for left subtree
        root.left = tree_node_from_string(input, opening_chars_index + 1, closing_chars_index - 1)

        # call for right subtree
        root.right = tree_node_from_string(input, next_opening_chars_index + 1, end_index - 1)

    return root


# Driver Code
if __name__ == '__main__':
    input = "aasdf{xxx{b}xxxxxzx{c}{d}}"
    #input = "44{3}"
    # print(input)
    root = tree_node_from_string(input, 0, len(input) - 1)
    root.debug()

