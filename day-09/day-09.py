# FILE_NAME = "day-09-test-input.txt"
FILE_NAME = "day-09-input.txt"


def get_total_risk_level():
    row_length = None
    height_map = []
    height_map_adjacents = []

    with open(FILE_NAME) as input:
        for line in input:
            line = line.strip()
            heights = [int(h) for h in line]
            height_map.append(heights)
            if row_length is None:
                row_length = len(heights)

    for i in range(len(height_map)):
        empty_row_adjacents = [set() for _ in range(row_length)]
        height_map_adjacents.append(empty_row_adjacents)

        i_heights = height_map[i]
        for j in range(len(i_heights)):
            current_adjacent_set = height_map_adjacents[i][j]

            if i != 0:
                above_value = height_map[i-1][j]
                current_adjacent_set.add(above_value)
            if i != len(height_map)-1:
                below_value = height_map[i+1][j]
                current_adjacent_set.add(below_value)
            if j != 0:
                left_value = height_map[i][j-1]
                current_adjacent_set.add(left_value)
            if j != len(i_heights)-1:
                right_value = height_map[i][j+1]
                current_adjacent_set.add(right_value)

    total_risk_level = 0
    for i in range(len(height_map)):
        for j in range(len(height_map[i])):
            current_height = height_map[i][j]
            current_height_adjacent = height_map_adjacents[i][j]
            if all([current_height < adjacent_height for adjacent_height in current_height_adjacent]):
                total_risk_level += current_height + 1

    return total_risk_level


print(get_total_risk_level())
