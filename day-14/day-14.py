# FILE_NAME = "day-14-test-input.txt"
FILE_NAME = "day-14-input.txt"


def parse_input():
    with open(FILE_NAME) as input:
        line = input.readline().strip()
        template = [char for char in line]
        input.readline()

        insertion_rules = {}
        for line in input:
            line = line.strip()
            key, value = line.split(' -> ')
            insertion_rules[key] = value

    return template, insertion_rules


def get_polymer_element_difference(n):
    polymer_template, insertion_rules = parse_input()
    pair_to_count = {}
    pair_to_count_temp = {}
    element_to_count = {}
    for element in polymer_template:
        count = element_to_count.get(element, 0) + 1
        element_to_count[element] = count

    for i in range(len(polymer_template)-1):
        j = i + 1
        a = polymer_template[i]
        b = polymer_template[j]
        key = f"{a}{b}"
        count = pair_to_count.get(key, 0) + 1
        pair_to_count[key] = count

    for _ in range(n):
        for pair, count in pair_to_count.items():
            new_element = insertion_rules.get(pair)
            new_pair_a = pair[0] + new_element
            new_pair_b = new_element + pair[1]

            count_a = pair_to_count_temp.get(new_pair_a, 0) + count
            pair_to_count_temp[new_pair_a] = count_a

            count_b = pair_to_count_temp.get(new_pair_b, 0) + count
            pair_to_count_temp[new_pair_b] = count_b

            element_count = element_to_count.get(new_element, 0) + count
            element_to_count[new_element] = element_count

        pair_to_count = pair_to_count_temp
        pair_to_count_temp = {}

    max_count = None
    min_count = None

    for count in element_to_count.values():
        if max_count is None:
            max_count = count
        if min_count is None:
            min_count = count

        if count < min_count:
            min_count = count
        if count > max_count:
            max_count = count

    return max_count - min_count


print(get_polymer_element_difference(n=10))
print(get_polymer_element_difference(n=40))
