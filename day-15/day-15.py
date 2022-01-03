# FILE_NAME = "day-15-test-input.txt"
FILE_NAME = "day-15-input.txt"


def parse_input():
    grid = []
    with open(FILE_NAME) as input:
        for line in input:
            line = line.strip()
            row = [int(value) for value in line]
            grid.append(row)
    return grid


def get_lowest_risk_level():
    grid = parse_input()
    max_x_coord = len(grid[0]) - 1
    max_y_coord = len(grid) - 1
    unvisited_coords = set([(x, y) for x in range(max_x_coord + 1) for y in range(max_y_coord + 1)])

    lowest_risk_path = {}
    previous_coords = {}

    start_coord = (0, 0)
    for coord in unvisited_coords:
        lowest_risk_path[coord] = float('inf')
    lowest_risk_path[start_coord] = 0

    while unvisited_coords:
        current_min_coord = None
        for coord in unvisited_coords:
            if current_min_coord is None:
                current_min_coord = coord
            elif lowest_risk_path[coord] < lowest_risk_path[current_min_coord]:
                current_min_coord = coord

        x, y = current_min_coord
        neighbor_coords = []
        if x != max_x_coord:
            neighbor_coords.append((x+1, y))
        if y != max_y_coord:
            neighbor_coords.append((x, y+1))

        for neighbor in neighbor_coords:
            x, y = neighbor
            tentative_value = lowest_risk_path[current_min_coord] + grid[y][x]
            if tentative_value < lowest_risk_path[neighbor]:
                lowest_risk_path[neighbor] = tentative_value
                previous_coords[neighbor] = current_min_coord

        unvisited_coords.remove(current_min_coord)

    return lowest_risk_path[(max_x_coord, max_y_coord)]


print(get_lowest_risk_level())
