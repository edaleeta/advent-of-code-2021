# FILE_NAME = 'day-03-test-input.txt'
FILE_NAME = 'day-03-input.txt'


def convert_binary_to_decimal(binary_chars):
    return int(''.join(binary_chars), 2)


def get_count_zeroes_ones_in_positions():
    count_zeroes = []
    count_ones = []
    with open(FILE_NAME) as input:
        for bnumber in input:
            bnumber = bnumber[:-1]  # Omit return char
            # First line, init values
            if not count_zeroes and not count_ones:
                count_zeroes = [0] * len(bnumber)
                count_ones = [0] * len(bnumber)

            for i, digit in enumerate(bnumber):
                if digit == '0':
                    count_zeroes[i] = count_zeroes[i] + 1
                else:
                    count_ones[i] = count_ones[i] + 1

    return count_zeroes, count_ones


def get_epsilon_and_gamma():
    count_zeroes, count_ones = get_count_zeroes_ones_in_positions()
    epsilon_binary, gamma_binary = [], []

    for count_zero, count_one in zip(count_zeroes, count_ones):
        if count_zero > count_one:
            epsilon_binary.append('0')
            gamma_binary.append('1')
        else:
            epsilon_binary.append('1')
            gamma_binary.append('0')

    return convert_binary_to_decimal(epsilon_binary), convert_binary_to_decimal(gamma_binary)


def get_power_consumption():
    epsilon, gamma = get_epsilon_and_gamma()
    print(f"epsilon: {epsilon}, gamma: {gamma}")
    return epsilon * gamma


class Node:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_end = True

    def get_values(self):
        values = []

        def recur(node, output=''):
            if node.is_end:
                values.append(output)
                return
            for char in node.children:
                recur(node.children[char], output + char)

        recur(self.root)
        return values

    def remove_char_at_position(self, remove_char, remove_position):

        def recur(node, current_position):
            if current_position == remove_position:
                # At the level where node should be in the children
                if remove_char not in node.children:
                    return
                del node.children[remove_char]
            else:
                # Need to traverse through children
                for char in node.children:
                    recur(node.children[char], current_position + 1)

        recur(self.root, 0)


def filter_input_by_mode(mode):
    """
    mode = 1 -> keeps most common digit in position, 1 if equal
    mode = 2 -> keeps least common digit in position, 0 if equal
    """

    len_bnumber = None
    trie = Trie()
    with open(FILE_NAME) as input:
        for bnumber in input:
            bnumber = bnumber[:-1]
            trie.insert(bnumber)
            if len_bnumber is None:
                len_bnumber = len(bnumber)

    values = trie.get_values()
    i = 0
    while len(values) > 1 and i < len_bnumber:
        count_zero = 0
        count_one = 0
        for value in values:
            if value[i] == '0':
                count_zero += 1
            else:
                count_one += 1

        if mode == 1:
            digit_to_discard = '1' if count_zero > count_one else '0'
        else:
            digit_to_discard = '0' if count_zero > count_one else '1'

        trie.remove_char_at_position(digit_to_discard, i)
        values = trie.get_values()
        i += 1

    if not values:
        print("Oops, all values were removed!")
        return
    if not len(values) == 1:
        print(f"Oops, had more than one value left: {values}")

    return values[0]


def get_oxygen_and_co2_scrubber_ratings():
    oxygen_rating_binary = filter_input_by_mode(mode=1)
    co2_scrubber_rating_binary = filter_input_by_mode(mode=2)
    return convert_binary_to_decimal(oxygen_rating_binary), convert_binary_to_decimal(co2_scrubber_rating_binary)


def get_life_support_rating():
    oxygen_rating, co2_scrubber_rating = get_oxygen_and_co2_scrubber_ratings()
    print(f"oxygen rating: {oxygen_rating}, co2 scrubber rating: {co2_scrubber_rating}")
    return oxygen_rating * co2_scrubber_rating


print(get_power_consumption())
print(get_life_support_rating())
