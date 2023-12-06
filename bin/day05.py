from advent import input
import collections
import itertools
import re
from dataclasses import dataclass


def main():
    seeds, *hunks = input.hunks()
    seeds = [int(n) for n in seeds[0].removeprefix("seeds: ").split()]

    # transformer = make_transformer(hunks)
    # print(min(transformer(seed) for seed in seeds))

    part_two(seeds, hunks)


# note: inclusive!
Range = collections.namedtuple('Range', ['start', 'end'])


def make_transformer(hunks):
    lookups = make_lookups(hunks)

    def fn(item):
        for lookup in lookups:
            for k, val in lookup.items():
                if k <= item < k + val.span:
                    item = val.dst + (item - val.src)
                    break

        return item

    return fn


def make_lookups(hunks):
    lookups = []

    for hunk in hunks:
        match = re.match(r"[a-z]+-to-(\w+) map", hunk[0])
        assert match is not None
        kind = match.group(1)
        _ = kind

        lookup = {}

        for line in hunk[1:]:
            dst, src, span = (int(n) for n in line.split())
            lookup[src] = Almanac(dst, src, span)

        lookups.append(lookup)

    return lookups


def part_two(seeds, hunks):
    lookups = make_lookups(hunks)
    print(lookups)

    for start, span in itertools.batched(seeds, 2):
        end = start + span - 1
        for stage in lookups:
            for a in stage.values():
                print(f"checking {start=}, {end=}, {a=}")
                if end < a.input.start:
                    print("left")
                elif a.input.end < start:
                    print("right")
                elif a.input.start <= start and end <= a.input.end:
                    print("contained")
                elif start < a.input.start:
                    print(f"dangle left; queue: {start}, {a.input.start}, {end}")
                elif start < a.input.end:
                    print(f"dangle right; queue: {start}, {a.input.end}, {a.input.end+1}, {end}")
                else:
                    print("dunno")
                    raise RuntimeError

            print("----")


@dataclass
class Almanac:
    dst: int
    src: int
    span: int

    @property
    def input(self) -> Range:
        return Range(self.src, self.src + self.span - 1)

    @property
    def output(self) -> Range:
        return Range(self.dst, self.dst + self.span - 1)

    def map(self, n) -> int:
        if n < self.input.start or n > self.input.end:
            return n

        return n + self.span



if __name__ == "__main__":
    main()
