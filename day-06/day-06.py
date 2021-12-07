# FILE_NAME = "day-06-test-input.txt"
FILE_NAME = "day-06-input.txt"

def parse_input():
    with open(FILE_NAME) as input:
        line = input.readline().rstrip()
        return [int(timer) for timer in line.split(",")]


def simulate(timers, num_days):
    total = len(timers)
    # A fish takes 7 days to produce a new fish, unless it is its first cycle, which takes 9
    # Reduce timers to timer_to_frequency, timers can only be ints [0, 8]
    timer_to_frequency = {i: 0 for i in range(9)}
    change_map = {i: 0 for i in range(9)}
    for timer in timers:
        timer_to_frequency[timer] = timer_to_frequency.get(timer, 0) + 1

    for i in range(num_days):
        for j in range(9):
            timer_count = timer_to_frequency[j]
            change_map[j] -= timer_count
            if j > 0 and timer_count > 0:
                change_map[j-1] += timer_count
            if j == 0:
                change_map[6] += timer_count
                change_map[8] += timer_count
                total += timer_count

        for timer, change in change_map.items():
            timer_to_frequency[timer] += change
            change_map[timer] = 0

    return total


def get_count_lanternfish_after_days(num_days):
    lanternfish_timers = parse_input()
    return simulate(lanternfish_timers, num_days)


print(get_count_lanternfish_after_days(80))
