# FILE_NAME = "day-11-test-input-short.txt"
# FILE_NAME = "day-11-test-input.txt"
FILE_NAME = "day-11-input.txt"

FLASH_THRESHOLD = 9


class Octopus:
    def __init__(self, energy):
        self.energy = energy
        self.has_flashed = False

    def __repr__(self):
        return f"{self.energy:2}"


def parse_input_to_oct_map():
    with open(FILE_NAME) as input:
        oct_map = []
        for line in input:
            line = line.strip()
            octopuses = [Octopus(int(e)) for e in line]
            oct_map.append(octopuses)
    return oct_map


def apply_step(oct_map):
    def handle_flash(coords_to_increase_energy, num_flashes):
        next_coords = []
        # Increment energy levels
        for i, j in coords_to_increase_energy:
            current_oct = oct_map[i][j]
            current_oct.energy += 1
            if current_oct.energy > FLASH_THRESHOLD and not current_oct.has_flashed:
                num_flashes += 1
                current_oct.has_flashed = True
                # create adjacent coords to update
                # left
                if j != 0:
                    next_coords.append((i, j-1))
                # left-top i == 0 or j == 0
                if i != 0 and j != 0:
                    next_coords.append((i-1, j-1))
                # top
                if i != 0:
                    next_coords.append((i-1, j))
                # top-right
                if i != 0 and j != len(oct_map[i])-1:
                    next_coords.append((i-1, j+1))
                # right
                if j != len(oct_map[i])-1:
                    next_coords.append((i, j+1))
                # right-bot
                if i != len(oct_map)-1 and j != len(oct_map[i])-1:
                    next_coords.append((i+1, j+1))
                # bot
                if i != len(oct_map)-1:
                    next_coords.append((i+1, j))
                # bot-left
                if i != len(oct_map)-1 and j != 0:
                    next_coords.append((i+1, j-1))

        if next_coords:
            return handle_flash(next_coords, num_flashes)
        return num_flashes

    coords_to_process = [(i, j) for i in range(len(oct_map)) for j in range(len(oct_map[i]))]
    total_flashed = handle_flash(coords_to_process, 0)

    # finish step by resetting energy
    for i in range(len(oct_map)):
        for j in range(len(oct_map[i])):
            current_oct = oct_map[i][j]
            if current_oct.energy > FLASH_THRESHOLD:
                current_oct.energy = 0
                current_oct.has_flashed = False

    return total_flashed


def get_flash_count_after_n_steps(n):
    num_flashes = 0
    oct_map = parse_input_to_oct_map()
    for i in range(n):
        num_flashes += apply_step(oct_map)
    return num_flashes


def check_is_synced(oct_map):
    for row in oct_map:
        if not all([octopus.energy == 0 for octopus in row]):
            return False
    return True


def get_step_synced():
    oct_map = parse_input_to_oct_map()
    is_synced = False
    n = 0
    while not is_synced:
        n += 1
        apply_step(oct_map)
        is_synced = check_is_synced(oct_map)
    return n


print(get_flash_count_after_n_steps(100))
print(get_step_synced())
