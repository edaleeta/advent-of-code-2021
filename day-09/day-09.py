# FILE_NAME = "day-09-test-input.txt"
FILE_NAME = "day-09-input.txt"


def parse_input_to_height_map():
    with open(FILE_NAME) as input:
        height_map = []
        for line in input:
            line = line.strip()
            heights = [int(h) for h in line]
            height_map.append(heights)
    return height_map


def get_total_risk_level():
    height_map = parse_input_to_height_map()
    if len(height_map) == 0:
        return 0

    row_length = len(height_map[0])
    height_map_adjacents = []

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


# print(get_total_risk_level())


def get_basin_sizes():
    height_map = parse_input_to_height_map()
    checked = set()
    basins = []

    def check_adjacent(basin, i, j):
        if height_map[i][j] == 9 or (i, j) in checked:
            checked.add((i, j))
            return basin

        basin.add((i, j))
        checked.add((i, j))

        if i != 0:
            check_adjacent(basin, i-1, j)
        if i != len(height_map) - 1:
            check_adjacent(basin, i+1, j)
        if j != 0:
            check_adjacent(basin, i, j-1)
        if j != len(height_map[i]) - 1:
            check_adjacent(basin, i, j+1)

        return basin

    for i in range(len(height_map)):
        for j in range(len(height_map[i])):
            basin = check_adjacent(set(), i, j)
            if len(basin) > 0:
                basins.append(basin)

    basin_sizes = [len(basin) for basin in basins]
    return basin_sizes


def get_product_of_largest_n_basin_sizes(n):
    basin_sizes = get_basin_sizes()
    basin_sizes.sort(reverse=True)
    largest_n_basin_sizes = basin_sizes[:n]
    product = 1
    for size in largest_n_basin_sizes:
        product *= size
    return product


print(get_product_of_largest_n_basin_sizes(3))
