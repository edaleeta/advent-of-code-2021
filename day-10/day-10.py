# FILE_NAME = "day-10-test-input.txt"
FILE_NAME = "day-10-input.txt"

OPEN_CHAR_TO_CLOSING_CHAR = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

CHAR_TO_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def get_first_invalid_char(chars):
    open_chars = []
    for char in chars:
        if char in OPEN_CHAR_TO_CLOSING_CHAR:
            open_chars.append(char)
        elif OPEN_CHAR_TO_CLOSING_CHAR.get(open_chars[-1]) == char:
            open_chars.pop()
        else:
            return char
    return ''


def parse_input():
    chars = "{([(<{}[<>[]}>{[]{[(<()>"
    return [char for char in chars]


def get_syntax_error_score():
    error_score = 0
    with open(FILE_NAME) as input:
        for line in input:
            chars = [char for char in line]
            invalid_char = get_first_invalid_char(chars)
            error_score += CHAR_TO_SCORE.get(invalid_char, 0)
    return error_score


print(get_syntax_error_score())
