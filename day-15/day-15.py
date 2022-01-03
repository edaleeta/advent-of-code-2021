import time
import heapq

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


def get_lowest_risk_level_dijkstra():
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


class PriorityQueue:
    def __init__(self):
        self.elements = []

    @property
    def is_empty(self):
        return not self.elements

    def put(self, priority, item):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def get_lowest_risk_level_astar():
    grid = parse_input()
    max_x_coord = len(grid[0]) - 1
    max_y_coord = len(grid) - 1
    start_coord = (0, 0)
    end_coord = (max_x_coord, max_y_coord)

    open_nodes = PriorityQueue()
    came_from = {start_coord: None}
    risk_so_far = {start_coord: 0}
    open_nodes.put(0, start_coord)

    while not open_nodes.is_empty:
        current_coord = open_nodes.get()

        if current_coord == end_coord:
            break

        x, y = current_coord
        next_coords = []
        if x != max_x_coord:
            next_coords.append((x+1, y))
        if y != max_y_coord:
            next_coords.append((x, y+1))

        for next_coord in next_coords:
            x, y = next_coord
            new_risk = risk_so_far[current_coord] + grid[y][x]
            if next_coord not in risk_so_far or new_risk < risk_so_far[next_coord]:
                risk_so_far[next_coord] = new_risk
                # heuristic = Manhattan distance to end node, minimum risk level = 1
                priority = new_risk + abs(next_coord[0] - end_coord[0]) + abs(next_coord[1] - end_coord[1])
                open_nodes.put(priority, next_coord)
                came_from[next_coord] = current_coord

    return risk_so_far[end_coord]


def run_timed_function(func):
    start_time = time.time()
    print(func())
    print(f'runtime: {(time.time() - start_time) * 1000} ms')


run_timed_function(get_lowest_risk_level_dijkstra)
run_timed_function(get_lowest_risk_level_astar)
