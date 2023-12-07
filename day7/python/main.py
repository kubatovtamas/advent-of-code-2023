import sys
from collections import Counter
from enum import Enum, auto
from functools import cmp_to_key
from typing import Iterator, Self

from sortedcontainers import SortedList


class HandType(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


class Card:
    @classmethod
    def symbol_to_value(cls, sym: str, part: int = 1) -> int:
        sym_to_val: dict[str, int] = {
            "A": 14,  # Ace
            "K": 13,  # King
            "Q": 12,  # Queen
            "T": 10,  # Ten
        }

        if sym == "J":
            if part == 1:
                return 11
            else:
                return 1

        if sym in sym_to_val:
            return sym_to_val[sym]

        return int(sym)

    def __init__(self, symbol: str, part: int = 1) -> None:
        self.symbol: str = symbol
        self.value: int = self.symbol_to_value(symbol, part)

    def __repr__(self) -> str:
        return self.symbol


class Hand:
    @classmethod
    def calculate_hand_type(cls, cards: list[Card], part: int) -> HandType:
        def _transform_jokers(cards: list[Card]) -> None:
            """Transform the Joker symbols to the most common other symbol, or Aces if cards are all Jokers."""
            occurrence_counter = Counter(c.symbol for c in cards if c.symbol != "J")

            if not occurrence_counter:
                to_replace_sym = "A"
            else:
                to_replace_sym = occurrence_counter.most_common(1)[0][0]

            for c in cards:
                if c.symbol == "J":
                    c.symbol = to_replace_sym

        if part == 2:
            _transform_jokers(cards)

        occurrence_counter = Counter(c.symbol for c in cards)
        occurrences = sorted(occurrence_counter.values())

        match occurrences:
            case [5]:
                return HandType.FIVE_OF_A_KIND
            case [1, 4]:
                return HandType.FOUR_OF_A_KIND
            case [2, 3]:
                return HandType.FULL_HOUSE
            case [1, 1, 3]:
                return HandType.THREE_OF_A_KIND
            case [1, 2, 2]:
                return HandType.TWO_PAIR
            case [1, 1, 1, 2]:
                return HandType.ONE_PAIR
            case _:
                return HandType.HIGH_CARD

    @classmethod
    def parse_line_to_hand(cls, line: str, part: int = 1) -> Self:
        card_str, bid_str = line.split()
        cards = [Card(c, part) for c in card_str]
        bid = int(bid_str)

        return cls(cards, bid, part)

    @classmethod
    def compare_hands(cls, a: Self, b: Self) -> int:
        """Comparator function for two Hand objects.

        Compares based on HandType, if they are the same, then the first high card in order wins.
        """
        if a.type.value < b.type.value:
            return -1
        elif a.type.value > b.type.value:
            return 1
        else:
            for ca, cb in zip(a.cards, b.cards):
                if ca.value < cb.value:
                    return -1
                elif ca.value > cb.value:
                    return 1
            return 0

    def __init__(self, cards: list[Card], bid: int, part: int = 1) -> None:
        self.cards = cards
        self.bid = bid
        self.type = self.calculate_hand_type(cards, part)

    def __repr__(self) -> str:
        return f"Hand({self.cards} ({self.type.name}), ${self.bid})"


def get_args() -> tuple[int, str]:
    if len(sys.argv) != 3:
        print("Usage: python main.py <1 or 2> <example or full>")
        sys.exit(1)

    part = int(sys.argv[1])
    if part not in (1, 2):
        print("First argument must be either 1 or 2")
        sys.exit(1)

    mode = sys.argv[2]

    return part, mode


def read_input(name: str) -> Iterator[str]:
    with open(f"../input/{name}", "r") as f:
        for line in f:
            yield line.rstrip()


def main():
    part, mode = get_args()

    if part == 1:
        solution = 0
        sorted_list = SortedList(key=cmp_to_key(Hand.compare_hands))

        for line in read_input(mode):
            hand = Hand.parse_line_to_hand(line)
            sorted_list.add(hand)

        for rank, hand in enumerate(sorted_list, start=1):
            solution += rank * hand.bid

        print("SOLUTION:", solution)
        assert solution == 251216224

    if part == 2:
        solution = 0
        sorted_list = SortedList(key=cmp_to_key(Hand.compare_hands))

        for line in read_input(mode):
            hand = Hand.parse_line_to_hand(line, part=2)
            sorted_list.add(hand)

        for rank, hand in enumerate(sorted_list, start=1):
            solution += rank * hand.bid

        print("SOLUTION:", solution)
        assert solution == 250825971


if __name__ == "__main__":
    main()
