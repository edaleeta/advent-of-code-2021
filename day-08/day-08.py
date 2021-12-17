# FILE_NAME = "day-08-test-input.txt"
FILE_NAME = "day-08-input.txt"

num_segments_to_digits = {
    2: {1},
    3: {7},
    4: {4},
    5: {2, 3, 5},
    6: {0, 6, 9},
    7: {8},
}

easy_output_lengths = {2, 3, 4, 7}


def get_easy_output_count():
    output_lights = []

    with open(FILE_NAME) as input:
        for line in input:
            line = line.rstrip()
            signal_patterns, output = line.split("|")

            output = output.strip()
            output_lights.extend(output.split())

    print(output_lights)

    easy_output_count = 0
    for light in output_lights:
        if len(light) in easy_output_lengths:
            easy_output_count += 1

    return easy_output_count


print(get_easy_output_count())
