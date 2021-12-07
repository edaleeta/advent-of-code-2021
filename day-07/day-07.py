# FILE_NAME = "day-07-test-input.txt"
FILE_NAME = "day-07-input.txt"


# Checking input
def get_possible_moves(positions):
    positions.sort()
    for i, position in enumerate(positions):
        cost = 0
        for j in range(len(positions)):
            if j == i:
                continue
            moving_position = positions[j]
            cost += abs(moving_position - position)

        print(f"Cost to move all to {position}: {cost}")


def get_lowest_cost(positions):
    positions.sort()
    middle = len(positions) // 2

    converge_position = positions[middle]
    cost = 0
    for position in positions:
        cost += abs(position - converge_position)

    return cost


def parse_input():
    with open(FILE_NAME) as input:
        line = input.readline().rstrip()
        return [int(num) for num in line.split(",")]


input = parse_input()
# print(get_possible_moves(input))
print(get_lowest_cost(input))
