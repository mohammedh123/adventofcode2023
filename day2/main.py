from collections import defaultdict
from math import prod


P1_CUBES_REQUIRED = {'red': 12, 'green': 13, 'blue': 14}

p1_result = 0
p2_result = 0
with open('input') as f:
    for line in f.readlines():
        game_str, items = [s.strip() for s in line.strip().split(':')]
        game_id = int(game_str.split()[1])
        min_cubes_required = defaultdict(int)

        for cube_set in (s.split(', ') for s in items.split('; ')):
            for s in cube_set:
                count, color = s.split()
                min_cubes_required[color] = max(min_cubes_required[color], int(count))

        is_game_possible_with_p1_requirements = not any(
            min_cubes_required[color] > available_count
            for color, available_count
            in P1_CUBES_REQUIRED.items()
        )

        if is_game_possible_with_p1_requirements:
            p1_result += game_id

        p2_result += prod(min_cubes_required.values())


print(f'Part 1: {p1_result}')
print(f'Part 2: {p2_result}')