import json
import time

# FILE_NAME = "day-18-test-input.txt"
# FILE_NAME = "day-18-test-input-b.txt"
FILE_NAME = "day-18-input.txt"


class Node:
    def __init__(self, value, parent=None):
        self.parent = parent
        self.depth = self.parent.depth + 1 if parent else 0

        if isinstance(value, list):
            self.is_pair = True
            self.left = Node(value[0], self)
            self.right = Node(value[1], self)
        elif isinstance(value, Node):
            self.is_pair = value.is_pair
            if self.is_pair:
                self.left = Node(value.left, self)
                self.right = Node(value.right, self)
            else:
                self.value = value.value
        else:
            self.is_pair = False
            self.value = value

    def __repr__(self):
        if not self.is_pair:
            return str(self.value)
        return f"[{self.left},{self.right}]"

    def __add__(self, other):
        return Node([self, other]).reduce()

    @staticmethod
    def _find_left(root, value):
        if not root:
            return None
        if root.left == value:
            return Node._find_left(root.parent, root)
        return root.left.find_first_right()

    @staticmethod
    def _find_right(root, value):
        if not root:
            return None
        if root.right == value:
            return Node._find_right(root.parent, root)
        return root.right.find_first_left()

    def find_first_left(self):
        if self.is_pair:
            return self.left.find_first_left()
        return self

    def find_first_right(self):
        if self.is_pair:
            return self.right.find_first_right()
        return self

    def find_left(self):
        return Node._find_left(self.parent, self)

    def find_right(self):
        return Node._find_right(self.parent, self)

    def find_explode(self):
        if self.is_pair:
            if self.depth >= 4:
                return self
            return self.left.find_explode() or self.right.find_explode()
        return None

    def explode(self):
        node = self.find_explode()
        if not node:
            return False

        node_to_left = node.find_left()
        node_to_right = node.find_right()
        if node_to_left:
            node_to_left.value += node.left.value
        if node_to_right:
            node_to_right.value += node.right.value

        node.is_pair = False
        node.value = 0
        return True

    def find_split(self):
        if not self.is_pair:
            if self.value >= 10:
                return self
            else:
                return None
        return self.left.find_split() or self.right.find_split()

    def split(self):
        node = self.find_split()
        if not node:
            return False

        left_value = node.value // 2
        right_value = node.value - (node.value // 2)

        node.is_pair = True
        node.left = Node(left_value, node)
        node.right = Node(right_value, node)
        return True

    def reduce(self):
        is_reducing = True
        while is_reducing:
            is_reducing = self.explode()
            if not is_reducing:
                is_reducing = self.split()

        return self

    @staticmethod
    def _calc_magnitude(root):
        if not root.is_pair:
            return root.value
        return 3 * Node._calc_magnitude(root.left) + 2 * Node._calc_magnitude(root.right)

    @property
    def magnitude(self):
        return self._calc_magnitude(self)


def test_pair():
    # [[1,9],[8,5]]
    value = json.loads('[[1,9],[8,5]]')
    root = Node(value)
    print(root)

    # [[[[1,2],[3,4]],[[5,6],[7,8]]],9]
    value = json.loads('[[[[1,2],[3,4]],[[5,6],[7,8]]],9]')
    root = Node(value)
    print(root)


def test_reduction():
    test_inputs = [
        '[[[[[9,8],1],2],3],4]',
        '[7,[6,[5,[4,[3,2]]]]]',
        '[[6,[5,[4,[3,2]]]],1]',
        '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
        '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'
    ]
    for test_input in test_inputs:
        root = Node(json.loads(test_input))
        print(f"{root} reduces to:")
        root.reduce()
        print(root)

# test_reduction()


def get_sum(inputs):
    nodes = [Node(json.loads(input)) for input in inputs]
    return sum(nodes[1:], nodes[0])


def parse_input():
    input_strings = []
    with open(FILE_NAME) as input:
        for line in input:
            input_strings.append(line.strip())
    return input_strings


snailfish_sum = get_sum(parse_input())
print(f"{snailfish_sum}, magnitude: {snailfish_sum.magnitude}")


def get_largest_magnitude_of_any_sum():
    start = time.time()
    input_strings = parse_input()
    string_to_node = {string: Node(json.loads(string)) for string in input_strings}
    permutations = []
    i = 0
    while i < len(input_strings) - 1:
        j = i + 1
        while j < len(input_strings):
            permutations.extend([[input_strings[i], input_strings[j]], [input_strings[j], input_strings[i]]])
            j += 1
        i += 1

    max_magnitude = 0
    for first, second in permutations:
        first_node = string_to_node.get(first)
        second_node = string_to_node.get(second)
        snailfish_sum = first_node + second_node
        sum_magnitude = snailfish_sum.magnitude
        if sum_magnitude > max_magnitude:
            max_magnitude = sum_magnitude
    print(f'done in {(time.time() - start) * 1000}ms')
    return max_magnitude


print(f"Largest magnitude of two numbers: {get_largest_magnitude_of_any_sum()}")
