# no valid answer until at least 5th element
# only need to check the row / column that the new digit is part of

# how to locate number...
# processing into BingoCard class, dict will track coordinates

# FILE_NAME = 'day-04-test-input.txt'
FILE_NAME = 'day-04-input.txt'


class BingoCard:
    SIZE = 5

    def __init__(self):
        self.number_to_location = {}
        card = []
        for i in range(self.SIZE):
            row = [None] * self.SIZE
            card.append(row)
        self.card = card

    def print_marks(self):
        for row in self.card:
            print(row)
        print("\n\n")

    def populate_number(self, number, row, col):
        self.number_to_location[number] = (row, col)

    def check_number(self, number):
        if number not in self.number_to_location:
            # Number is not on the card
            return -1

        # Add mark
        row, col = self.number_to_location[number]
        self.card[row][col] = True

        # Remove number from dict
        del self.number_to_location[number]

        # Check row / col for bingo
        card_row = self.card[row]
        card_col = [self.card[i][col] for i in range(self.SIZE)]

        if all(card_row) or all(card_col):
            # Bingo, compute score
            return sum(self.number_to_location) * number

        return -1


def parse_input():
    called_numbers = None
    cards = []
    row = 0
    with open(FILE_NAME) as input:
        called_numbers = input.readline().rstrip()
        called_numbers = [int(number) for number in called_numbers.split(",")]

        card = BingoCard()

        for line in input:
            line = line.strip()
            if not line:
                continue

            numbers = [int(number) for number in line.split()]
            for col, number in enumerate(numbers):
                card.populate_number(number, row, col)

            row = (row + 1) % card.SIZE
            if row == 0:
                # Current card is done being populated; save and start a new one
                cards.append(card)
                card = BingoCard()

    return called_numbers, cards


def play_bingo():
    called_numbers, cards = parse_input()
    for called_number in called_numbers:
        for card in cards:
            score = card.check_number(called_number)
            if score > 0:
                return score

    return 0


print(play_bingo())
