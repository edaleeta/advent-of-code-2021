# FILE_NAME = "day-07-test-input.txt"
FILE_NAME = "day-07-input.txt"


# Checking input
def print_possible_moves(positions, is_part_two=False):
    positions.sort()
    for i, position in enumerate(positions):
        cost = 0
        for j in range(len(positions)):
            if j == i:
                continue
            moving_position = positions[j]
            distance = abs(moving_position - position)
            if is_part_two:
                cost += sum([i for i in range(1, distance + 1)])
            else:
                cost += distance

        print(f"Cost to move all to {position}: {cost}")


def get_lowest_cost(positions, is_part_two=False):
    positions.sort()
    converge_position = round(sum(positions) // len(positions)) if is_part_two else positions[len(positions) // 2]
    converge_positions = [converge_position, converge_position + 1]

    lowest_cost = None
    for converge_position in converge_positions:
        cost = 0
        for position in positions:
            distance = abs(position - converge_position)
            if is_part_two:
                cost += sum([i for i in range(1, distance + 1)])
            else:
                cost += abs(position - converge_position)
        if lowest_cost is None or cost < lowest_cost:
            lowest_cost = cost
    return lowest_cost


def parse_input():
    with open(FILE_NAME) as input:
        line = input.readline().rstrip()
        return [int(num) for num in line.split(",")]


input = parse_input()
# print(print_possible_moves(input))
print(get_lowest_cost(input))
# print_possible_moves(input, is_part_two=True)
print(get_lowest_cost(input, is_part_two=True))
