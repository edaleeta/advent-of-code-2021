# FILE_NAME = "day-08-test-short-input.txt"
# FILE_NAME = "day-08-test-input.txt"
FILE_NAME = "day-08-input.txt"

NUM_SEGMENTS_TO_DIGITS = {
    2: {1},
    3: {7},
    4: {4},
    5: {2, 3, 5},
    6: {0, 6, 9},
    7: {8},
}

EASY_OUTPUT_LENGTHS = {2, 3, 4, 7}

BINARY_TO_NUMBER = {
    0b1111110: 0,
    0b0110000: 1,
    0b1101101: 2,
    0b1111001: 3,
    0b0110011: 4,
    0b1011011: 5,
    0b1011111: 6,
    0b1110000: 7,
    0b1111111: 8,
    0b1111011: 9,
}

POSITION_TO_BINARY = {
    'a': 0b1000000,
    'b': 0b0100000,
    'c': 0b0010000,
    'd': 0b0001000,
    'e': 0b0000100,
    'f': 0b0000010,
    'g': 0b0000001,
}

BINARY_TO_POSITION = {
    0b1000000: 'a',
    0b0100000: 'b',
    0b0010000: 'c',
    0b0001000: 'd',
    0b0000100: 'e',
    0b0000010: 'f',
    0b0000001: 'g',
}


def get_easy_output_count():
    output_lights = []

    with open(FILE_NAME) as input:
        for line in input:
            line = line.rstrip()
            signal_patterns, output = line.split("|")

            output = output.strip()
            output_lights.extend(output.split())

    easy_output_count = 0
    for light in output_lights:
        if len(light) in EASY_OUTPUT_LENGTHS:
            easy_output_count += 1

    return easy_output_count


class Decoder:
    """
    Process a series of encoded segment signals to decode to 'true' positions/segments
    Decoded segments are oriented as follows:
     aaaa
    f    b
    f    b
     gggg
    e    c
    e    c
     dddd
    """
    def __init__(self):
        self.segment_map = {}

    def __repr__(self):
        reverse_segment_map = {value: key for key, value in self.segment_map.items()}
        default_char = "-"
        top_char = reverse_segment_map.get('a', default_char)
        top_right_char = reverse_segment_map.get('b', default_char)
        bot_right_char = reverse_segment_map.get('c', default_char)
        bot_char = reverse_segment_map.get('d', default_char)
        bot_left_char = reverse_segment_map.get('e', default_char)
        top_left_char = reverse_segment_map.get('f', default_char)
        mid_char = reverse_segment_map.get('g', default_char)
        return f"""
{" "}{top_char * 4}{" "}
{top_left_char}{" " * 4}{top_right_char}
{top_left_char}{" " * 4}{top_right_char}
{" "}{mid_char * 4}{" "}
{bot_left_char}{" " * 4}{bot_right_char}
{bot_left_char}{" " * 4}{bot_right_char}
{" "}{bot_char * 4}{" "}
"""

    @property
    def found_segments(self):
        return set(self.segment_map)

    def decode_signal(self, signal):
        actual_positions = [self.segment_map.get(char) for char in signal]
        binary_positions = [POSITION_TO_BINARY.get(position) for position in actual_positions]
        binary_number = 0b0000000
        for binary_position in binary_positions:
            binary_number = binary_number | binary_position
        return BINARY_TO_NUMBER.get(binary_number)

    def create_decoder(self, signals):
        num_segments_to_segments = {}
        number_to_segments = {}

        # Scan for easy numbers
        for signal in signals:
            num_segments = len(signal)
            possible_numbers = NUM_SEGMENTS_TO_DIGITS[num_segments]
            segments = {char for char in signal}
            if len(possible_numbers) == 1:
                # Easy number!
                number, = possible_numbers
                number_to_segments[number] = segments
            else:
                # Multiple possibilities
                if num_segments not in num_segments_to_segments:
                    num_segments_to_segments[num_segments] = []
                num_segments_to_segments[num_segments].append(segments)

        # 'a' = {7 segments} - {1 segments}
        a_segments = number_to_segments[7] - number_to_segments[1]
        if len(a_segments) != 1:
            raise Exception(f"Too many segments found: {a_segments}, expected one")
        self.segment_map[next(iter(a_segments))] = 'a'

        # 'b' = {1 segments} - {6 segments}
        for i, segments in enumerate(num_segments_to_segments[6]):
            b_segments = number_to_segments[1] - segments
            if len(b_segments) == 1:
                # Found segments for 6
                number_to_segments[6] = segments
                self.segment_map[next(iter(b_segments))] = 'b'
                del num_segments_to_segments[6][i]
                break

        # 'c' = {1 segments} - {found segments}
        c_segments = number_to_segments[1] - self.found_segments
        if len(a_segments) != 1:
            raise Exception(f"Too many segments found: {c_segments}, expected one")
        self.segment_map[next(iter(c_segments))] = 'c'

        # Only 0 and 9 left in num_segments_to_segments[6]
        # g is not in 0, but is in 9
        # e is not in 9, but is in 0
        segments_x = num_segments_to_segments[6][0]
        segments_y = num_segments_to_segments[6][1]
        sym_diff = segments_x ^ segments_y
        segment = sym_diff.pop()
        if segment in number_to_segments[4]:
            # segment is 'g', other is 'e'
            self.segment_map[segment] = 'g'
            segment = sym_diff.pop()
            self.segment_map[segment] = 'e'
        else:
            # segment is 'e', other is 'g'
            self.segment_map[segment] = 'e'
            segment = sym_diff.pop()
            self.segment_map[segment] = 'g'

        # f is {4 segments} - {found segments}
        f_segments = number_to_segments[4] - self.found_segments
        if len(f_segments) != 1:
            raise Exception(f"Too many segments found: {f_segments}, expected one")
        self.segment_map[next(iter(f_segments))] = 'f'

        # d is {8 segments} - {found segments}
        d_segments = number_to_segments[8] - self.found_segments
        if len(d_segments) != 1:
            raise Exception(f"Too many segments found: {d_segments}, expected one")
        self.segment_map[next(iter(d_segments))] = 'd'


def create_value_from_numbers(numbers):
    value = 0
    for i in range(len(numbers)-1, -1, -1):
        # also count from 0 -> last index
        j = len(numbers) - 1 - i
        value += numbers[j] * 10 ** i
    return value


def get_output_sum():
    all_signal_patterns = []
    all_output_signals = []
    sum_of_output = 0
    with open(FILE_NAME) as input:
        for line in input:
            line = line.rstrip()
            signal_patterns, output = line.split("|")
            signal_patterns = signal_patterns.strip()
            output = output.strip()
            all_signal_patterns.append(signal_patterns)
            all_output_signals.append(output)

    for signal_pattern, output_signal in zip(all_signal_patterns, all_output_signals):
        signals = signal_pattern.split()
        decoder = Decoder()
        decoder.create_decoder(signals)

        output_signals = output_signal.split()
        output_numbers = [decoder.decode_signal(signal) for signal in output_signals]
        sum_of_output += create_value_from_numbers(output_numbers)

    return sum_of_output


print(get_easy_output_count())
print(get_output_sum())
