from enum import Enum
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


class ReadMode(Enum):
    VERSION = 0
    TYPE_ID = 1
    LITERAL = 2
    OPERATOR = 3
    LENGTH_TYPE_ID = 4


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


def decode_packets(input_hex):
    version_numbers = []
    binary = deque()
    transmission = deque(input_hex)

    def parse_packets(transmission, binary, num_bits=None, num_packets=None):
        read_mode = ReadMode.VERSION
        while transmission:

            if num_bits == 0:
                break

            if num_packets == 0:
                break

            if read_mode == ReadMode.VERSION:
                bits_to_read = 3
                bits = get_next_bits(bits_to_read, transmission, binary)
                version_number = int(''.join(bits), 2)
                version_numbers.append(version_number)
                read_mode = ReadMode.TYPE_ID
                if num_bits is not None:
                    num_bits -= bits_to_read
                continue
            elif read_mode == ReadMode.TYPE_ID:
                bits_to_read = 3
                bits = get_next_bits(bits_to_read, transmission, binary)
                type_id = int(''.join(bits), 2)
                if type_id == 4:
                    read_mode = ReadMode.LITERAL
                else:
                    read_mode = ReadMode.OPERATOR
                if num_bits is not None:
                    num_bits -= bits_to_read
                continue
            elif read_mode == ReadMode.LITERAL:
                literal, total_bits_read = read_literal(transmission, binary)
                read_mode = ReadMode.VERSION
                if num_bits is not None:
                    num_bits -= total_bits_read
                if num_packets is not None:
                    num_packets -= 1
                continue
            elif read_mode == ReadMode.OPERATOR:
                bits_to_read = 1
                read_next_hex_to_binary(transmission, binary, bits_to_read)
                type_id_bit = binary.popleft()
                if type_id_bit == '0':
                    # Next 15 bits is the total length of subpackets
                    bits_to_read = 15
                    bits = get_next_bits(bits_to_read, transmission, binary)
                    subpacket_length = int(''.join(bits), 2)
                    parse_packets(transmission, binary, num_bits=subpacket_length)
                else:
                    # Next 11 bits is the number of subpackets
                    bits_to_read = 11
                    bits = get_next_bits(bits_to_read, transmission, binary)
                    num_subpackets = int(''.join(bits), 2)
                    parse_packets(transmission, binary, num_packets=num_subpackets)
                read_mode = ReadMode.VERSION

    parse_packets(transmission, binary)
    print(f"Version numbers: {version_numbers}")
    print(f"Sum of version numbers: {sum(version_numbers)}")


def parse_input():
    with open(FILE_NAME) as input:
        return input.readline().strip()


# test_hex = 'D2FE28'
# test_hex = '38006F45291200'
test_hex = 'EE00D40C823060'

input_hex = parse_input()
decode_packets(input_hex)

