# FILE_NAME = 'day-04-test-short-input.txt'
# FILE_NAME = 'day-04-test-input.txt'
FILE_NAME = 'day-04-input.txt'


class BingoCard:
    SIZE = 5

    def __init__(self):
        self.numbers = []

    def get_winning_round(self, called_number_to_round):
        winning_rounds = []

        def eval_called_rounds(rounds):
            if all([number >= 0 for number in rounds]):
                # All valid rounds, save round
                winning_rounds.append(max(rounds))

        for i in range(self.SIZE):
            column_called = [
                called_number_to_round.get(self.numbers[i + (j * self.SIZE)], -1) for j in range(self.SIZE)
            ]

            row_start_index = i * self.SIZE
            row_called = [
                called_number_to_round.get(number)
                for number in self.numbers[row_start_index:row_start_index + self.SIZE]
            ]

            eval_called_rounds(column_called)
            eval_called_rounds(row_called)

        if len(winning_rounds) == 0:
            # Card can't win
            return -1

        return min(winning_rounds)

    def get_unmarked_numbers_after_round(self, round, called_numbers):
        card_numbers = set(self.numbers)
        called_numbers = set(called_numbers[:round+1])
        return card_numbers - called_numbers


def parse_input():
    cards = []
    with open(FILE_NAME) as input:
        called_numbers = input.readline().rstrip()
        called_numbers = [int(number) for number in called_numbers.split(",")]
        called_number_to_round = {number: i for i, number in enumerate(called_numbers)}

        card = BingoCard()
        i = 0
        for line in input:
            line = line.strip()
            if not line:
                continue

            numbers = [int(number) for number in line.split()]
            card.numbers.extend(numbers)

            i = (i + 1) % card.SIZE
            if i == 0:
                # Current card is done being populated; save and start a new one
                cards.append(card)
                card = BingoCard()

    return called_numbers, called_number_to_round, cards


def eval_bingo(is_last_win=False):
    called_numbers, called_number_to_round, cards = parse_input()
    winning_rounds = [card.get_winning_round(called_number_to_round) for card in cards]

    eval_cards = max if is_last_win else min

    winning_card, winning_round = eval_cards(
        [(cards[i], round) for i, round in enumerate(winning_rounds) if round > -1],
        key=lambda x: x[1]
    )

    return sum(
        winning_card.get_unmarked_numbers_after_round(winning_round, called_numbers)
    ) * called_numbers[winning_round]


print(eval_bingo())
print(eval_bingo(is_last_win=True))
