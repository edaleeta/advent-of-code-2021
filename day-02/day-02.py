
def get_x_y_position(mode=1):
    x, y, aim = 0, 0, 0
    with open('day-02-input.txt') as input:
        for instruction in input:
            direction, amount = instruction.split()
            amount = int(amount)

            if direction == 'forward':
                x += amount
                if mode != 1:
                    y += aim * amount

            elif direction == 'down':
                if mode == 1:
                    y += amount
                else:
                    aim += amount

            elif direction == 'up':
                if mode == 1:
                    y -= amount
                else:
                    aim -= amount

            else:
                print(f'Unknown direction: {direction}')

    print(f"x: {x}, y: {y}")
    return x, y


def get_position_multiplied(mode=1):
    x, y = get_x_y_position(mode)
    return x * y


print(get_position_multiplied(mode=1))
print(get_position_multiplied(mode=2))
