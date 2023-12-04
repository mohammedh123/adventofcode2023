from dataclasses import dataclass
import re


@dataclass
class Scratchcard:
    num: int
    winning_numbers: set[int]
    player_numbers: list[int]

    def __post_init__(self):
        self.matching_number_count = sum(player_num in self.winning_numbers for player_num in self.player_numbers)


LINE_REGEX = re.compile(r'Card +(?P<card_num>\d+): +(?P<winning_numbers>(?:\d+ *)+) \| +(?P<player_numbers>(?:\d+ *)+)')

card_lookup: dict[int, Scratchcard] = {}
with open('input') as f:
    for line in f.readlines():
        line = line.strip()

        card_data = LINE_REGEX.match(line).groupdict()
        card = Scratchcard(
            num=int(card_data['card_num']),
            winning_numbers=set(map(int, card_data['winning_numbers'].split())),
            player_numbers=list(map(int, card_data['player_numbers'].split())),
        )
        card_lookup[card.num] = card

p1_result = 0
for card in card_lookup.values():
    matching_num_count = card.matching_number_count
    if matching_num_count > 0:
        p1_result += 1 * pow(2, matching_num_count - 1)

print(f'Part 1: {p1_result}')

p2_result = 0
card_counts_to_process = {n: 1 for n in card_lookup.keys()}
for card_num in range(1, len(card_lookup) + 1):
    count = card_counts_to_process[card_num]
    p2_result += count

    card = card_lookup[card_num]
    for copy_card_num in range(card.num, card.num + card.matching_number_count + 1):
        card_counts_to_process[copy_card_num] += count

print(f'Part 2: {p2_result}')