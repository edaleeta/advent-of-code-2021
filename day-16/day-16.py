from collections import deque

FILE_NAME = 'day-16-input.txt'
HEX_TO_BINARY = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def convert_hex_to_bin(hex):
    """Print conversion output for debugging"""
    hex_out = []
    bin_out = []
    for char in hex:
        hex_out.extend(char + ' ' * 3)
        bin_out.extend(HEX_TO_BINARY.get(char))
    print(''.join(hex_out))
    print(''.join(bin_out))


def read_next_hex_to_binary(transmission, binary, length_needed):
    while len(binary) < length_needed:
        hex_char = transmission.popleft()
        # print(f'converting hex char {hex_char} to {HEX_TO_BINARY[hex_char]}')
        binary.extend(HEX_TO_BINARY[hex_char])


def get_next_bits(num_bits, transmission, binary):
    read_next_hex_to_binary(transmission, binary, num_bits)
    return [binary.popleft() for _ in range(num_bits)]


def read_literal(transmission, binary):
    total_bits_read = 0
    bits_to_read = 5
    chars_for_literal = []

    is_reading = True
    while is_reading:
        bits = get_next_bits(bits_to_read, transmission, binary)
        chars_for_literal.extend(bits[1:5])
        total_bits_read += len(bits)
        if bits[0] == '0':
            is_reading = False
    return int(''.join(chars_for_literal), 2), total_bits_read


def apply_operator(type_id, values):
    if type_id == 0:
        return sum(values)
    if type_id == 1:
        prod = 1
        for value in values:
            prod *= value
        return prod
    if type_id == 2:
        return min(values)
    if type_id == 3:
        return max(values)
    if type_id == 5:
        if len(values) != 2:
            raise Exception(f"Invalid number of values, received {values}")
        return 1 if values[0] > values[1] else 0
    if type_id == 6:
        if len(values) != 2:
            raise Exception(f"Invalid number of values, received {values}")
        return 1 if values[0] < values[1] else 0
    if type_id == 7:
        if len(values) != 2:
            raise Exception(f"Invalid number of values, received {values}")
        return 1 if values[0] == values[1] else 0

    raise Exception(f'Invalid type_id {type_id} given.')


def get_transmission_value(input_hex):
    binary = deque()
    transmission = deque(input_hex)
    versions = []

    def get_packet_value_and_bits_read():
        total_bits_read = 0

        if not transmission:
            return None, total_bits_read

        bits_to_read = 6
        bits = get_next_bits(bits_to_read, transmission, binary)

        total_bits_read += bits_to_read
        version = int(''.join(bits[0:3]), 2)
        versions.append(version)
        type_id = int(''.join(bits[3:]), 2)

        if type_id == 4:
            literal, num_bits_read = read_literal(transmission, binary)
            total_bits_read += num_bits_read
            return literal, total_bits_read

        bits_to_read = 1
        length_type_bit = get_next_bits(bits_to_read, transmission, binary)[0]
        total_bits_read += bits_to_read

        subpacket_values = []
        if length_type_bit == '0':
            # Next 15 bits is the total length of subpackets
            bits_to_read = 15
            bits = get_next_bits(bits_to_read, transmission, binary)
            total_bits_read += bits_to_read
            remaining_bits = int(''.join(bits), 2)
            while remaining_bits > 0:
                value, bits_read = get_packet_value_and_bits_read()
                subpacket_values.append(value)
                total_bits_read += bits_read
                remaining_bits -= bits_read
        else:
            # Next 11 bits is the number of subpackets
            bits_to_read = 11
            bits = get_next_bits(bits_to_read, transmission, binary)
            total_bits_read += bits_to_read
            remaining_packets = int(''.join(bits), 2)
            while remaining_packets > 0:
                value, bits_read = get_packet_value_and_bits_read()
                total_bits_read += bits_read
                subpacket_values.append(value)
                remaining_packets -= 1

        result = apply_operator(type_id, subpacket_values)
        return result, total_bits_read

    value_and_bits_read = get_packet_value_and_bits_read()
    
    print(f"Sum of versions: {sum(versions)}")
    return value_and_bits_read


def parse_input():
    with open(FILE_NAME) as input:
        return input.readline().strip()


# test_hex = 'D2FE28'
# test_hex = '38006F45291200'
# test_hex = 'EE00D40C823060'
# test_hex = 'C200B40A82'  # -> 3
# test_hex = '04005AC33890'  # -> 54
# test_hex = '880086C3E88112'  # -> 7
# test_hex = 'CE00C43D881120'  # -> 9
# test_hex = 'D8005AC2A8F0'  # -> 1
# test_hex = '9C005AC2F8F0'  # -> 0
# test_hex = '9C0141080250320F1802104A08'  # -> 1

# print(get_transmission_value(test_hex))

input_hex = parse_input()
print(get_transmission_value(input_hex))
