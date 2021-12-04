def convert_binary_to_decimal(binary_chars):
    return int(''.join(binary_chars), 2)


def get_epsilon_and_gamma():
    count_zeroes = []
    count_ones = []
    with open('day-03-input.txt') as input:
        for bnumber in input:
            bnumber = bnumber[:-1]  # Omit return char
            # First line, init values
            if not count_zeroes and not count_ones:
                count_zeroes = [0] * len(bnumber)
                count_ones = [0] * len(bnumber)

            for i, digit in enumerate(bnumber):
                if digit == '0':
                    count_zeroes[i] = count_zeroes[i] + 1
                else:
                    count_ones[i] = count_ones[i] + 1

    epsilon_binary, gamma_binary = [], []

    for count_zero, count_one in zip(count_zeroes, count_ones):
        if count_zero > count_one:
            epsilon_binary.append('0')
            gamma_binary.append('1')
        else:
            epsilon_binary.append('1')
            gamma_binary.append('0')

    return convert_binary_to_decimal(epsilon_binary), convert_binary_to_decimal(gamma_binary)


def get_power_consumption():
    epsilon, gamma = get_epsilon_and_gamma()
    print(f"epsilon: {epsilon}, gamma: {gamma}")
    return epsilon * gamma


print(get_power_consumption())
