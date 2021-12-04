# Part 1

# def get_increase_count():
#     increase_count = 0
#     measurement_a , measurement_b = None, None
#
#     with open('day-01-test-input.txt') as input:
#         for measurement in input:
#             measurement = int(measurement)
#
#             if measurement_a is None:
#                 measurement_a = measurement
#                 continue
#
#             measurement_b = measurement
#
#             if measurement_b > measurement_a:
#                 increase_count += 1
#
#             # Prep window for next check
#             measurement_a = measurement_b
#
#     return increase_count

# print(get_increase_count())

# Part 2

def is_sum_increased(values_a, values_b):
    a = sum(values_a)
    b = sum(values_b)
    return b > a


def scan_window_and_get_increase_count(window_size):
    increase_count = 0

    comp_measurements = []
    max_num_comp_measurements = window_size + 1

    with open('day-01-input.txt') as input:
        for measurement in input:
            measurement = int(measurement)

            if len(comp_measurements) < max_num_comp_measurements:
                comp_measurements.append(measurement)
            else:
                comp_measurements[-1] = measurement

            if len(comp_measurements) < max_num_comp_measurements:
                continue

            first_window = comp_measurements[0:window_size]
            second_window = comp_measurements[1:]

            if is_sum_increased(first_window, second_window):
                increase_count += 1

            # Prep window for next check
            for i in range(window_size):
                comp_measurements[i] = comp_measurements[i+1]

    return increase_count

print(scan_window_and_get_increase_count(1))
print(scan_window_and_get_increase_count(3))
