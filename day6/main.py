from dataclasses import dataclass
from math import prod


@dataclass
class InputData:
    times: list[int]
    distances: list[int]

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            times = list(map(int, f.readline().strip().split()[1:]))
            distances = list(map(int, f.readline().strip().split()[1:]))

            return cls(times, distances)


def get_count_of_winning_durations(race_duration, record_distance):
    count = 0
    for t in range((race_duration + 1) // 2):
        if (race_duration - t) * t > record_distance:
            count += 1

    return count * 2 + (1 if race_duration % 2 == 0 else 0)


input_data = InputData.from_file('input')
winning_ways_counts = [get_count_of_winning_durations(dur, dist) for dur, dist in zip(input_data.times, input_data.distances)]
print(f'Part 1: {prod(winning_ways_counts)}')

p2_duration = int(''.join(map(str, input_data.times)))
p2_distance = int(''.join(map(str, input_data.distances)))
print(f'Part 2: {get_count_of_winning_durations(p2_duration, p2_distance)}')
