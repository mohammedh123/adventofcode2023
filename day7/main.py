from collections import Counter
from dataclasses import dataclass, field
from enum import IntEnum, auto


class HandType(IntEnum):
    FIVE_OF_A_KIND = auto()
    FOUR_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    THREE_OF_A_KIND = auto()
    TWO_PAIR = auto()
    ONE_PAIR = auto()
    HIGH_CARD = auto()


@dataclass(order=True)
class CardHand:
    sort_index: int = field(init=False, repr=False)
    cards: str
    bid: int

    def __post_init__(self):
        self.hand_type_p1 = CardHand.get_hand_type_p1(self.cards)
        self.hand_type_p2 = CardHand.get_hand_type_p2(self.cards)

    def get_sort_index_for_p1(self):
        return (self.hand_type_p1, *self.get_card_rankings('AKQJT98765432'))

    def get_sort_index_for_p2(self):
        return (self.hand_type_p2, *self.get_card_rankings('AKQT98765432J'))

    @staticmethod
    def get_hand_type_p1(cards: str) -> HandType:
        assert len(cards) == 5

        card_counts = Counter(cards)
        distinct_card_types = list(set(cards))

        if len(distinct_card_types) == 1:
            return HandType.FIVE_OF_A_KIND
        elif len(distinct_card_types) == 2:
            if card_counts[distinct_card_types[0]] in (1, 4):
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.FULL_HOUSE
        elif len(distinct_card_types) == 3:
            if any(c == 3 for c in card_counts.values()):
                return HandType.THREE_OF_A_KIND
            elif any(c == 2 for c in card_counts.values()):
                return HandType.TWO_PAIR
        elif len(distinct_card_types) == 4:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    @staticmethod
    def get_hand_type_p2(cards: str):
        card_counts = Counter(cards)

        if card_counts.get('J', 0) > 0:
            del card_counts['J']

            most_freq_card, _ = (card_counts.most_common(1) or [('A', 0)])[0]

            new_hand = cards.replace('J', most_freq_card)
            return CardHand.get_hand_type_p1(new_hand)

        return CardHand.get_hand_type_p1(cards)

    def get_card_rankings(self, ranking_str):
        return tuple(ranking_str.index(c) for c in self.cards)


@dataclass
class InputData:
    hands: list[CardHand]

    @classmethod
    def from_filename(cls, filename) -> 'InputData':
        with open(filename) as f:
            hands = []
            for line in f.readlines():
                cards, bid_str = line.strip().split()
                hands.append(CardHand(cards, int(bid_str)))

            return cls(hands)


def calculate_total_winnings(hands: list[CardHand]) -> int:
    rank = 1
    total_winnings = 0
    for hand in input.hands:
        total_winnings += rank * hand.bid
        rank += 1

    return total_winnings


input = InputData.from_filename('input')

input.hands.sort(reverse=True, key=lambda h: h.get_sort_index_for_p1())
print(f'Part 1: {calculate_total_winnings(input.hands)}')

input.hands.sort(reverse=True, key=lambda h: h.get_sort_index_for_p2())
print(f'Part 2: {calculate_total_winnings(input.hands)}')