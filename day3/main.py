from collections import defaultdict
from itertools import product, tee


with open('input') as f:
    current_id = 0
    ids_to_numbers = {}
    coordinate_to_id_map = {}
    symbols = []
    part_number_ids = set()

    r = 0
    for line in f.readlines():
        line = line.strip()

        c = 0
        while c < len(line):
            if line[c].isdigit():
                start = c
                while c < len(line) and line[c].isdigit():
                    coordinate_to_id_map[(r, c)] = current_id
                    c += 1
                num = int(line[start:c])
                ids_to_numbers[current_id] = num
                current_id += 1
                c -= 1  # Because we overshot by 1 when finding the number boundaries
            elif line[c] != '.':
                symbols.append((line[c], r, c))

            c += 1

        r += 1

    gear_ratios = []
    for symbol, r, c in symbols:
        adjacent_part_number_ids = set()
        for dr, dc in product(*tee((-1, 0, 1))):
            coords = (r + dr, c + dc)
            if coords in coordinate_to_id_map:
                part_number_ids.add(coordinate_to_id_map[coords])
                adjacent_part_number_ids.add(coordinate_to_id_map[coords])

        if symbol == '*' and len(adjacent_part_number_ids) == 2:
            gear_ratio = 1
            for pnid in adjacent_part_number_ids:
                gear_ratio *= ids_to_numbers[pnid]
            gear_ratios.append(gear_ratio)



print(f'Part 1: {sum(ids_to_numbers[i] for i in part_number_ids)}')
print(f'Part 2: {sum(gear_ratios)}')