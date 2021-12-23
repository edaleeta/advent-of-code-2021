# FILE_NAME = "day-10-test-input.txt"
FILE_NAME = "day-10-input.txt"

OPEN_CHAR_TO_CLOSING_CHAR = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

CHAR_TO_ERROR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

CHAR_TO_AUTOCOMPLETE_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
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


def get_syntax_error_score():
    error_score = 0
    with open(FILE_NAME) as input:
        for line in input:
            chars = [char for char in line.strip()]
            invalid_char = get_first_invalid_char(chars)
            error_score += CHAR_TO_ERROR_SCORE.get(invalid_char, 0)
    return error_score


def get_completing_sequence(chars):
    open_chars = []
    for char in chars:
        if char in OPEN_CHAR_TO_CLOSING_CHAR:
            open_chars.append(char)
        elif OPEN_CHAR_TO_CLOSING_CHAR.get(open_chars[-1]) == char:
            open_chars.pop()
        else:
            # corrupt sequence
            return []

    if len(open_chars) == 0:
        # complete sequence
        return []

    open_chars.reverse()
    return [OPEN_CHAR_TO_CLOSING_CHAR.get(char) for char in open_chars]


def get_middle_autocomplete_score():
    autocomplete_scores = []
    with open(FILE_NAME) as input:
        for line in input:
            chars = [char for char in line.strip()]
            completing_sequence = get_completing_sequence(chars)
            if completing_sequence:
                score = 0
                for char in completing_sequence:
                    score *= 5
                    score += CHAR_TO_AUTOCOMPLETE_SCORE.get(char)
                autocomplete_scores.append(score)

    autocomplete_scores.sort()
    mid = len(autocomplete_scores) // 2
    return autocomplete_scores[mid]


print(get_syntax_error_score())
print(get_middle_autocomplete_score())
