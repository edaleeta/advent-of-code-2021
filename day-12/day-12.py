# FILE_NAME = "day-12-test-input.txt"
# FILE_NAME = "day-12-test-input-long.txt"
FILE_NAME = "day-12-input.txt"


class CaveSystem:
    def __init__(self):
        self.caves = {}

    def add_cave_connection(self, cave_connection):
        # cave_connection format: <cave>-<cave>
        cave_a, cave_b = cave_connection.split('-')
        if cave_a not in self.caves:
            self.caves[cave_a] = set()
        if cave_b not in self.caves:
            self.caves[cave_b] = set()

        self.caves[cave_a].add(cave_b)
        self.caves[cave_b].add(cave_a)

    def find_all_paths(self):
        paths = []

        def visit_cave(cave, path, visited):
            path.append(cave)
            # may only visit small caves once
            if cave.islower():
                visited.add(cave)

            if cave == 'end':
                paths.append(path)
                return

            for next_cave in self.caves[cave]:
                if next_cave not in visited:
                    visit_cave(next_cave, path[:], visited.copy())

        visit_cave('start', [], set())
        return paths


def build_cave_system():
    cave_system = CaveSystem()

    with open(FILE_NAME) as input:
        for line in input:
            line = line.strip()
            cave_system.add_cave_connection(line)
    return cave_system


def get_num_paths_in_cave_system(cave_system):
    paths = cave_system.find_all_paths()
    return len(paths)


cave_system = build_cave_system()
print(get_num_paths_in_cave_system(cave_system))
