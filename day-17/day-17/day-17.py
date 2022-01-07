import time


def get_valid_initial_velocities(lower_x, upper_x, lower_y, upper_y, step_limit):
    start = time.time()
    valid_initial_velocities = []

    initial_x_upper = upper_x
    initial_x_lower = 1
    initial_y_lower = lower_y
    initial_y_upper = abs(lower_y)

    for initial_x in range(initial_x_lower, initial_x_upper + 1):
        for initial_y in range(initial_y_lower, initial_y_upper):
            position_x = 0
            position_y = 0
            for step in range(step_limit):
                position_x += 0 if step > initial_x else initial_x - step
                position_y += initial_y - step
                if lower_x <= position_x <= upper_x and lower_y <= position_y <= upper_y:
                    valid_initial_velocities.append((initial_x, initial_y))
                    break
    print(f"took {(time.time() - start) * 1000} ms")
    return valid_initial_velocities


def get_max_y(valid_xy_velocities):
    sorted_velocities = sorted(valid_xy_velocities, key=lambda x: x[1], reverse=True)
    max_initial_y = sorted_velocities[0][1]
    step = 0
    max_position_y = 0
    is_increasing = True
    while is_increasing:
        next_position_y = max_position_y + max_initial_y - step
        if next_position_y < max_position_y:
            is_increasing = False
        else:
            max_position_y = next_position_y
        step += 1
    return max_position_y


# initial_velocities = get_valid_initial_velocities(20, 30, -10, -5, 300)
initial_velocities = get_valid_initial_velocities(156, 202, -110, -69, 300)

print(f"Max y position: {get_max_y(initial_velocities)}")
print(f"Num initial velocities: {len(initial_velocities)}")
