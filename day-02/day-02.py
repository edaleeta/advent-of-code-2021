
def get_x_y_position():
    x, y = 0, 0
    with open('day-02-input.txt') as input:
        for instruction in input:
            direction, distance = instruction.split()
            distance = int(distance)

            if direction == 'forward':
                x += distance
            elif direction == 'down':
                y += distance
            elif direction == 'up':
                y -= distance
            else:
                print(f'Unknown direction: {direction}')

    print(f"x: {x}, y: {y}")
    return x, y

def get_position_multiplied():
    x, y = get_x_y_position()
    return x * y

print(get_position_multiplied())
