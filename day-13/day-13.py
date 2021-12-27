# FILE_NAME = "day-13-test-input.txt"
FILE_NAME = "day-13-input.txt"


def parse_input():
    coords = set()
    instructions = []
    with open(FILE_NAME) as input:
        is_folding_instruction = False
        for line in input:
            line = line.strip()

            if line == "":
                is_folding_instruction = True
                continue
            if is_folding_instruction:
                _, instruction = line.split("fold along ")
                instructions.append(instruction)
            else:
                x, y = line.split(',')
                coords.add((int(x), int(y)))
    return coords, instructions


def get_cutoff_index(target, values):
    cutoff_index = -1
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            cutoff_index = mid
            hi = mid - 1

    return cutoff_index


def get_coords_after_fold(instruction, coords):
    direction, fold_coord = instruction.split('=')
    fold_coord = int(fold_coord)
    is_direction_x = direction == 'x'  # else y direction
    if is_direction_x:
        sorted_coords = sorted(coords, key=lambda x: x[0])
    else:
        sorted_coords = sorted(coords, key=lambda x: x[1])

    i = get_cutoff_index(fold_coord, [coord[0 if is_direction_x else 1] for coord in sorted_coords])
    coords_to_fold = set(sorted_coords[i:])
    coords = coords - coords_to_fold
    folded_coords = set()

    for coord in coords_to_fold:
        x, y = coord
        if is_direction_x:
            distance = x - fold_coord
            folded_x = fold_coord - distance
            folded_coords.add((folded_x, y))
        else:
            distance = y - fold_coord
            folded_y = fold_coord - distance
            folded_coords.add((x, folded_y))

    coords = coords | folded_coords
    return coords


def get_num_dots_visible():
    coords, instructions = parse_input()
    coords = get_coords_after_fold(instructions[0], coords)
    return len(coords)


print(get_num_dots_visible())
