from dataclasses import dataclass, field


@dataclass(order=True)
class Interval:
    sort_index: int = field(init=False, repr=False)
    start: int
    end: int

    def __post_init__(self):
        self.sort_index = self.start

    def intersects(self, other: 'Interval'):
        return (
            self.start <= other.start <= self.end or
            self.start <= other.end <= self.end or
            other.start <= self.start <= other.end or
            other.start <= self.end <= other.end
        )

    def is_contained_by(self, other: 'Interval'):
        return other.start <= self.start <= other.end and other.start <= self.end <= other.end

    def __repr__(self):
        return f'[{self.start}, {self.end}]'


@dataclass
class CategoryRange:
    intervals: list[tuple[Interval, int]]

    @classmethod
    def from_list_of_intervals(cls, intervals):
        _intervals = []

        for dst_start, src_start, range_length in intervals:
            _intervals.append((Interval(src_start, src_start + range_length - 1), dst_start - src_start))

        _intervals.sort()
        return cls(_intervals)


@dataclass
class SeedCategoryCondenser:
    category_maps: list[CategoryRange]

    def convert_seed_ranges_to_location_ranges(self, seed_ranges: list[Interval]):
        # Intersect and offset intervals as we traverse the category maps
        src_intervals = seed_ranges
        for category in self.category_maps:

            for category_interval, _ in category.intervals:
                src_intervals.sort()
                dst_intervals = []

                for src_interval in src_intervals:
                    # First, split apart all current source intervals so that they intersect with at most 1 category interval
                    # Several cases:
                    # - If this interval is completely contained by the category interval, do nothing
                    #   e.g.: 50,55 vs 45,60 -> 50,55
                    # - If this interval intersects the category interval (but not completely contained), split the source interval
                    #   into 2 intervals
                    #   e.g.: 50,55 vs 53,56 -> 50,53 + 53,55
                    # - If this interval completely contains the category interval, split the source interval into up to 3 intervals
                    #   e.g.: 50,55 vs 52,55 -> 50,51 + 52,55
                    #         50,55 vs 53,54 -> 50,52 + 53,54 + 55,55
                    if not src_interval.intersects(category_interval):
                        dst_intervals.append(src_interval)

                    else:
                        if src_interval.is_contained_by(category_interval):
                            dst_intervals.append(src_interval)

                        elif category_interval.is_contained_by(src_interval):
                            # If they share an edge, split the source interval according to the category interval
                            shared_start_edge = category_interval.start in (src_interval.start, src_interval.end)
                            shared_end_edge = category_interval.end in (src_interval.start, src_interval.end)
                            if shared_start_edge or shared_end_edge:
                                dst_intervals.append(category_interval)

                                if shared_start_edge:
                                    # e.g.: 50,55 50,51 -> 50,51 + 52,55
                                    dst_intervals.append(Interval(category_interval.end + 1, src_interval.end))
                                else:
                                    # e.g.: 50,55 54,55 -> 50,53 + 54,55
                                    dst_intervals.append(Interval(src_interval.start, category_interval.start - 1))
                            else:
                                dst_intervals.append(Interval(src_interval.start, category_interval.start - 1))
                                dst_intervals.append(category_interval)
                                dst_intervals.append(Interval(category_interval.end + 1, src_interval.end))

                        else:  # 'Normal' intersection
                            if category_interval.start < src_interval.start:
                                # e.g.: 50,55 vs 49,52 -> 50,52 + 53,55
                                dst_intervals.append(Interval(src_interval.start, category_interval.end))
                                dst_intervals.append(Interval(category_interval.end + 1, src_interval.end))
                            else:
                                # e.g.: 50,55 vs 53,56 -> 50,52 + 53,55
                                dst_intervals.append(Interval(src_interval.start, category_interval.start - 1))
                                dst_intervals.append(Interval(category_interval.start, src_interval.end))
                assert all(i.start <= i.end for i in dst_intervals)

                src_intervals = dst_intervals

            # We are finished splitting, now iterate through again and apply deltas
            dst_intervals = []
            category_interval_idx = 0
            for src_interval in src_intervals:
                any_found = False
                while category_interval_idx < len(category.intervals):
                    category_interval, delta = category.intervals[category_interval_idx]
                    if category_interval.start > src_interval.end:
                        break

                    if src_interval.intersects(category_interval):
                        dst_intervals.append(Interval(src_interval.start + delta, src_interval.end + delta))
                        any_found = True
                        break

                    category_interval_idx += 1

                if not any_found:
                    dst_intervals.append(src_interval)

            src_intervals = dst_intervals

        return sorted(src_intervals)


@dataclass
class InputData:
    seeds: list[int]
    seed_ranges: list[tuple[int, int]]
    category_maps: list[CategoryRange]

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            seeds = list(map(int, f.readline().strip()[6:].split()))
            seed_itr = iter(seeds)
            seed_ranges = [Interval(start, start + len - 1) for start, len in zip(seed_itr, seed_itr)]
            category_maps = [CategoryRange.from_list_of_intervals(cls._parse_map_section(f)) for _ in range(7)]

            return cls(seeds, seed_ranges, category_maps)

    def _parse_map_section(file):
        file.readlines(2)
        ranges = []
        while (line := file.readline()) not in ('\n', ''):
            ranges.append(map(int, tuple(line.strip().split())))

        return ranges


input_data = InputData.from_file('input')
condenser = SeedCategoryCondenser(input_data.category_maps)
p1_location_ranges = condenser.convert_seed_ranges_to_location_ranges([Interval(n, n) for n in input_data.seeds])
p2_location_ranges = condenser.convert_seed_ranges_to_location_ranges(input_data.seed_ranges)

print(f'Part 1: {p1_location_ranges[0].start}')
print(f'Part 2: {p2_location_ranges[0].start}')